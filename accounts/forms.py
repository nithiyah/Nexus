from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class VolunteerRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class OrganisationRegistrationForm(UserCreationForm):
    organisation_name = forms.CharField(max_length=255, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'organisation_name', 'password1', 'password2']
