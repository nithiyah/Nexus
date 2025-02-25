from django.urls import path
from .views import chat_room, delete_chat_room, chat_home, send_message

app_name = "chat"

urlpatterns = [
    path('', chat_home, name='chat_home'),  # Homepage for Chat
    path('room/<int:event_id>/', chat_room, name='chat_room'),  # Make sure this matches the event.id call
    # path("<int:event_id>/", chat_room, name="chat_room"),
    path("<int:event_id>/delete/", delete_chat_room, name="delete_chat_room"),
    path("send_message/<int:event_id>/", send_message, name="send_message"),

    
]
