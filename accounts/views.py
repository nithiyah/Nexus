
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .forms import VolunteerRegistrationForm, OrganisationRegistrationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth import get_user_model
from .forms import ProfileUpdateForm 
from django.shortcuts import render, redirect
from django.contrib import messages
from events.models import Event, VolunteerEvent, VolunteerParticipation
from announcements.models import Announcement
from django.db import models
from django.db.models import Sum

User = get_user_model()


def welcome(request):
    return render(request, 'accounts/welcome.html')


@login_required
def login_redirect(request):
    if request.user.user_type == 'organisation':
        return redirect('events:organisation_dashboard')  # Redirect to organisation dashboard
    else:
        return redirect('events:volunteer_dashboard')  # Redirect to volunteer dashboard


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

            # Build context for the email template
            context = {
                'username': user.username,
                'login_url': request.build_absolute_uri('/login/')
            }

            # Render HTML & plain-text versions
            html_message = render_to_string('accounts/welcome_email.html', context)
            plain_message = strip_tags(html_message)

            subject = "Welcome to Nexus!"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            print("EMAIL LOGIC TRIGGERED")
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=from_email,
                recipient_list=recipient_list,
                html_message=html_message,
                fail_silently=False,
            )
            messages.success(request, "Profile has been successfully created!")
            return render(request, 'accounts/registration_success.html')

        else:
            messages.error(request, "There were errors. Please correct them below.")
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

            # Build context for the email template
            context = {
                'username': user.username,
                'login_url': request.build_absolute_uri('/login/')
            }

            # Render HTML & plain-text versions
            html_message = render_to_string('accounts/welcome_email.html', context)
            plain_message = strip_tags(html_message)

            subject = "Welcome to Nexus (Organisation)!"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            print("EMAIL LOGIC TRIGGERED (ORG)")
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=from_email,
                recipient_list=recipient_list,
                html_message=html_message,
                fail_silently=False,
            )
            messages.success(request, "Profile has been successfully created!")
            return render(request, 'accounts/registration_success.html')

        else:
            messages.error(request, "There were errors. Please correct them below.")
    else:
        form = OrganisationRegistrationForm()
    
    return render(request, 'accounts/register_organisation.html', {'form': form})


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been successfully updated!")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})

@login_required
def update_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("update_profile")  
        else:
            messages.error(request, "There was an error updating your profile. Please try again.")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "profile.html", {"form": form})

# I was getting a reverse no match error 
class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done') 


from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from django.contrib.auth import logout

# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     template_name = 'accounts/password_reset_confirm.html'
#     success_url = reverse_lazy("accounts:password_reset_complete")

#     def dispatch(self, request, *args, **kwargs):
#         response = super().dispatch(request, *args, **kwargs)
#         try:
#             # del request.session['_password_reset_token']
#             self.request.session.pop('_password_reset_token', None)

#         except KeyError:
#             pass
#         return response

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy("accounts:password_reset_complete")

# @login_required
# def public_profile_view(request, username):
#     # Fetch and display another user's public profile 
#     profile_user = get_object_or_404(User, username=username)

#     # Ensure users cannot access their own profile through this view
#     if profile_user == request.user:
#         return redirect('accounts:profile')  # Redirect them to their own profile

#     return render(request, 'accounts/public_profile.html', {'profile_user': profile_user})

@login_required
def public_profile_view(request, username):
    # View another user's public profile, showing different details for volunteers and organisations
    profile_user = get_object_or_404(User, username=username)

    # Ensure users cannot access their own profile through this view
    if profile_user == request.user:
        return redirect('accounts:profile')  # Redirect them to their own profile

    events = None
    announcements = None
    registered_events = None
    total_hours = 0

    if profile_user.user_type == "organisation":
        # Get the events created by the organisation
        events = Event.objects.filter(organisation=profile_user)
        # Get the announcements made by the organisation
        announcements = Announcement.objects.filter(organisation=profile_user)

    elif profile_user.user_type == "volunteer":
        # Get the events the volunteer has registered for
        registered_events = VolunteerEvent.objects.filter(volunteer=profile_user).select_related('event')
        # Calculate total hours contributed
        total_hours = VolunteerParticipation.objects.filter(volunteer=profile_user).aggregate(total_hours=models.Sum('hours_contributed'))['total_hours'] or 0

    return render(request, "accounts/public_profile.html", {
        "profile_user": profile_user,
        "events": events,
        "announcements": announcements,
        "registered_events": registered_events,
        "total_hours": round(total_hours, 2),  # Rounded for cleaner display
    })

# @login_required
# def volunteer_event_report(request):
#     # Get the events the user participated in
#     volunteer_events = VolunteerEvent.objects.filter(volunteer=request.user)

#     # Calculate total hours from VolunteerParticipation model
#     total_hours = VolunteerParticipation.objects.filter(volunteer=request.user).aggregate(
#         total=Sum('hours_contributed')
#     )['total'] or 0

#     return render(request, 'accounts/volunteer_event_report.html', {
#         'volunteer_events': volunteer_events,
#         'total_hours': round(total_hours, 2),
#     })
@login_required
def volunteer_event_report(request):
    participations = VolunteerParticipation.objects.filter(
        volunteer=request.user,
        event__is_completed=True
    ).select_related('event')

    total_hours = participations.aggregate(total=Sum('hours_contributed'))['total'] or 0

    return render(request, 'accounts/volunteer_event_report.html', {
        'participations': participations,
        'total_hours': total_hours,
    })

# @login_required
# def volunteer_event_report(request):
#     # Fetch all participation entries
#     participations = VolunteerParticipation.objects.filter(volunteer=request.user).select_related('event')

#     # Loop through and auto-log hours if needed
#     for participation in participations:
#         event = participation.event
#         if event.date < timezone.now() and participation.hours_contributed == 0:
#             participation.hours_contributed = event.get_duration_hours()
#             participation.save()

#     total_hours = participations.aggregate(
#         total=Sum('hours_contributed')
#     )['total'] or 0

#     return render(request, 'accounts/volunteer_event_report.html', {
#         'volunteer_events': participations,
#         'total_hours': round(total_hours, 2),
#     })
