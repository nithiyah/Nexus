#from django.urls import path
from . import views
from django.urls import path
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView
from .views import welcome, organisation_dashboard, volunteer_dashboard, register_volunteer, register_organisation

urlpatterns = [
    path('', welcome, name='home'),  # Root URL for welcome page
    path('login/', CustomLoginView.as_view(), name='login'), 
    path('register/volunteer/', views.register_volunteer, name='register_volunteer'),
    path('register/organisation/', views.register_organisation, name='register_organisation'),
    path('dashboard/organisation/', views.organisation_dashboard, name='organisation_dashboard'),
    path('dashboard/volunteer/', views.volunteer_dashboard, name='volunteer_dashboard'),

    # path('dashboard/', dashboard_redirect, name='dashboard_redirect'),
    path('login/redirect/', views.login_redirect, name='login_redirect'),  # Custom redirect

]

urlpatterns += [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/volunteer/', volunteer_dashboard, name='volunteer_dashboard'),
    path('dashboard/organisation/', organisation_dashboard, name='organisation_dashboard'),
]