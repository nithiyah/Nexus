from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from datetime import time 


# need to update the different categories
class Event(models.Model):
    CATEGORY_CHOICES = [
        ('education', 'Education'),
        ('social development', 'Social Development'),
        ('senior citizen', 'Senior Citizen'),
        ('community development', 'Community Development'),
        ('animal welfare', 'Animal Welfare'),
        ('arts, culture & heritage', 'Arts, Culture & Heritage'),
        ('fundraising', 'Fundraising'),
        ('technology & digital volunteering', 'Technology & Digital Volunteering'),
        ('youth & children', 'Youth & Children'),

    ]

    is_completed = models.BooleanField(default=False) 
    organisation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    start_time = models.TimeField(default=time(9, 0))  # Default: 09:00 AM
    end_time = models.TimeField(default=time(17, 0))  # Default: 05:00 PM
    location = models.CharField(max_length=255)
    volunteers_needed = models.PositiveIntegerField()
    roles_responsibilities = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=False, default='Education')

    # # Add event and particpation hours
    # duration_hours = models.FloatField(default=0) 
##############################################################################
    #CAN BE USED IN REPORT BECAUSE THIS CALCULATION DOESNT WORK 
    # def get_duration_hours(self):
    #     """Calculate duration of the event in hours."""
    #     start_datetime = datetime.combine(self.date, self.start_time)
    #     end_datetime = datetime.combine(self.date, self.end_time)
    #     duration = end_datetime - start_datetime
    #     return duration.total_seconds() / 3600  # Convert seconds to hours
#############################################################################

    def get_duration_hours(self):
        # Calculate duration of the event in hours
        if self.start_time and self.end_time:
            start_datetime = datetime.combine(self.date.date(), self.start_time)
            end_datetime = datetime.combine(self.date.date(), self.end_time)

            # Ensure end time is after start time
            if end_datetime < start_datetime:
                return 0  # Invalid time range

            duration = (end_datetime - start_datetime).total_seconds() / 3600
            return round(duration, 2)  # Ensure hours are rounded properly
        return 0


    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class VolunteerParticipation(models.Model):
    volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="participations")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="participations")
    hours_contributed = models.FloatField(default=0)
    date_participated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.volunteer.username} - {self.event.name}"
    
    
# Implementing a waiting list
class VolunteerEvent(models.Model):
    STATUS_CHOICES = [
        ('Registered', 'Registered'),
        ('Waiting List', 'Waiting List'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registered_volunteers")
    volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="registered_events")
    registered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Registered')

    class Meta:
        unique_together = ('event', 'volunteer')  # Prevent duplicate registrations

    def __str__(self):
        return f"{self.volunteer.username} - {self.get_status_display()} for {self.event.name}"

User = get_user_model()
# Model for the Feedback Form (Created by Organisation)
class FeedbackForm(models.Model):
    event = models.OneToOneField("Event", on_delete=models.CASCADE, related_name="feedback_form")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_feedback_forms")
    published = models.BooleanField(default=False)  # Set to True when published

    # Default Likert scale questions
    question_1 = models.CharField(max_length=255, default="How would you rate the overall event experience?")
    question_2 = models.CharField(max_length=255, default="How would you rate the registration process?")
    question_3 = models.CharField(max_length=255, default="How would you rate the event location/venue?")
    question_4 = models.CharField(max_length=255, default="How would you rate the event schedule and timing?")
    question_5 = models.CharField(max_length=255, default="How would you rate the communication before, during, and after the event?")

    # Additional open-ended questions (optional)
    additional_question_1 = models.TextField(blank=True, null=True, verbose_name="Additional Question 1")
    additional_question_2 = models.TextField(blank=True, null=True, verbose_name="Additional Question 2")

    # Follow-up options
    notify_future_events = models.BooleanField(default=True, verbose_name="Would you like to be notified about future events?")
    allow_follow_up_contact = models.BooleanField(default=True, verbose_name="Can we contact you for follow-up?")

    def __str__(self):
        return f"Feedback Form for {self.event.name}"


# Model for Volunteer Feedback Responses
class FeedbackResponse(models.Model):
    feedback_form = models.ForeignKey(FeedbackForm, on_delete=models.CASCADE, related_name="responses")
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedback_responses")

    # Likert scale ratings (1-5)
    rating_1 = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    rating_2 = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    rating_3 = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    rating_4 = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    rating_5 = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    # Open-ended answers
    additional_answer_1 = models.TextField(blank=True, null=True, verbose_name="Response to Additional Question 1")
    additional_answer_2 = models.TextField(blank=True, null=True, verbose_name="Response to Additional Question 2")

    # Follow-up selections
    notify_future_events = models.BooleanField(default=False, verbose_name="Would you like to be notified about future events?")
    allow_follow_up_contact = models.BooleanField(default=False, verbose_name="Can we contact you for follow-up?")

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.volunteer.username} for {self.feedback_form.event.name}"