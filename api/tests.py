from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from accounts.models import CustomUser
from events.models import Event
from announcements.models import Announcement, AnnouncementComment
from chat.models import ChatRoom, Message

class APITests(APITestCase):

    def setUp(self):
        """Setup test users, sample event, and chatroom"""
        self.organisation = CustomUser.objects.create_user(
            username="org1",
            password="testpass123",
            user_type="organisation",
            email="org1@example.com"
        )

        self.volunteer = CustomUser.objects.create_user(
            username="volunteer1",
            password="testpass123",
            user_type="volunteer",
            email="volunteer1@example.com"
        )

        self.announcement = Announcement.objects.create(
            organisation=self.organisation,
            title="Volunteer Meetup",
            content="We will have a meetup this weekend!"
        )

        # Create an Event before the ChatRoom
        self.event = Event.objects.create(
            organisation=self.organisation,
            name="Beach Cleanup",
            description="A volunteer event to clean the beach",
            date="2025-06-15",
            location="Sentosa Beach",
            volunteers_needed=20,
            roles_responsibilities="Cleaning and sorting out the recyclables",
            category="Environment"
        )

        # Create a ChatRoom linked to the Event
        self.chatroom = ChatRoom.objects.create(event=self.event)

            

    # Permissions & Authentication Tests
    def test_unauthenticated_user_cannot_create_event(self):
        data = {
            "organisation_id": self.organisation.id,
            "name": "Unauthorized Event",
            "description": "Should not be created",
            "date": "2025-07-10",
            "location": "Unauthorized",
            "volunteers_needed": 10,
            "roles_responsibilities": "Unauthorized roles",
            "category": "environment"
        }
        response = self.client.post(reverse("events-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_volunteer_cannot_create_event(self):
        self.client.force_authenticate(user=self.volunteer)
        data = {
            "organisation_id": self.organisation.id,
            "name": "Volunteer Created Event",
            "description": "Should be blocked",
            "date": "2025-07-10",
            "location": "Unauthorized",
            "volunteers_needed": 10,
            "roles_responsibilities": "Unauthorized roles",
            "category": "Test"
        }
        response = self.client.post(reverse("events-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthorized_event_delete(self):
        self.client.force_authenticate(user=self.volunteer)
        response = self.client.delete(reverse("events-detail", args=[self.event.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Announcements API Test
    def test_volunteer_cannot_create_announcement(self):
        """Test that volunteers cannot create announcements"""
        self.client.force_authenticate(user=self.volunteer)
        data = {"title": "Volunteer Announcement", "content": "Should not be allowed"}
        response = self.client.post(reverse("announcements-list"), data, format="json")
        print(f"Test Response: {response.data}")  # Debugging output
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_volunteer_cannot_access_chatroom_without_registration(self):
        self.client.force_authenticate(user=self.volunteer)
        response = self.client.get(reverse("chatrooms-detail", args=[self.chatroom.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Events API Tests
    def test_list_events(self):
        response = self.client.get(reverse("events-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_event(self):
        self.client.force_authenticate(user=self.organisation)
        data = {
            "organisation_id": self.organisation.id,
            "name": "Tree Planting",
            "description": "Planting trees in local parks",
            "date": "2025-07-10",
            "location": "East Coast Park",
            "volunteers_needed": 10,
            "roles_responsibilities": "Digging, planting",
            "category": "social development"
        }
        response = self.client.post(reverse("events-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_pagination_on_event_list(self):
        for i in range(15):
            Event.objects.create(
                organisation=self.organisation,
                name=f"Event {i}",
                description="Sample event",
                date="2025-07-10",
                location="Test Location",
                volunteers_needed=5,
                roles_responsibilities="Testing roles",
                category="Education"
            )
        response = self.client.get(reverse("events-list") + "?page=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertGreaterEqual(response.data["count"], 15)

    # Announcements API Tests
    def test_list_announcements(self):
        """Test retrieving a list of announcements"""
        response = self.client.get(reverse("announcements-list"))
        print(f"Test Response: {response.data}")  # Debugging output
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_create_announcement(self):
        self.client.force_authenticate(user=self.volunteer)
        data = {"title": "Volunteer Announcement", "content": "Should not be allowed"}
        response = self.client.post(reverse("announcements-list"), data, format="json")
        print(f"Test Response: {response.data}")  # Debugging output
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    # Announcement Comments API Test

    def test_add_comment_to_announcement(self):
        """Test that a volunteer can add a comment to an announcement"""
        self.client.force_authenticate(user=self.volunteer)
        data = {"announcement": self.announcement.id, "comment": "Looking forward to it!"}
        response = self.client.post(reverse("announcement-comments-list"), data, format="json")
        print(f"Test Response: {response.data}")  # Debugging output
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)




    # Chat API Tests
    def test_list_chatrooms(self):
        self.client.force_authenticate(user=self.volunteer)
        response = self.client.get(reverse("chatrooms-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


    def test_send_message_in_chatroom(self):
        """Test that an organisation can send a message in a chatroom"""
        self.client.force_authenticate(user=self.organisation)
        data = {"chatroom": self.chatroom.id, "content": "Hello volunteers!"}
        response = self.client.post(reverse("chat-messages-list"), data, format="json")
        print(f"Test Response: {response.data}")  # Debugging output
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
