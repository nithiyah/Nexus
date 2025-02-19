# from django.shortcuts import render, redirect
# from django.contrib.auth import login
# from .forms import VolunteerRegistrationForm, OrganisationRegistrationForm
# from django.contrib.auth.views import LoginView
# from django.contrib.auth.decorators import login_required

# def welcome(request):
#     return render(request, 'accounts/welcome.html')

# @login_required
# def dashboard_redirect(request):
#     if request.user.user_type == 'volunteer':
#         return redirect('volunteer_dashboard')
#     elif request.user.user_type == 'organisation':
#         return redirect('organisation_dashboard')
#     else:
#         return redirect('login')

# def register_volunteer(request):
#     if request.method == 'POST':
#         form = VolunteerRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.user_type = 'volunteer'
#             user.save()
#             login(request, user)
#             return redirect('login')  # Redirect to login page after successful registration
#     else:
#         form = VolunteerRegistrationForm()
#     return render(request, 'accounts/register_volunteer.html', {'form': form})

# def register_organisation(request):
#     if request.method == 'POST':
#         form = OrganisationRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.user_type = 'organisation'
#             user.save()
#             login(request, user)
#             return redirect('login')  # Redirect to login page after successful registration
#     else:
#         form = OrganisationRegistrationForm()
#     return render(request, 'accounts/register_organisation.html', {'form': form})

# class CustomLoginView(LoginView):
#     template_name = 'accounts/login.html'

#     from django.shortcuts import render
# from django.contrib.auth.decorators import login_required

# @login_required
# def volunteer_dashboard(request):
#     return render(request, 'accounts/volunteer_dashboard.html')

# @login_required
# def organisation_dashboard(request):
#     return render(request, 'accounts/organisation_dashboard.html')


# # @login_required
# # def organisation_dashboard_redirect(request):
# #     return redirect('organisation_dashboard')  # This will redirect to the events app dashboard


# @login_required
# def login_redirect(request):
#     if request.user.user_type == 'organisation':
#         return redirect('organisation_dashboard')
#     else:
#         return redirect('volunteer_dashboard')  # Adjust if you have a volunteer view

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import VolunteerRegistrationForm, OrganisationRegistrationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm


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
            return redirect('login')
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
            return redirect('login')
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