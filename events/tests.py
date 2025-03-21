from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model
from events.models import Event, VolunteerEvent, VolunteerParticipation, FeedbackForm, FeedbackResponse

User = get_user_model()

class EventTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.org = User.objects.create_user(username="org1", password="pass123", user_type="organisation")
        cls.vol = User.objects.create_user(username="vol1", password="pass123", user_type="volunteer")

        cls.event = Event.objects.create(
            organisation=cls.org,
            name="Cleanup Drive",
            description="Beach cleanup",
            date=now() + timedelta(days=2),
            location="Beach",
            start_time="09:00",
            end_time="12:00",
            volunteers_needed=5,
            roles_responsibilities="Pick up trash",
            category="social development"
        )

    def test_organisation_dashboard_view(self):
        self.client.login(username="org1", password="pass123")
        response = self.client.get(reverse("events:organisation_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cleanup Drive")

    def test_volunteer_dashboard_view(self):
        self.client.login(username="vol1", password="pass123")
        response = self.client.get(reverse("events:volunteer_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cleanup Drive")

    def test_create_edit_delete_event(self):
        self.client.login(username="org1", password="pass123")

        # Create
        response = self.client.post(reverse("events:create_event"), {
            "name": "Tree Planting",
            "description": "Park beautification",
            "date": (now() + timedelta(days=3)).strftime('%Y-%m-%dT%H:%M'),
            "start_time": "10:00",
            "end_time": "13:00",
            "location": "Park",
            "volunteers_needed": 10,
            "roles_responsibilities": "Plant trees",
            "category": "social development"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Event.objects.filter(name="Tree Planting").exists())

        event = Event.objects.get(name="Tree Planting")

        # Edit
        response = self.client.post(reverse("events:edit_event", args=[event.id]), {
            "name": "Tree Planting Day",
            "description": "Updated",
            "date": event.date.strftime('%Y-%m-%dT%H:%M'),
            "start_time": "10:00",
            "end_time": "13:00",
            "location": "Park",
            "volunteers_needed": 10,
            "roles_responsibilities": "Plant trees",
            "category": "social development"
        })
        self.assertRedirects(response, reverse("events:organisation_events"))
        self.assertTrue(Event.objects.filter(name="Tree Planting Day").exists())

        # Delete
        response = self.client.post(reverse("events:delete_event", args=[event.id]))
        self.assertRedirects(response, reverse("events:organisation_events"))
        self.assertFalse(Event.objects.filter(id=event.id).exists())

    def test_register_and_cancel_event(self):
        self.client.login(username="vol1", password="pass123")

        # Register
        response = self.client.get(reverse("events:register_for_event", args=[self.event.id]))
        self.assertRedirects(response, reverse("events:volunteer_dashboard"))
        self.assertTrue(VolunteerEvent.objects.filter(event=self.event, volunteer=self.vol).exists())

        # Cancel
        response = self.client.get(reverse("events:cancel_registration", args=[self.event.id]))
        self.assertRedirects(response, reverse("events:volunteer_events"))
        self.assertFalse(VolunteerEvent.objects.filter(event=self.event, volunteer=self.vol).exists())

    def test_complete_event_logs_hours(self):
        self.client.login(username="org1", password="pass123")
        VolunteerEvent.objects.create(event=self.event, volunteer=self.vol, status="Registered")

        response = self.client.get(reverse("events:complete_event", args=[self.event.id]))
        self.assertRedirects(response, reverse("events:organisation_events"))
        self.assertTrue(VolunteerParticipation.objects.filter(event=self.event, volunteer=self.vol).exists())

    def test_feedback_flow(self):
        self.client.login(username="org1", password="pass123")
        # Create Feedback Form
        response = self.client.post(reverse("events:create_feedback_form", args=[self.event.id]), {
            "question_1": "Q1",
            "question_2": "Q2",
            "question_3": "Q3",
            "question_4": "Q4",
            "question_5": "Q5"
        })
        self.assertRedirects(response, reverse("events:organisation_dashboard"))
        form = FeedbackForm.objects.get(event=self.event)

        # Publish
        response = self.client.get(reverse("events:publish_feedback", args=[self.event.id]))
        self.assertRedirects(response, reverse("events:organisation_dashboard"))
        form.refresh_from_db()
        self.assertTrue(form.published)

        # Volunteer fills feedback
        self.client.logout()
        self.client.login(username="vol1", password="pass123")
        VolunteerEvent.objects.create(event=self.event, volunteer=self.vol, status="Registered")

        response = self.client.post(reverse("events:complete_feedback", args=[self.event.id]), {
            "rating_1": 5,
            "rating_2": 4,
            "rating_3": 4,
            "rating_4": 5,
            "rating_5": 5,
            "notify_future_events": True,
            "allow_follow_up_contact": False
        })
        self.assertRedirects(response, reverse("events:volunteer_events"))
        self.assertTrue(FeedbackResponse.objects.filter(feedback_form=form, volunteer=self.vol).exists())
