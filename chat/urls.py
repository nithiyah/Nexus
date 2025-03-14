from django.urls import path
from .views import chat_home, chat_room, send_message, get_online_users  
from . import views

app_name = "chat"

urlpatterns = [
    path('', chat_home, name='chat_home'),
    # path('room/<int:event_id>/', chat_room, name='chat_room'),
    path('room/<int:event_id>/', chat_room, name='chat_room'),
    path('send_message/<int:event_id>/', send_message, name='send_message'),
    path('get_online_users/<int:event_id>/', get_online_users, name='get_online_users'),
    path("unread_messages_count/", views.unread_messages_count, name="unread_messages_count"),  
]
