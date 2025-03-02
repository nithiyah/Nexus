import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import ChatRoom, Message

from datetime import datetime, timedelta

# async def receive(self, text_data):
#     """Handle incoming messages and save to database."""
#     data = json.loads(text_data)
#     sender = self.scope["user"]
#     message = data["message"]

#     # Get the current time in Singapore Time
#     singapore_time = (datetime.now() +  timedelta(hours=8)).strftime("%H:%M")  # Format to HH:MM only

#     chatroom = await sync_to_async(ChatRoom.objects.get)(event__id=self.event_id)
#     message_obj = await sync_to_async(Message.objects.create)(
#         chatroom=chatroom, sender=sender, content=message
#     )

#     # Send correctly formatted timestamp without breaking updates
#     await self.channel_layer.group_send(
#         self.room_group_name, {
#             "type": "chat_message",
#             "message": message_obj.content,
#             "sender": sender.username,
#             "timestamp": singapore_time,  # Now using correct SG time
#         }
#     )
from django.utils.timezone import now

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

async def receive(self, text_data):
    """Handle incoming messages and save to database."""
    data = json.loads(text_data)
    sender = self.scope["user"]
    message = data["message"]

    #  Get the current time in Singapore Time
    singapore_time = datetime.now().strftime("%H:%M")  # Format to HH:MM only

    chatroom = await sync_to_async(ChatRoom.objects.get)(event__id=self.event_id)
    message_obj = await sync_to_async(Message.objects.create)(
        chatroom=chatroom, sender=sender, content=message
    )

    #  Send correctly formatted timestamp without breaking updates
    await self.channel_layer.group_send(
        self.room_group_name, {
            "type": "chat_message",
            "message": message_obj.content,
            "sender": sender.username,
            "timestamp": singapore_time,  #Now using correct SG time
        }
    )

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Accept WebSocket connection."""
        self.event_id = self.scope["url_route"]["kwargs"]["event_id"]
        self.room_group_name = f"chat_{self.event_id}"  # Ensure it matches `routing.py`

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        print(f" WebSocket Connected: {self.room_group_name}")

    async def disconnect(self, close_code):
        """Handle user disconnecting."""
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print(f" WebSocket Disconnected: {self.room_group_name}")

    async def receive(self, text_data):
        """Handle incoming messages and save to database."""
        data = json.loads(text_data)
        sender = self.scope["user"]
        message = data["message"]

        print(f" Received Message: {message} from {sender}")

        # Fetch the correct chatroom
        chatroom = await sync_to_async(ChatRoom.objects.get)(event__id=self.event_id)
        message_obj = await sync_to_async(Message.objects.create)(
            chatroom=chatroom, sender=sender, content=message
        )

        # Send message to ALL clients in the chat room (real-time update)
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat.message",
                "message": message_obj.content,
                "sender": sender.username,
                "timestamp": str(message_obj.timestamp),
            }
        )
        print(f"Broadcasted Message: {message_obj.content}")

    async def chat_message(self, event):
        """ Send messages to connected clients instantly."""
        print(f" Sending Message to Clients: {event['message']}")
        await self.send(text_data=json.dumps({
            "type": "chat_message",  # Ensure frontend can detect this type
            "message": event["message"],
            "sender": event["sender"],
            "timestamp": event["timestamp"],
        }))


    # trying to get the correct time
    # async def chat_message(self, event):
    #     """Send messages to connected clients with correct timezone."""
    #     singapore_time = convert_to_singapore_time(event["timestamp"])  # Convert UTC to SG time


        
    # #     await self.send(text_data=json.dumps({
    # #     "type": "chat_message",  # Ensure frontend can detect this type
    #     await self.send(text_data=json.dumps({
    #         "message": event["message"],
    #         "sender": event["sender"],
    #         "timestamp": singapore_time,  # Now in Singapore Time
    # }))

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import ChatRoom, Message
# from django.contrib.auth import get_user_model
# from asgiref.sync import sync_to_async

# User = get_user_model()

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         """Accept the WebSocket connection."""  
#         # self.event_id = self.scope["url_route"]["kwargs"]["event_id"]
#         # # self.room_id = self.scope["url_route"]["kwargs"]["event_id"]  # Match routing.py

#         # self.room_group_name = f"chat_{self.event_id}"

#         self.event_id = self.scope["url_route"]["kwargs"]["event_id"]
#         self.room_group_name = f"chat_{self.event_id}"  # Match routing.py

#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         """Handle user disconnecting."""
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     async def receive(self, text_data):
#         """Handle incoming messages."""
#         data = json.loads(text_data)
#         sender = self.scope["user"]
#         message = data["message"]

#         # Save message to database asynchronously
#         # chatroom = await sync_to_async(ChatRoom.objects.get)(id=self.event_id)
#         chatroom = await sync_to_async(ChatRoom.objects.get)(event__id=self.event_id)

#         message_obj = await sync_to_async(Message.objects.create)(chatroom=chatroom, sender=sender, content=message)

#         # Send message to the WebSocket group
#         await self.channel_layer.group_send(
#             self.room_group_name, {
#                 "type": "chat_message",
#                 "message": message_obj.content,
#                 "sender": sender.username,
#                 "timestamp": str(message_obj.timestamp),
#             }
#         )

#     async def chat_message(self, event):
#         """Send messages to connected clients."""
#         await self.send(text_data=json.dumps({
#             "message": event["message"],
#             "sender": event["sender"],
#             "timestamp": event["timestamp"],
#         }))

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import sync_to_async
# from .models import ChatRoom, Message

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         """Accept WebSocket connection."""
#         self.event_id = self.scope["url_route"]["kwargs"]["event_id"]
#         self.room_group_name = f"chat_{self.event_id}"  # Ensure it matches `routing.py`

#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         """Handle user disconnecting."""
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     async def receive(self, text_data):
#         """Handle incoming messages and save to database."""
#         data = json.loads(text_data)
#         sender = self.scope["user"]
#         message = data["message"]

#         # Fetch the correct chatroom
#         chatroom = await sync_to_async(ChatRoom.objects.get)(event__id=self.event_id)
#         message_obj = await sync_to_async(Message.objects.create)(
#             chatroom=chatroom, sender=sender, content=message
#         )

#         # Send message to WebSocket group
#         await self.channel_layer.group_send(
#             self.room_group_name, {
#                 "type": "chat_message",
#                 "message": message_obj.content,
#                 "sender": sender.username,
#                 "timestamp": str(message_obj.timestamp),
#             }
#         )

#     async def chat_message(self, event):
#         """Send messages to connected clients."""
#         await self.send(text_data=json.dumps({
#             "message": event["message"],
#             "sender": event["sender"],
#             "timestamp": event["timestamp"],
#         }))
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import sync_to_async
# from .models import ChatRoom, Message

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         """Accept WebSocket connection."""
#         self.event_id = self.scope["url_route"]["kwargs"]["event_id"]
#         self.room_group_name = f"chat_{self.event_id}"  # Ensure it matches `routing.py`

#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#         await self.accept()
#         print(f" WebSocket Connected: {self.room_group_name}")

#     async def disconnect(self, close_code):
#         """Handle user disconnecting."""
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
#         print(f" WebSocket Disconnected: {self.room_group_name}")

#     async def receive(self, text_data):
#         """Handle incoming messages and save to database."""
#         data = json.loads(text_data)
#         sender = self.scope["user"]
#         message = data["message"]

#         print(f" Received Message: {message} from {sender}")

#         # Fetch the correct chatroom
#         chatroom = await sync_to_async(ChatRoom.objects.get)(event__id=self.event_id)
#         message_obj = await sync_to_async(Message.objects.create)(
#             chatroom=chatroom, sender=sender, content=message
#         )

#         #  Send message to ALL clients in the chat room (real-time update)
#         await self.channel_layer.group_send(
#             self.room_group_name, {
#                 "type": "chat_message",
#                 "message": message_obj.content,
#                 "sender": sender.username,
#                 "timestamp": str(message_obj.timestamp),
#             }
#         )
#         print(f"Broadcasted Message: {message_obj.content}")

#     async def chat_message(self, event):
#         """Send messages to connected clients instantly."""
#         print(f"📨 Sending Message to Clients: {event['message']}")
#         await self.send(text_data=json.dumps({
#             "message": event["message"],
#             "sender": event["sender"],
#             "timestamp": event["timestamp"],
#         }))
