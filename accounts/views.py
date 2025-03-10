
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import VolunteerRegistrationForm, OrganisationRegistrationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy


def welcome(request):
    return render(request, 'accounts/welcome.html')


@login_required
def login_redirect(request):
    if request.user.user_type == 'organisation':
        return redirect('events:organisation_dashboard')  # Redirect to events app
    else:
        return redirect('events:volunteer_dashboard')  # Redirect to events app


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'


# Registration Views
def register_volunteer(request):
    if request.method == 'POST':
        form = VolunteerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'volunteer'
            user.save()
            login(request, user)
            return redirect('accounts:login')
    else:
        form = VolunteerRegistrationForm()
    return render(request, 'accounts/register_volunteer.html', {'form': form})


def register_organisation(request):
    if request.method == 'POST':
        form = OrganisationRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'organisation'
            user.save()
            login(request, user)
            return redirect('accounts:login')
    else:
        form = OrganisationRegistrationForm()
    return render(request, 'accounts/register_organisation.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user  # Get logged-in user
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')  # Redirect to profile page after saving
    else:
        form = ProfileUpdateForm(instance=user)
    
    return render(request, 'accounts/profile.html', {'form': form})

# I was getting a reverse no match error 
class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done') 


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'

    def form_valid(self, form):
        # Log out the user before setting a new password
        logout(self.request)
        return super().form_valid(form)