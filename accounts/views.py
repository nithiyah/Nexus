
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

User = get_user_model()



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

            # Build context for the email template
            context = {
                'username': user.username,
                'login_url': request.build_absolute_uri('/login/')  
                  # or "https://yourdomain.com/login/"
            }

            # Render HTML & plain-text versions
            html_message = render_to_string('accounts/welcome_email.html', context)
            plain_message = strip_tags(html_message)

            subject = "Welcome to Nexus!"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]

            send_mail(
                subject=subject,
                message=plain_message,        # fallback if recipient can’t read HTML
                from_email=from_email,
                recipient_list=recipient_list,
                html_message=html_message,    # our HTML version
                fail_silently=False,
            )



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
    

@login_required
def public_profile_view(request, username):
    # Fetch and display another user's public profile 
    profile_user = get_object_or_404(User, username=username)

    # Ensure users cannot access their own profile through this view
    if profile_user == request.user:
        return redirect('accounts:profile')  # Redirect them to their own profile

    return render(request, 'accounts/public_profile.html', {'profile_user': profile_user})
