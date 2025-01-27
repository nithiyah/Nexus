from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import VolunteerRegistrationForm, OrganisationRegistrationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

def welcome(request):
    return render(request, 'accounts/welcome.html')

@login_required
def dashboard_redirect(request):
    if request.user.user_type == 'volunteer':
        return redirect('volunteer_dashboard')
    elif request.user.user_type == 'organisation':
        return redirect('organisation_dashboard')
    else:
        return redirect('login')

def register_volunteer(request):
    if request.method == 'POST':
        form = VolunteerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'volunteer'
            user.save()
            login(request, user)
            return redirect('login')  # Redirect to login page after successful registration
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
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = OrganisationRegistrationForm()
    return render(request, 'accounts/register_organisation.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def volunteer_dashboard(request):
    return render(request, 'accounts/volunteer_dashboard.html')

@login_required
def organisation_dashboard(request):
    return render(request, 'accounts/organisation_dashboard.html')
