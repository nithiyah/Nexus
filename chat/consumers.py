import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import ChatRoom, Message

from datetime import datetime, timedelta
from django.utils.timezone import now


from channels.sessions import SessionMiddlewareStack
from channels.auth import AuthMiddlewareStack

async def receive(self, text_data):
    """Handle incoming messages and save to database."""
    data = json.loads(text_data)
    sender = self.scope["user"]
    message = data["message"]

    #  Get current Singapore Time without adding extra hours
    singapore_time = now().strftime("%H:%M")  #  Remove timedelta adjustment

    chatroom = await sync_to_async(ChatRoom.objects.get)(event__id=self.event_id)
    message_obj = await sync_to_async(Message.objects.create)(
        chatroom=chatroom, sender=sender, content=message
    )

    #  Send correctly formatted timestamp
    await self.channel_layer.group_send(
        self.room_group_name, {
            "type": "chat_message",
            "message": message_obj.content,
            "sender": sender.username,
            "timestamp": singapore_time,  #  Now uses correct Singapore Time
        }
    )
from channels.auth import get_user
from django.contrib.auth.models import AnonymousUser
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Accept WebSocket connection."""
        self.event_id = self.scope["url_route"]["kwargs"]["event_id"]
        self.room_group_name = f"chat_{self.event_id}"  # Ensure it matches `routing.py`
 ###############################################################################

        # Ensure user authentication for WebSocket
        # self.scope["user"] = await sync_to_async(get_user)(self.scope)
        # self.scope["user"] = await get_user(self.scope)
        if "user" not in self.scope or self.scope["user"] is None:
            self.scope["user"] = await get_user(self.scope)

        
        if self.scope["user"] is None or isinstance(self.scope["user"], AnonymousUser):
            await self.close()  # Close connection if user is not authenticated
            return
##########################################################################################

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        print(f" WebSocket Connected: {self.room_group_name}")

    async def disconnect(self, close_code):
        """Handle user disconnecting."""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print(f" WebSocket Disconnected: {self.room_group_name}")


    async def receive(self, text_data):
        """Handle incoming messages including files and save to database."""
        data = json.loads(text_data)
        sender = self.scope["user"]
        message = data.get("message", None)
        file_url = data.get("file_url", None)

        chatroom = await sync_to_async(ChatRoom.objects.get)(event__id=self.event_id)
        message_obj = await sync_to_async(Message.objects.create)(
            chatroom=chatroom, sender=sender, content=message, file=file_url
        )

        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message",
                "message": message_obj.content if message_obj.content else "",
                "file_url": message_obj.file.url if message_obj.file else "",
                "sender": sender.username,
                "timestamp": str(message_obj.timestamp),
            }
        )
        print(f"Broadcasted Message: {message_obj.content}")

    async def chat_message(self, event):
        """Send messages and files to connected clients instantly."""
        message = event.get("message", "")
        file_url = event.get("file_url", "")
        sender = event["sender"]
        timestamp = event["timestamp"]

        await self.send(text_data=json.dumps({
            "type": "chat_message",
            "message": message if message else "",  # Ensure it's not None
            "file_url": file_url if file_url else "",
            "sender": sender,
            "timestamp": timestamp
        }))


