from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class AccountsTests(TestCase):
    def setUp(self):
        """Setup test users before each test"""
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

    def test_volunteer_registration(self):
        """Test if a volunteer can register successfully"""
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

    def test_organisation_registration(self):
        """Test if an organisation can register successfully"""
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


    def test_login_volunteer(self):
        """Test if a volunteer can log in"""
        response = self.client.post(reverse("accounts:login"), {
            "username": "volunteer1",
            "password": "testpass123"
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to dashboard

    def test_login_organisation(self):
        """Test if an organization can log in"""
        response = self.client.post(reverse("accounts:login"), {
            "username": "org1",
            "password": "testpass123"
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to dashboard

    def test_dashboard_redirection_volunteer(self):
        """Test if a volunteer is redirected to the correct dashboard"""
        self.client.login(username="volunteer1", password="testpass123")
        response = self.client.get(reverse("accounts:login_redirect"))
        self.assertRedirects(response, reverse("events:volunteer_dashboard"))

    def test_dashboard_redirection_organisation(self):
        """Test if an organization is redirected to the correct dashboard"""
        self.client.login(username="org1", password="testpass123")
        response = self.client.get(reverse("accounts:login_redirect"))
        self.assertRedirects(response, reverse("events:organisation_dashboard"))

    def test_profile_update(self):
        """Test if a user can update their profile"""
        self.client.login(username="volunteer1", password="testpass123")
        response = self.client.post(reverse("accounts:profile"), {
            "username": "updatedvolunteer",
            "email": "updated@example.com",
            "contact_number": "98765432"
        }, follow=True)

        self.volunteer.refresh_from_db()  # Reload user from DB
        print("Updated Username:", self.volunteer.username)  # Debugging output
        self.assertEqual(self.volunteer.email, "updated@example.com")  # Ensure email changed

    from django.core.files.uploadedfile import SimpleUploadedFile

    def test_profile_update_with_image(self):
        """Test profile update with an image upload"""
        self.client.login(username="volunteer1", password="testpass123")
        
        image = SimpleUploadedFile(
            "profile.jpg",
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04\x01\x00\x00\x00\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4C\x01\x00\x3B",
            content_type="image/jpeg"
        )

        response = self.client.post(reverse("accounts:profile"), {
            "email": "updated@example.com",
            "profile_picture": image,
        }, follow=True)

        print("Form errors:", response.context.get('form', {}).errors)  # Debug
        self.assertEqual(response.status_code, 302)  # Should redirect to profile page


    def test_unauthorised_access_to_dashboard(self):
        """Ensure unauthenticated users cannot access the dashboard"""
        response = self.client.get(reverse("accounts:login_redirect"))
        print("Redirect URL:", response.url)  # Debugging
        self.assertRedirects(response, reverse("accounts:login") + "?next=" + reverse("accounts:login_redirect"))

    def test_invalid_login(self):
        """Ensure invalid credentials prevent login"""
        response = self.client.post(reverse("accounts:login"), {
            "username": "wronguser",
            "password": "wrongpass"
        })
        self.assertEqual(response.status_code, 200)  # Should stay on login page
        self.assertContains(response, "Invalid username or password")

    def test_logout(self):
        """Ensure users can log out"""
        self.client.login(username="volunteer1", password="testpass123")
        response = self.client.post(reverse("accounts:logout"))  # Use POST instead of GET
        self.assertEqual(response.status_code, 302)  # Should redirect after logout
