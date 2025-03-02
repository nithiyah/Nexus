from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from accounts.models import CustomUser
from events.models import Event

class APITests(APITestCase):
    def setUp(self):
        """Setup test users and sample data"""
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

        self.event = Event.objects.create(
            organisation=self.organisation,
            name="Beach Cleanup",
            description="A volunteer event to clean the beach",
            date="2025-06-15",
            location="Sentosa Beach",
            volunteers_needed=20,
            roles_responsibilities="Cleaning, sorting recyclables",
            category="Environment"
        )
        self.admin = CustomUser.objects.create_superuser(
        username="admin",
        password="adminpass123",
        email="admin@example.com",
    )


    ##  TESTING EVENT API ##
    def test_list_events(self):
        """Test retrieving a list of events"""
        response = self.client.get(reverse("events-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_event(self):
        """Test retrieving a specific event"""
        response = self.client.get(reverse("events-detail", args=[self.event.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Beach Cleanup")

    def test_create_event(self):
        """Test event creation (allowed for organisations only)"""
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
        self.client.force_authenticate(user=self.organisation)  # Ensure authentication
        response = self.client.post(reverse("events-list"), data, format="json")
        print("Response Data:", response.data)  # Debugging
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_update_event(self):
        """Test updating an event (only by the organisation that created it)"""
        self.client.force_authenticate(user=self.organisation)
        data = {
            "name": "Updated Beach Cleanup",
            "description": "Updated description",
        }
        response = self.client.patch(reverse("events-detail", args=[self.event.id]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Beach Cleanup")

    def test_delete_event(self):
        """Test deleting an event (only by the organisation that created it)"""
        self.client.force_authenticate(user=self.organisation)
        response = self.client.delete(reverse("events-detail", args=[self.event.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Event.objects.filter(id=self.event.id).exists())

    ##  TESTING ORGANIZATION API ##
    def test_list_organisations(self):
        """Test retrieving all organisations"""
        response = self.client.get(reverse("organisations-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        
    def test_create_organisation(self):
        """Test creating a new organisation user"""
        self.client.force_authenticate(user=self.admin)  #Authenticate as admin

        data = {
            "username": "org2",
            "password": "securepass123",
            "email": "org2@example.com",
            "user_type": "organisation"
        }
        response = self.client.post(reverse("organisations-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "org2")


    ##  TESTING VOLUNTEER API ##
    def test_list_volunteers(self):
        """Test retrieving all volunteers"""
        response = self.client.get(reverse("volunteers-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_volunteer(self):
        """Test creating a new volunteer user"""
        self.client.force_authenticate(user=self.admin)  #Authenticate as admin

        data = {
            "username": "volunteer2",
            "password": "securepass123",
            "email": "volunteer2@example.com",
            "user_type": "volunteer"
        }
        response = self.client.post(reverse("volunteers-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "volunteer2")


    ##  PERMISSIONS & AUTHENTICATION TESTS ##
    def test_unauthorised_create_event(self):
        """Test that unauthenticated users cannot create events"""
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
        print("Response Data:", response.data)  # Debugging
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Change to 403


    def test_volunteer_cannot_create_event(self):
        """Test that volunteers cannot create events"""
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
        """Test that volunteers cannot delete events"""
        self.client.force_authenticate(user=self.volunteer)
        response = self.client.delete(reverse("events-detail", args=[self.event.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

