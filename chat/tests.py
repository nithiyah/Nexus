import json
from django.test import TestCase
from channels.db import database_sync_to_async

from django.contrib.auth import get_user_model
from django.urls import reverse
from channels.testing import WebsocketCommunicator
from channels.routing import URLRouter
from chat.routing import websocket_urlpatterns
from chat.models import ChatRoom, Message
from events.models import Event
from asgiref.sync import sync_to_async
from chat.consumers import ChatConsumer

User = get_user_model()


class ChatTests(TestCase):
    """Tests for chat room API & WebSocket functionality."""

    def setUp(self):
        """Setup test data."""
        # Create test users
        self.organisation = User.objects.create_user(
            username="org1",
            password="testpass123",
            user_type="organisation"
        )
        self.volunteer = User.objects.create_user(
            username="volunteer1",
            password="testpass123",
            user_type="volunteer"
        )
        self.other_user = User.objects.create_user(
            username="randomuser",
            password="testpass123",
            user_type="volunteer"
        )

        # Create event
        self.event = Event.objects.create(
            organisation=self.organisation,
            name="Community Clean-Up",
            description="Cleaning the park",
            date="2025-07-10",
            location="Community Park",
            volunteers_needed=10,
            roles_responsibilities="Sweeping, collecting trash",
            category="environment"
        )

        # Create chat room associated with the event
        self.chatroom = ChatRoom.objects.create(event=self.event)

        # Authenticate volunteer
        self.client.login(username="volunteer1", password="testpass123")

    ##  1. API TESTS ##

    def test_chatroom_creation(self):
        """Ensure a chat room is automatically created for an event."""
        self.assertIsNotNone(self.chatroom)
        self.assertEqual(self.chatroom.event, self.event)

    def test_join_chatroom(self):
        """Test if a volunteer can join a chatroom."""
        response = self.client.get(reverse("chat:chat_room", args=[self.event.id]))
        self.assertEqual(response.status_code, 200)  # Should render chat room page

    def test_send_message(self):
        """Test sending a message in the chat room."""
        data = {"content": "Hello, this is a test message!"}
        response = self.client.post(reverse("chat:send_message", args=[self.event.id]), json.dumps(data), content_type="application/json")
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Message.objects.filter(content="Hello, this is a test message!").exists())

    def test_fetch_messages(self):
        """Test retrieving messages from a chat room."""
        # Create a message
        Message.objects.create(chatroom=self.chatroom, sender=self.volunteer, content="Test message")
        
        response = self.client.get(reverse("chat:chat_room", args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test message")

    def test_unauthorized_user_cannot_join_chat(self):
        """Test that unauthorized users cannot join chat rooms."""
        self.client.logout()  # Ensure the user is not logged in
        response = self.client.get(reverse("chat:chat_room", args=[self.event.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    ##  2. WEBSOCKET TESTS ##

    async def test_websocket_connection(self):
        """Ensure users can establish a WebSocket connection."""
        communicator = WebsocketCommunicator(
            URLRouter(websocket_urlpatterns),
            f"/ws/chat/{self.event.id}/"
        )
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    async def test_send_message_websocket(self):
        """Test sending and receiving messages through WebSocket."""
        
        # Authenticate user
        self.volunteer = await database_sync_to_async(User.objects.get)(username="volunteer1")

        communicator = WebsocketCommunicator(
            ChatConsumer.as_asgi(),
            f"/ws/chat/{self.event.id}/"
        )
        
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Send message
        message_data = {"message": "Hello WebSocket!"}
        await communicator.send_json_to(message_data)

        # Receive message
        response = await communicator.receive_json_from()
        self.assertEqual(response["message"], "Hello WebSocket!")

        await communicator.disconnect()

    async def test_websocket_broadcast(self):
        """Ensure a message sent by one user is received by another user in the chat."""
        # First user connects
        communicator1 = WebsocketCommunicator(
            URLRouter(websocket_urlpatterns),
            f"/ws/chat/{self.event.id}/"
        )
        connected, _ = await communicator1.connect()
        self.assertTrue(connected)

        # Second user connects
        communicator2 = WebsocketCommunicator(
            URLRouter(websocket_urlpatterns),
            f"/ws/chat/{self.event.id}/"
        )
        connected, _ = await communicator2.connect()
        self.assertTrue(connected)

        # Send message from first user
        message_data = {"message": "Hello everyone!"}
        await communicator1.send_json_to(message_data)

        # Receive message from second user
        response = await communicator2.receive_json_from()
        self.assertEqual(response["message"], "Hello everyone!")

        await communicator1.disconnect()
        await communicator2.disconnect()

    async def test_unauthorized_websocket_access(self):
        """Test that unauthorized users cannot connect to a chat WebSocket."""
        communicator = WebsocketCommunicator(
            URLRouter(websocket_urlpatterns),
            f"/ws/chat/9999/"  # Invalid event ID
        )
        connected, _ = await communicator.connect()
        self.assertFalse(connected)
