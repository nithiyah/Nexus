from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from announcements.models import Announcement, AnnouncementComment, AnnouncementLike
from events.models import Event, VolunteerEvent

User = get_user_model()

class AnnouncementTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.org = User.objects.create_user(username="org1", password="testpass123", user_type="organisation")
        cls.volunteer = User.objects.create_user(username="vol1", password="testpass123", user_type="volunteer")
        cls.event = Event.objects.create(
            organisation=cls.org,
            name="Test Event",
            description="Desc",
            date="2025-01-01",
            location="Loc",
            volunteers_needed=5,
            roles_responsibilities="Help",
            category="environment"
        )
        VolunteerEvent.objects.create(event=cls.event, volunteer=cls.volunteer)
        cls.announcement = Announcement.objects.create(
            organisation=cls.org,
            event=cls.event,
            title="Test Announcement",
            content="Important info."
        )

    def test_create_announcement_as_org(self):
        self.client.login(username="org1", password="testpass123")
        response = self.client.post(reverse("announcements:create_announcement"), {
            "title": "New Post",
            "content": "Details",
            "event": self.event.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Announcement.objects.filter(title="New Post").exists())

    def test_create_announcement_as_volunteer_forbidden(self):
        self.client.login(username="vol1", password="testpass123")
        response = self.client.post(reverse("announcements:create_announcement"), {
            "title": "Blocked",
            "content": "Should not happen",
            "event": self.event.id
        })
        self.assertRedirects(response, reverse("announcements:announcement_list"))
        self.assertFalse(Announcement.objects.filter(title="Blocked").exists())

    def test_announcement_detail_and_comment(self):
        self.client.login(username="vol1", password="testpass123")
        detail_url = reverse("announcements:announcement_detail", args=[self.announcement.id])
        comment_url = reverse("announcements:add_comment", args=[self.announcement.id])

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)

        comment_response = self.client.post(comment_url, {"comment": "Nice one!"})
        self.assertRedirects(comment_response, detail_url)
        self.assertTrue(AnnouncementComment.objects.filter(comment__icontains="Nice one!").exists())

    def test_like_and_unlike_announcement(self):
        self.client.login(username="vol1", password="testpass123")
        like_url = reverse("announcements:like_announcement", args=[self.announcement.id])

        # Like it
        response1 = self.client.post(like_url, follow=True)
        self.assertTrue(AnnouncementLike.objects.filter(user=self.volunteer, announcement=self.announcement).exists())

        # Unlike it
        response2 = self.client.post(like_url, follow=True)
        self.assertFalse(AnnouncementLike.objects.filter(user=self.volunteer, announcement=self.announcement).exists())

    def test_announcement_list_view_filter_all(self):
        self.client.login(username="vol1", password="testpass123")
        response = self.client.get(reverse("announcements:announcement_list") + "?filter=all")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.announcement.content)
        self.assertContains(response, "All Announcements")

    def test_announcement_list_view_filter_my(self):
        self.client.login(username="vol1", password="testpass123")
        response = self.client.get(reverse("announcements:announcement_list") + "?filter=my")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.announcement.content)
        self.assertContains(response, "My Announcements")

        self.client.logout()
        self.client.login(username="org1", password="testpass123")
        response2 = self.client.get(reverse("announcements:announcement_list") + "?filter=my")
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, self.announcement.content)

    def test_breadcrumb_in_detail_view(self):
        self.client.login(username="vol1", password="testpass123")
        response = self.client.get(reverse("announcements:announcement_detail", args=[self.announcement.id]))
        self.assertContains(response, "breadcrumb")
        self.assertContains(response, "Announcements")
        self.assertContains(response, "View")

    def test_breadcrumb_in_create_view(self):
        self.client.login(username="org1", password="testpass123")
        response = self.client.get(reverse("announcements:create_announcement"))
        self.assertContains(response, "breadcrumb")
        self.assertContains(response, "Announcements")
        self.assertContains(response, "Create")