from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError


User = get_user_model()

class AccountsTests(TestCase):
    def setUp(self):
        # Setup test users before each test
        self.volunteer = User.objects.create_user(
            username="volunteer1",
            password="testpass123",
            user_type="volunteer"
        )
        self.organization = User.objects.create_user(
            username="org1",
            password="testpass123",
            user_type="organisation"
        )

    ##  Volunteer Registration Tests
    def test_volunteer_registration(self):
        # Test if a volunteer can register successfully
        response = self.client.post(reverse("accounts:register_volunteer"), {
            "username": "newvolunteer",
            "email": "newvolunteer@example.com",
            "password1": "securepassword123",
            "password2": "securepassword123",
            "full_name": "Alice Doe",
            "contact_number": "98765432",
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        self.assertTrue(User.objects.filter(username="newvolunteer").exists())

    def test_invalid_volunteer_registration(self):
        # Ensure volunteer registration fails with mismatched passwords
        response = self.client.post(reverse("accounts:register_volunteer"), {
            "username": "volunteerX",
            "email": "volunteerX@example.com",
            "password1": "securepassword123",
            "password2": "wrongpassword",
            "full_name": "Alice Doe",
            "contact_number": "98765432",
        })
        self.assertEqual(response.status_code, 200)  # Should not redirect
        self.assertFalse(User.objects.filter(username="volunteerX").exists())

    ##  Organisation Registration Tests
    def test_organisation_registration(self):
        # Test if an organisation can register successfully
        response = self.client.post(reverse("accounts:register_organisation"), {
            "username": "neworg",
            "email": "neworg@example.com",
            "password1": "securepassword123",
            "password2": "securepassword123",
            "organisation_name": "Helping Hands",
            "personnel_name": "John Doe",
            "contact_number": "12345678",
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        self.assertTrue(User.objects.filter(username="neworg").exists())

    ##  Login Tests
    def test_login_volunteer(self):
        # Test if a volunteer can log in
        response = self.client.post(reverse("accounts:login"), {
            "username": "volunteer1",
            "password": "testpass123"
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to dashboard

    def test_login_organisation(self):
        # Test if an organization can log in
        response = self.client.post(reverse("accounts:login"), {
            "username": "org1",
            "password": "testpass123"
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to dashboard

    def test_invalid_login(self):
        # Ensure invalid credentials prevent login
        response = self.client.post(reverse("accounts:login"), {
            "username": "wronguser",
            "password": "wrongpass"
        })
        self.assertEqual(response.status_code, 200)  # Should stay on login page
        self.assertContains(response, "Invalid username or password")

    ##  Logout Test
    def test_logout(self):
        # Ensure users can log out
        self.client.login(username="volunteer1", password="testpass123")
        response = self.client.post(reverse("accounts:logout"))
        self.assertEqual(response.status_code, 302)  # Should redirect after logout

    ##  Dashboard Redirection Tests
    def test_dashboard_redirection_volunteer(self):
        # est if a volunteer is redirected to the correct dashboard
        self.client.login(username="volunteer1", password="testpass123")
        response = self.client.get(reverse("accounts:login_redirect"))
        self.assertRedirects(response, reverse("events:volunteer_dashboard"))

    def test_dashboard_redirection_organisation(self):
        # Test if an organization is redirected to the correct dashboard
        self.client.login(username="org1", password="testpass123")
        response = self.client.get(reverse("accounts:login_redirect"))
        self.assertRedirects(response, reverse("events:organisation_dashboard"))

    ##  Unauthorized Access Tests
    def test_unauthorised_access_to_dashboard(self):
        # Ensure unauthenticated users cannot access the dashboard
        response = self.client.get(reverse("accounts:login_redirect"))
        self.assertRedirects(response, reverse("accounts:login") + "?next=" + reverse("accounts:login_redirect"))

    def test_profile_update(self):
        # Ensure profile updates correctly
        self.client.login(username="volunteer1", password="testpass123")
        response = self.client.post(reverse("accounts:profile"), {
            "full_name": "Updated Name",
            "email": "updated@example.com",  # Expecting email to change
            "contact_number": "99999999"
        }, follow=True)

        self.volunteer.refresh_from_db()
        self.assertEqual(self.volunteer.full_name, "Updated Name")
        self.assertEqual(self.volunteer.email, "updated@example.com")  # Now checking if email updates
        self.assertEqual(self.volunteer.contact_number, "99999999")

    def test_profile_update_with_image(self):
        # Ensure profile updates with an image upload
        self.client.login(username="volunteer1", password="testpass123")

        image = SimpleUploadedFile(
            "profile.jpg",
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04\x01\x00\x00\x00\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4C\x01\x00\x3B",
            content_type="image/jpeg"
        )

        response = self.client.post(reverse("accounts:profile"), {
            "profile_picture": image,
        }, follow=True)

        self.volunteer.refresh_from_db()
        self.assertIsNotNone(self.volunteer.profile_picture)

    ##  User Type Enforcement Tests
    def test_invalid_user_type_creation(self):
        # Ensure user cannot be created with an invalid user type
        with self.assertRaises(ValidationError):  # Expecting ValidationError, not ValueError
            user = User(username="invaliduser", password="password123", user_type="invalid_type")
            user.full_clean()  # This manually triggers validation
            user.save()

            
    # ##  Password Reset Test
    # def test_password_reset(self):
    #     """Ensure users can request a password reset"""
    #     response = self.client.post(reverse("accounts:password_reset"), {
    #         "email": self.volunteer.email
    #     })
    #     self.assertEqual(response.status_code, 302)  # Should redirect
