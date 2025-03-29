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
    path('organisation-events/', views.organisation_events, name='organisation_events'),
    path('register/<int:event_id>/', views.register_for_event, name='register_for_event'),
    path('cancel/<int:event_id>/', views.cancel_registration, name='cancel_registration'),  
    path('remove-volunteer/<int:registration_id>/', views.remove_volunteer, name='remove_volunteer'),
    path('publish-feedback/<int:event_id>/', views.publish_feedback, name='publish_feedback'),
    # path('submit-feedback/<int:event_id>/', views.submit_feedback, name='submit_feedback'),
    path('view-feedback/<int:event_id>/', views.view_feedback, name='view_feedback'),
    path('create-feedback/<int:event_id>/', views.create_feedback_form, name='create_feedback_form'),
    path("complete-feedback/<int:event_id>/", views.complete_feedback, name="complete_feedback"),
    # path('feedback-hub/', views.feedback_hub, name='feedback_hub'),
    path('volunteer-list/<int:event_id>/', views.volunteer_list, name='volunteer_list'),
    path('complete-event/<int:event_id>/', views.complete_event, name='complete_event'),

    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/feedback/', views.feedback_event_page, name='feedback_event_page'),
    path("complete-event/<int:event_id>/", views.complete_event, name="complete_event"),


# path('feedback/event/<int:event_id>/', views.feedback_event_page, name='feedback_event_page'),



]
