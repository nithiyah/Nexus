#from django.urls import path
from . import views
from django.urls import path
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView, LoginView
from .views import welcome, register_volunteer, register_organisation
from .views import profile_view
from .views import CustomPasswordResetView, CustomPasswordResetConfirmView
from django.contrib.auth import views as auth_views
from .views import update_profile
from django.conf import settings
from django.conf.urls.static import static

app_name = 'accounts'  # Ensures 'accounts:profile' works
urlpatterns = [
    path('', welcome, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'), 
    path('register/volunteer/', views.register_volunteer, name='register_volunteer'),
    path('register/organisation/', views.register_organisation, name='register_organisation'),
    path('login/redirect/', views.login_redirect, name='login_redirect'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', update_profile, name='update_profile'),
    path('profile/event-report/', views.volunteer_event_report, name='volunteer_event_report'),  # keep this OR the line below
    # path('report/', views.volunteer_event_report, name='volunteer_event_report'),

    path('profile/<str:username>/', views.public_profile_view, name='public_profile'),

    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]
