from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('volunteer', 'Volunteer'),
        ('organisation', 'Organisation'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    contact_number = models.CharField(max_length=10, blank= True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    personnel_name = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/',
                                        blank=True,
                                        null=True,
                                        default='profile_pics/default.jpg')
    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.clean()  # Call clean() before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username  #  Keep for easier debugging