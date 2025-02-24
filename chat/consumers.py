import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, Message
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Accept the WebSocket connection."""
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Disconnect the WebSocket connection."""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Handle incoming messages."""
        data = json.loads(text_data)
        sender = self.scope["user"]
        message = data["message"]

        # Save message to database
        chatroom = await self.get_chatroom(self.room_id)
        message_obj = Message.objects.create(chatroom=chatroom, sender=sender, content=message)

        # Send message to the WebSocket group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message",
                "message": message_obj.content,
                "sender": sender.username,
                "timestamp": str(message_obj.timestamp),
            }
        )

    async def chat_message(self, event):
        """Send the received message to WebSocket clients."""
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
            "timestamp": event["timestamp"],
        }))

    @staticmethod
    async def get_chatroom(room_id):
        """Retrieve the chatroom instance."""
        return await ChatRoom.objects.get(id=room_id)
