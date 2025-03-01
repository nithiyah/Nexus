from django.db import models
from django.conf import settings
from events.models import Event  

class ChatRoom(models.Model):
    """Each event has one chat room."""
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name="chatroom")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat Room for {self.event.name}"

class Message(models.Model):
    """Messages within a chat room."""
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"
