#from django.urls import path
from . import views
from django.urls import path
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView, LoginView
from .views import welcome, register_volunteer, register_organisation
from .views import profile_view
from .views import CustomPasswordResetView, CustomPasswordResetConfirmView
from django.contrib.auth import views as auth_views

app_name = 'accounts'  # Ensures 'accounts:profile' works
urlpatterns = [
    path('', welcome, name='home'),  # Root URL for welcome page
    path('login/', CustomLoginView.as_view(), name='login'), 
    path('register/volunteer/', views.register_volunteer, name='register_volunteer'),
    path('register/organisation/', views.register_organisation, name='register_organisation'),
    path('login/redirect/', views.login_redirect, name='login_redirect'),  # Custom redirect
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    
    # Password Reset
    # path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html', email_template_name='accounts/password_reset_email.html'), 
    #                                                               name='password_reset'),
    # path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
    #     template_name='accounts/password_reset_done.html'
    # ), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),


    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),





]



# urlpatterns += [
#     path('logout/', LogoutView.as_view(), name='logout'),
#     path('dashboard/volunteer/', volunteer_dashboard, name='volunteer_dashboard'),
#     path('dashboard/organisation/', organisation_dashboard, name='organisation_dashboard'),
# ]