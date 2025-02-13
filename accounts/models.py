from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('volunteer', 'Volunteer'),
        ('organisation', 'Organisation'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    contact_number = models.CharField(max_length=10, blank= True, null=True)

    def __str__(self):
        return self.username
