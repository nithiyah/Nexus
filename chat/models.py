from django.db import models
from django.conf import settings
from events.models import Event  

class ChatRoom(models.Model):

    # each event = 1 chat room
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name="chatroom")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat Room for {self.event.name}"

class Message(models.Model):

    # messages in a chat room itself 
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)

    # add file field to store files, file support
    file = models.FileField(upload_to="chat_uploads/", blank=True, null=True)  
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        if self.content:
            return f"{self.sender.username}: {self.content[:30]}"
        elif self.file:
            return f"{self.sender.username}: [File Uploaded]"
        else:
            return f"{self.sender.username}: [Empty Message]"

