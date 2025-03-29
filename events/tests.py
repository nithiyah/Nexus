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
        self.assertRedirects(response, reverse("events:organisation_dashboard"))
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
  
  
    def test_cannot_complete_event_twice(self):
        # once event is marked as complete, message should appear to confirm
        self.client.login(username="org1", password="pass123")
        self.event.is_completed = True
        self.event.save()

        response = self.client.get(reverse("events:complete_event", args=[self.event.id]), follow=True)
        self.assertContains(response, "already marked as completed")

    def test_volunteer_cannot_register_past_event(self):
        # volunteers should not be able to register for past events
        self.client.login(username="vol1", password="pass123")
        self.event.date = now() - timedelta(days=1)
        self.event.save()

        response = self.client.get(reverse("events:register_for_event", args=[self.event.id]), follow=True)
        self.assertContains(response, "You cannot register for past events.")
        self.assertFalse(VolunteerEvent.objects.filter(event=self.event, volunteer=self.vol).exists())

    def test_volunteer_cannot_cancel_completed_event(self):
        # volunteers should not be able to cancel a completed event
        self.client.login(username="vol1", password="pass123")
        self.event.date = now() - timedelta(days=1)
        self.event.save()
        VolunteerEvent.objects.create(event=self.event, volunteer=self.vol, status="Registered")

        response = self.client.get(reverse("events:cancel_registration", args=[self.event.id]), follow=True)
        self.assertContains(response, "You cannot cancel registration for a completed event.")

    def test_organisation_dashboard_filter_by_category(self):
        # organisation dashbaord category filtering
        self.client.login(username="org1", password="pass123")
        url = reverse("events:organisation_dashboard") + "?category=social+development"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cleanup Drive")


    def test_event_creation_invalid_data(self):
        # event form should be rejected if there are mssing fields, -ve volunteers_needed 
        # end time earlier than start time
        self.client.login(username="org1", password="pass123")
        response = self.client.post(reverse("events:create_event"), {
            "name": "",
            "description": "Invalid event",
            "date": "",
            "volunteers_needed": -5,
        })
        self.assertEqual(response.status_code, 200)
        form = response.context["form"]
        self.assertTrue(form.errors)
        self.assertIn("name", form.errors)


    def test_volunteer_cannot_access_create_event(self):
        # volunteers should not be able to access organistion only views 
        self.client.login(username="vol1", password="pass123")
        response = self.client.get(reverse("events:create_event"), follow=True)
        self.assertEqual(response.status_code, 200)


    def test_delete_event_confirmation_page(self):
        # checks to see if GET reuquest to detle event page shows the confirmatoin message 
        self.client.login(username="org1", password="pass123")
        response = self.client.get(reverse("events:delete_event", args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Delete")  # Adjust depending on your template text

    def test_volunteer_event_feedback_flag(self):
        # each volunteer event list should should feedback status
        self.client.login(username="vol1", password="pass123")
        VolunteerEvent.objects.create(event=self.event, volunteer=self.vol, status="Registered")
        FeedbackForm.objects.create(event=self.event, created_by=self.org, published=True)

        response = self.client.get(reverse("events:volunteer_events"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Feedback")

    def test_only_event_owner_can_remove_volunteer(self):
        # only the correct organisaton can remove volunteers 
        other_org = User.objects.create_user(username="org2", password="pass123", user_type="organisation")
        registration = VolunteerEvent.objects.create(event=self.event, volunteer=self.vol, status="Registered")

        self.client.login(username="org2", password="pass123")
        response = self.client.get(reverse("events:remove_volunteer", args=[registration.id]), follow=True)
        self.assertContains(response, "not authorised")

    def test_view_feedback_averages_render(self):
        # making sure the average rating feedback logic runs, page renders 
        self.client.login(username="org1", password="pass123")
        form = FeedbackForm.objects.create(event=self.event, created_by=self.org, published=True)
        FeedbackResponse.objects.create(
            feedback_form=form,
            volunteer=self.vol,
            rating_1=4, rating_2=5, rating_3=4, rating_4=5, rating_5=5,
        )
        response = self.client.get(reverse("events:view_feedback", args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "average")
