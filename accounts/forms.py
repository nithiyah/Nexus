from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class VolunteerRegistrationForm(UserCreationForm):

    contact_number = forms.CharField(max_length=10, required=True, help_text= "Enter your contact number.")
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'contact_number', 'password1', 'password2']

class OrganisationRegistrationForm(UserCreationForm):
    organisation_name = forms.CharField(max_length=255, required=True)
    contact_number = forms.CharField(max_length=10, required=True, help_text= "Enter your contact number.")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'contact_number', 'organisation_name', 'password1', 'password2']
