from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('dashboard/organisation/', views.organisation_dashboard, name='organisation_dashboard'),
    path('dashboard/volunteer/', views.volunteer_dashboard, name='volunteer_dashboard'),
    path('create/', views.create_event, name='create_event'),
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('my-events/', views.volunteer_events, name='volunteer_events'),
    path('register/<int:event_id>/', views.register_for_event, name='register_for_event'),
    path('cancel/<int:event_id>/', views.cancel_registration, name='cancel_registration'),  # Add this


]
