from django import forms
from django.forms import inlineformset_factory
from .models import CVProfile, WorkExperience, Reference, Attachment

class CVProfileForm(forms.ModelForm):
    class Meta:
        model = CVProfile
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'email', 'phone', 'address',
            'profile_picture', 'resume_color', 'payment_package',
            'highest_qualification', 'summary', 'skills', 'hobbies'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Address'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'resume_color': forms.Select(attrs={'class': 'select'}),
            'payment_package': forms.Select(attrs={'class': 'select'}),
            'highest_qualification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Qualification'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write Summary'}),
            'skills': forms.SelectMultiple(attrs={'class': 'select'}),
            'hobbies': forms.SelectMultiple(attrs={'class': 'select'}),
        }

class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = ['company_name', 'job_title', 'start_date', 'end_date', 'description']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Company Name'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Job Title'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Job Description'}),
        }

class ReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = ['name', 'relationship', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name'}),
            'relationship': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Relationship'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone'}),
        }

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }

# Formsets
WorkExperienceFormSet = inlineformset_factory(
    CVProfile, WorkExperience, form=WorkExperienceForm, extra=1, can_delete=True
)

ReferenceFormSet = inlineformset_factory(
    CVProfile, Reference, form=ReferenceForm, extra=1, can_delete=True
)

AttachmentFormSet = inlineformset_factory(
    CVProfile, Attachment, form=AttachmentForm, extra=1, can_delete=True
)
