from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class VolunteerRegistrationForm(UserCreationForm):

    full_name = forms.CharField(max_length=255, required=True, help_text="Enter your full name.") 
    contact_number = forms.CharField(max_length=10, required=True, help_text= "Enter your contact number.")
    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'email', 'contact_number',
                   'password1', 'password2']

class OrganisationRegistrationForm(UserCreationForm):
    organisation_name = forms.CharField(max_length=255, required=True)
    personnel_name = forms.CharField(max_length=255, required=True, help_text="Enter the personnel contact name.")
    contact_number = forms.CharField(max_length=10, required=True, help_text= "Enter your contact number.")

    class Meta:
        model = CustomUser
        fields = ['organisation_name', 'personnel_name', 'username', 
                  'email', 'contact_number', 'password1', 'password2']


# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['profile_picture', 'full_name', 'email', 'contact_number']
#         widgets = {
#             'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
#         }

# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['profile_picture', 'full_name', 'email', 'contact_number']
#         widgets = {
#             'full_name': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
#             'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
#         }
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'full_name', 'email', 'contact_number']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'readonly': 'readonly', 'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
