from django.shortcuts import render
from django.shortcuts import render
from .models import Job, JobCategory, NewsArticle, ContactInformation
from django.utils import timezone
from django.shortcuts import render
from .models import *
from django.shortcuts import render, get_object_or_404
from .models import NewsArticle, NewsTag
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from .models import Job, JobCategory, JobType, JobLevel, NewsArticle, ContactInformation
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.timezone import now, timedelta
from django.shortcuts import render
from .models import Job, JobCategory, JobLevel, JobType, Country, State, City, NewsArticle, ContactInformation
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.timezone import now
from datetime import timedelta
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import NewsArticle, NewsCategory, NewsTag
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactInformation
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CVProfile
from .forms import *

from django.contrib import messages
from django.shortcuts import render, redirect

def cvprofile_manage(request):
    # Get the CVProfile for this user, or None if not created yet
    cvprofile = CVProfile.objects.filter(user=request.user).first()

    if request.method == 'POST':
        if 'delete' in request.POST and cvprofile:
            cvprofile.delete()
            messages.success(request, 'Your CV Profile was deleted successfully.')
            return redirect('cvs')

        form = CVProfileForm(request.POST, request.FILES, instance=cvprofile)
        workexp_formset = WorkExperienceFormSet(request.POST, request.FILES, instance=cvprofile)
        reference_formset = ReferenceFormSet(request.POST, request.FILES, instance=cvprofile)
        attachment_formset = AttachmentFormSet(request.POST, request.FILES, instance=cvprofile)

        if (
            form.is_valid()
            and workexp_formset.is_valid()
            and reference_formset.is_valid()
            and attachment_formset.is_valid()
        ):
            cvprofile = form.save(commit=False)
            cvprofile.user = request.user
            cvprofile.save()
            form.save_m2m()

            workexp_formset.instance = cvprofile
            workexp_formset.save()

            reference_formset.instance = cvprofile
            reference_formset.save()

            attachment_formset.instance = cvprofile
            attachment_formset.save()

            messages.success(request, 'Your CV Profile has been saved successfully.')
            return redirect('cvs')
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = CVProfileForm(instance=cvprofile)
        workexp_formset = WorkExperienceFormSet(instance=cvprofile)
        reference_formset = ReferenceFormSet(instance=cvprofile)
        attachment_formset = AttachmentFormSet(instance=cvprofile)
        
    skills = list(Skill.objects.values_list('name', flat=True))
    hobbies = list(Hobby.objects.values_list('name', flat=True))

    context = {
        'form': form,
        'workexp_formset': workexp_formset,
        'reference_formset': reference_formset,
        'attachment_formset': attachment_formset,
        'cvprofile': cvprofile,
        "skills": skills,
        "hobbies": hobbies
    }
    return render(request, 'cvs.html', context)


def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        associated_users = User.objects.filter(email=email)
        if associated_users.exists():
            for user in associated_users:
                # Generate token and UID
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                # Build password reset URL
                reset_url = request.build_absolute_uri(f'/reset/{uid}/{token}/')
                
                # Prepare email
                subject = "Password Reset Requested"
                message = render_to_string('password_reset_email.txt', {
                    'user': user,
                    'reset_url': reset_url,
                })
                send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
            messages.success(request, "A password reset link has been sent to your email.")
            return redirect('forgot')
        else:
            messages.error(request, "No user is associated with this email address.")
            return redirect('forgot')
    return render(request, 'forgot-password.html')


def signup(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        agree = request.POST.get("agree")

        # Validate agreement
        if not agree:
            messages.error(request, "You must agree to the Terms of Service.")
            return render(request, "signup.html")

        # Validate existing user
        if User.objects.filter(email=email).exists():
            messages.error(request, "A user with this email already exists.")
            return render(request, "signup.html")

        # Validate password
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return render(request, "signup.html")

        # Create user (using email as username)
        username = email
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = full_name
        user.save()

        messages.success(request, "Your account was created successfully. You can now log in.")
        return redirect("login")  # Update 'login' to match your login URL name

    return render(request, "signup.html",{'contact_info': ContactInformation.objects.last()})

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember = request.POST.get("remember")
        next_url = request.POST.get("next")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)

            # Handle session expiry for "Remember Me"
            if not remember:
                request.session.set_expiry(0)  # Expires on browser close
            else:
                request.session.set_expiry(1209600)  # 2 weeks

            # Redirect to next if provided
            if next_url:
                return redirect(next_url)
            return redirect("home")  # Or your desired success URL
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html",{'contact_info': ContactInformation.objects.last()})


def contact(request):
    contact_info = ContactInformation.objects.last()  # or .first() if you prefer

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        # Compose email body
        email_body = f"""
        You have a new contact form submission:

        Name: {name}
        Email: {email}
        Subject: {subject}

        Message:
        {message}
        """

        try:
            send_mail(
                subject=f"New Contact Form Submission: {subject}",
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[contact_info.email_primary or settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
            return redirect("contact")
        except Exception as e:
            messages.error(request, f"An error occurred while sending the message: {e}")

    return render(request, "contact.html", {
        "contact_info": contact_info
        
    })


def about(request):
    return render(request, 'coming-soon.html')

def cvs(request):
    return render(request, 'cvs.html')

def faq(request):
    return render(request, 'coming-soon.html')

def tos(request):
    return render(request, 'coming-soon.html')


def forgot(request):
    return render(request, 'forgot-password.html',{'contact_info': ContactInformation.objects.last()})

def privacy(request):
    return render(request, 'coming-soon.html')

def guide(request):
    return render(request, 'coming-soon.html')

def chat(request):
    return render(request, 'coming-soon.html')



def news(request):
    articles = NewsArticle.objects.select_related('category').prefetch_related('tags').filter(status="Published")
    # Keyword search
    keyword = request.GET.get("keyword")
    if keyword:
        articles = articles.filter(
            Q(title__icontains=keyword) |
            Q(summary__icontains=keyword) |
            Q(content__icontains=keyword)
        )

    # Category filter
    category_slug = request.GET.get("category")
    if category_slug:
        articles = articles.filter(category__slug=category_slug)

    # Tag filter
    tag_slug = request.GET.get("tag")
    if tag_slug:
        articles = articles.filter(tags__slug=tag_slug)

    # Pagination
    paginator = Paginator(articles, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "articles": page_obj,
        "categories": NewsCategory.objects.all(),
        "tags": NewsTag.objects.all(),
        "selected_category": category_slug or "",
        "selected_tag": tag_slug or "",
        "keyword": keyword or "",
        'contact_info': ContactInformation.objects.last(),
    }
    return render(request, "blog.html", context)


def team(request):
    return render(request, 'coming-soon.html')



def logout(request):
    return render(request, 'team.html')

def register(request):
    return render(request, 'register.html')

def support_center(request):
    return render(request, 'coming-soon.html')

def plans(request):
    return render(request, 'coming-soon.html')

def sitemap(request):
    return render(request, 'coming-soon.html')

def index(request):
    latest_jobs = Job.objects.select_related('organization', 'category', 'job_type', 'city').order_by('-created_at')[:6]
    
    # Add split skills to each job object
    for job in latest_jobs:
        job.skills_list = [skill.strip() for skill in job.required_skills.split(',') if skill.strip()]

    context = {
        'latest_jobs': latest_jobs,
        'categories': JobCategory.objects.all(),
        'latest_news': NewsArticle.objects.filter(status="Published").order_by('-published_date')[:3],
        'contact_info': ContactInformation.objects.last(),
    }
    return render(request, 'index.html', context)


def news_detail(request, slug):
    article = get_object_or_404(
        NewsArticle.objects.select_related('category').prefetch_related('tags'),
        slug=slug,
        status="Published"
    )

    # Related articles from the same category
    related_articles = (
        NewsArticle.objects.filter(category=article.category, status="Published")
        .exclude(id=article.id)
        .order_by("-published_date")[:3]
    )

    context = {
        "article": article,
        "related_articles": related_articles,
        "categories": NewsCategory.objects.all(),
        "tags": NewsTag.objects.all(),
        'contact_info': ContactInformation.objects.last(),
    }
    return render(request, "blog-single.html", context)



def job_detail(request, id):
    job = get_object_or_404(
        Job.objects.select_related(
            'category', 'job_type', 'job_level', 'country', 'state', 'city', 'organization'
        ),
        id=id
    )

    # Split the skills (if any)
    required_skills = [s.strip() for s in job.required_skills.split(',')] if job.required_skills else []

    related_jobs = (
        Job.objects.filter(category=job.category)
        .exclude(id=job.id)
        .order_by('-created_at')[:3]
    )

    context = {
        'job': job,
        'required_skills': required_skills,
        'related_jobs': related_jobs,
        'contact_info': ContactInformation.objects.last(),
    }

    return render(request, 'jobsingle.html', context)


def jobs(request):
    # Base queryset with select_related for efficiency
    jobs = Job.objects.select_related(
        'category', 'job_type', 'job_level', 'country', 'state', 'city'
    )

    # Keyword search
    keyword = request.GET.get('keyword')
    if keyword:
        jobs = jobs.filter(
            Q(title__icontains=keyword) |
            Q(description__icontains=keyword) |
            Q(required_skills__icontains=keyword)
        )

    # Location filter (country name)
    location = request.GET.get('location')
    if location:
        jobs = jobs.filter(country__name__iexact=location)

    # Category (checkbox)
    category = request.GET.getlist('category')
    if category:
        jobs = jobs.filter(category_id__in=category)

    # Job Types (checkboxes)
    job_types = request.GET.getlist('job-type')
    if job_types:
        jobs = jobs.filter(job_type_id__in=job_types)

    # Experience Levels (checkboxes)
    experience_levels = request.GET.getlist('experience')
    if experience_levels:
        jobs = jobs.filter(job_level_id__in=experience_levels)

    # Job Posted (checkboxes)
    posted = request.GET.getlist('job-posted')
    if posted:
        now_time = now()
        posted_filter = Q()
        for val in posted:
            if val == '2':
                posted_filter |= Q(created_at__gte=now_time - timedelta(hours=1))
            elif val == '3':
                posted_filter |= Q(created_at__gte=now_time - timedelta(days=1))
            elif val == '4':
                posted_filter |= Q(created_at__gte=now_time - timedelta(days=7))
            elif val == '5':
                posted_filter |= Q(created_at__gte=now_time - timedelta(days=30))
        jobs = jobs.filter(posted_filter)

    # Gender filter (single select)
    selected_gender = request.GET.get('gender')
    if selected_gender and selected_gender != "Any":
        jobs = jobs.filter(gender__iexact=selected_gender)

    # Country, State, City (dropdowns)
    selected_country = request.GET.get('country')
    if selected_country:
        jobs = jobs.filter(country_id=selected_country)

    selected_state = request.GET.get('state')
    if selected_state:
        jobs = jobs.filter(state_id=selected_state)

    selected_city = request.GET.get('city')
    if selected_city:
        jobs = jobs.filter(city_id=selected_city)

    # Sort options
    sort = request.GET.get('sort')
    if sort == 'latest':
        jobs = jobs.order_by('-created_at')
    elif sort == 'salary-asc':
        jobs = jobs.order_by('salary_min')
    elif sort == 'salary-desc':
        jobs = jobs.order_by('-salary_max')
    else:
        jobs = jobs.order_by('-created_at')

    # Pagination
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Context variables
    context = {
        'jobs': page_obj,
        'categories': JobCategory.objects.all(),
        'job_types': JobType.objects.all(),
        'job_levels': JobLevel.objects.all(),
        'countries': Country.objects.all(),
        'states': State.objects.all(),
        'cities': City.objects.all(),
        'latest_news': NewsArticle.objects.filter(status="Published").order_by('-published_date')[:3],
        'contact_info': ContactInformation.objects.last(),

        # Selected filters
        'selected_categories': category,
        'selected_job_types': job_types,
        'selected_experience_levels': experience_levels,
        'selected_posted': posted,
        'selected_gender': selected_gender or "",
        'selected_country': selected_country or "",
        'selected_state': selected_state or "",
        'selected_city': selected_city or "",
        'selected_sort': sort or "",

        # Filter options
        'job_posted_options': [
            ('1', 'All'),
            ('2', 'Last Hour'),
            ('3', 'Last 24 Hours'),
            ('4', 'Last 7 Days'),
            ('5', 'Last 30 Days'),
        ],
        'gender_options': [
            ('Any', 'Any'),
            ('Male', 'Male'),
            ('Female', 'Female'),
        ],
    }

    return render(request, 'jobs.html', context)
