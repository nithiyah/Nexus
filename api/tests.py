from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from accounts.models import CustomUser
from events.models import Event
from announcements.models import Announcement

class APITests(APITestCase):

    def setUp(self):
        self.organisation = CustomUser.objects.create_user(
            username="org1", password="testpass123", user_type="organisation", email="org1@example.com"
        )
        self.volunteer = CustomUser.objects.create_user(
            username="volunteer1", password="testpass123", user_type="volunteer", email="volunteer1@example.com"
        )
        self.announcement = Announcement.objects.create(
            organisation=self.organisation, title="Welcome", content="Event incoming!"
        )
        self.event = Event.objects.create(
            organisation=self.organisation,
            name="Beach Cleanup",
            description="Clean the beach",
            date="2025-06-15",
            location="Sentosa",
            volunteers_needed=10,
            roles_responsibilities="Clean up & sort recyclables",
            category="social development"
        )

    def test_create_event_as_organisation(self):
        self.client.force_authenticate(user=self.organisation)
        data = {
            "name": "New Event",
            "description": "Details",
            "date": "2025-12-01",
            "location": "Test Park",
            "volunteers_needed": 5,
            "roles_responsibilities": "Help out",
            "category": "social development"  # Use a valid category
        }
        response = self.client.post(reverse("events-list"), data)
        print("Event POST response:", response.status_code, response.data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_volunteer_cannot_create_event(self):
        self.client.force_authenticate(user=self.volunteer)
        data = {
            "name": "Should Not Work",
            "description": "Blocked",
            "date": "2025-12-01",
            "location": "Nowhere",
            "volunteers_needed": 5,
            "roles_responsibilities": "None",
            "category": "social development"
        }
        response = self.client.post(reverse("events-list"), data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_post_comment(self):
        self.client.force_authenticate(user=self.volunteer)
        data = {"announcement": self.announcement.id, "comment": "Looking forward!"}
        response = self.client.post(reverse("announcement-comments-list"), data)
        print("Comment POST response:", response.status_code, response.data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_like_announcement(self):
        self.client.force_authenticate(user=self.volunteer)
        data = {"announcement": self.announcement.id}
        response = self.client.post(reverse("announcement-likes-list"), data)
        print("Like POST response:", response.status_code, response.data)
        assert response.status_code == status.HTTP_201_CREATED