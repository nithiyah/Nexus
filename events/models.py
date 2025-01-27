from django.db import models
from django.conf import settings

# need to update the different categories
class Event(models.Model):
    CATEGORY_CHOICES = [
        ('education', 'Education'),
        ('social', 'Social Development'),
        ('senior', 'Senior Citizen'),
    ]

    organisation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    volunteers_needed = models.PositiveIntegerField()
    roles_responsibilities = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank = False, default='education')

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
