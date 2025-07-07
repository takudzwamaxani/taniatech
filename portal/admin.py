from django.contrib import admin
from .models  import *
from django.utils.html import format_html

# Lookup Models Admin

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(JobType)
class JobTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(JobLevel)
class JobLevelAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ("name", "country")
    list_filter = ("country",)
    search_fields = ("name",)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "state")
    list_filter = ("state",)
    search_fields = ("name",)


# Job Model Admin

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "job_type",
        "job_level",
        "country",
        "state",
        "city",
        "start_date",
        "end_date",
        "created_at",
    )
    list_filter = (
        "category",
        "job_type",
        "job_level",
        "gender",
        "country",
        "state",
        "city",
        "start_date",
    )
    search_fields = ("title", "qualification", "required_skills", "description")
    date_hierarchy = "start_date"


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(PaymentPackage)
class PaymentPackageAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    search_fields = ("name",)

admin.site.register(Attachment) 
class WorkExperienceInline(admin.TabularInline):
    model = WorkExperience
    extra = 1


class ReferenceInline(admin.TabularInline):
    model = Reference
    extra = 1
    
class AttachmentsInline(admin.TabularInline):
    model = Attachment
    extra = 1



@admin.register(CVProfile)
class CVProfileAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "payment_package", "created_at")
    search_fields = ("first_name", "last_name", "email")
    list_filter = ("payment_package", "resume_color")
    inlines = [WorkExperienceInline, ReferenceInline, AttachmentsInline]
    
    
    
@admin.register(ContactInformation)
class ContactInformationAdmin(admin.ModelAdmin):
    list_display = ("company_name", "phone_primary", "email_primary", "updated_at")
    search_fields = ("company_name", "phone_primary", "email_primary")


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(NewsTag)
class NewsTagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "category", "published_date", "created_at")
    list_filter = ("status", "category", "tags", "published_date")
    search_fields = ("title", "summary", "content")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_date"
    
    

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'logo_preview')
    search_fields = ('name', 'website')

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:50px;" />', obj.logo.url)
        return "-"
    logo_preview.short_description = 'Logo'