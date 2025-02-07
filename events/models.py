# from django.db import models
# from django.conf import settings

# # need to update the different categories
# class Event(models.Model):
#     CATEGORY_CHOICES = [
#         ('education', 'Education'),
#         ('social', 'Social Development'),
#         ('senior', 'Senior Citizen'),
#     ]

#     organisation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     date = models.DateTimeField()
#     location = models.CharField(max_length=255)
#     volunteers_needed = models.PositiveIntegerField()
#     roles_responsibilities = models.TextField()
#     category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank = False, default='education')

#     def __str__(self):
#         return f"{self.name} ({self.get_cate gory_display()})"
from django.db import models
from django.conf import settings

# need to update the different categories
class Event(models.Model):
    CATEGORY_CHOICES = [
        ('Education', 'Education'),
        ('Social Development', 'Social Development'),
        ('Senior Citizen', 'Senior Citizen'),
    ]

    organisation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    volunteers_needed = models.PositiveIntegerField()
    roles_responsibilities = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=False, default='education')

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


# Implementing a waiting list
class VolunteerEvent(models.Model):
    STATUS_CHOICES = [
        ('Registered', 'Registered'),
        ('Waiting List', 'Waiting List'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registered_volunteers")
    volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="registered_events")
    registered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')

    class Meta:
        unique_together = ('event', 'volunteer')  # Prevent duplicate registrations

    def __str__(self):
        return f"{self.volunteer.username} - {self.get_status_display()} for {self.event.name}"
