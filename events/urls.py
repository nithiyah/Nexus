# from django.urls import path
# from . import views

# urlpatterns = [
#     path('dashboard/', views.organisation_dashboard, name='organisation_dashboard'),
#     path('create/', views.create_event, name='create_event'),
#     path('edit/<int:event_id>/', views.edit_event, name='edit_event'),
#     path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
# ]

from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('dashboard/organisation/', views.organisation_dashboard, name='organisation_dashboard'),
    path('dashboard/volunteer/', views.volunteer_dashboard, name='volunteer_dashboard'),
    path('create/', views.create_event, name='create_event'),
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
]
