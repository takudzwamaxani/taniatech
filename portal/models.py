from django.db import models
from django.contrib.auth.models import User

# Lookup tables

class JobCategory(models.Model):
    name = models.CharField(max_length=100)
    icon_class = models.CharField(
        max_length=100, 
        blank=True,   # allow empty if no icon specified
        help_text="CSS class for the icon (e.g., 'fas fa-briefcase')"
    )

    class Meta:
        verbose_name_plural = "Job Categories"

    def __str__(self):
        return self.name



class JobType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Job Types"

    def __str__(self):
        return self.name


class JobLevel(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Job Levels"

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "States"

    def __str__(self):
        return f"{self.name}, {self.country.name}"


class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return f"{self.name}, {self.state.name}"




class Organization(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='organizations/logos/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    application_instructions = models.TextField(
        blank=True,
        help_text="Instructions on how to apply for jobs at this organization."
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Organizations"

    def __str__(self):
        return self.name


class Job(models.Model):
    GENDER_CHOICES = [
        ('Any', 'Any'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    title = models.CharField(max_length=200)
    category = models.ForeignKey('JobCategory', on_delete=models.SET_NULL, null=True)
    job_type = models.ForeignKey('JobType', on_delete=models.SET_NULL, null=True)
    job_level = models.ForeignKey('JobLevel', on_delete=models.SET_NULL, null=True)

    offered_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    experience = models.CharField(max_length=100, blank=True)
    qualification = models.CharField(max_length=255, blank=True)
    required_skills = models.TextField(
        blank=True,
        help_text="Enter skills separated by commas. Example: Figma, Adobe XD, Photoshop"
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Any')
    age = models.CharField(max_length=50, blank=True)

    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey('State', on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True)

    zip_code = models.CharField(max_length=20, blank=True)
    full_address = models.TextField(blank=True)

    start_date = models.DateField()
    end_date = models.DateField()

    description = models.TextField()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        related_name='jobs',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Jobs"

    def __str__(self):
        return f"{self.title} at {self.organization.name if self.organization else 'Unknown Organization'}"

class Skill(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Skills"

    def __str__(self):
        return self.name


class Hobby(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Hobbies"

    def __str__(self):
        return self.name


class PaymentPackage(models.Model):
    PACKAGE_CHOICES = [
        ('Basic', 'Basic - $10 (2 CV concepts)'),
        ('Pro', 'Pro - $20 (5 CV concepts + unlimited changes)'),
    ]
    name = models.CharField(max_length=20, choices=PACKAGE_CHOICES, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name_plural = "Payment Packages"

    def __str__(self):
        return f"{self.get_name_display()} - ${self.price}"


class CVProfile(models.Model):
    RESUME_COLOR_CHOICES = [
        ('Blue', 'Blue'),
        ('Green', 'Green'),
        ('Gray', 'Gray'),
        ('Black', 'Black'),
        ('Custom', 'Custom Color'),
    ]

    # Bio Data
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    address = models.TextField()
    profile_picture = models.ImageField(upload_to='cv/profile_pictures/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cv_profiles')

    # Resume Preferences
    resume_color = models.CharField(max_length=20, choices=RESUME_COLOR_CHOICES, default='Blue')
    payment_package = models.ForeignKey(PaymentPackage, on_delete=models.SET_NULL, null=True)

    # Qualifications
    highest_qualification = models.CharField(max_length=255, blank=True)
    summary = models.TextField(blank=True, help_text="Brief professional summary")

    # Skills and Hobbies
    skills = models.ManyToManyField(Skill, blank=True)
    hobbies = models.ManyToManyField(Hobby, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "CV Profiles"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class WorkExperience(models.Model):
    cv_profile = models.ForeignKey(CVProfile, related_name="work_experiences", on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Work Experiences"

    def __str__(self):
        return f"{self.job_title} at {self.company_name}"


class Reference(models.Model):
    cv_profile = models.ForeignKey(CVProfile, related_name="references", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name_plural = "References"

    def __str__(self):
        return f"{self.name} ({self.relationship})"


class Attachment(models.Model):
    cv_profile = models.ForeignKey(CVProfile, related_name="attachments", on_delete=models.CASCADE)
    file = models.FileField(upload_to='cv/attachments/')

    class Meta:
        verbose_name_plural = "Attachments"

    def __str__(self):
        return f"Attachment for {self.cv_profile}"

class ContactInformation(models.Model):
    company_name = models.CharField(max_length=255, blank=True)
    address = models.TextField()
    phone_primary = models.CharField(max_length=50, blank=True)
    phone_secondary = models.CharField(max_length=50, blank=True)
    email_primary = models.EmailField(blank=True)
    email_secondary = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    # Social Media
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    whatsapp_number = models.CharField(
        max_length=50, 
        blank=True,
        help_text="Enter WhatsApp number in international format, e.g., +2637..."
    )

    # Google Maps Embed
    google_maps_embed_url = models.URLField(
    blank=True,
    max_length=1000,  # Increase the max length as needed
    help_text="Paste the Google Maps embed URL here."
)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Contact Information"

    def __str__(self):
        return self.company_name or "Contact Information"



class NewsCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, help_text="Used in URLs")

    class Meta:
        verbose_name_plural = "News Categories"

    def __str__(self):
        return self.name


class NewsTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "News Tags"

    def __str__(self):
        return self.name



class NewsArticle(models.Model):
    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Published', 'Published'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(
        NewsCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="articles"
    )
    tags = models.ManyToManyField(NewsTag, blank=True, related_name="articles")
    author = models.CharField(max_length=100, blank=True)
    featured_image = models.ImageField(
        upload_to="news/featured_images/",
        blank=True,
        null=True
    )
    summary = models.TextField(help_text="Short summary of the article.")
    content = models.TextField(help_text="Full article content in HTML or Markdown.")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Draft")
    published_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "News Articles"
        ordering = ["-published_date", "-created_at"]

    def __str__(self):
        return self.title
