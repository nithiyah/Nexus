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
from django.contrib.auth import get_user_model


# need to update the different categories
class Event(models.Model):
    CATEGORY_CHOICES = [
        ('education', 'Education'),
        ('social development', 'Social Development'),
        ('senior citizen', 'Senior Citizen'),
    ]

    organisation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    volunteers_needed = models.PositiveIntegerField()
    roles_responsibilities = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=False, default='Education')

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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Registered')

    class Meta:
        unique_together = ('event', 'volunteer')  # Prevent duplicate registrations

    def __str__(self):
        return f"{self.volunteer.username} - {self.get_status_display()} for {self.event.name}"

# class Feedback(models.Model):
#     event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='feedbacks')
#     volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     question_1 = models.CharField(max_length=255, default="Neutral")  # ✅ Add default
#     submitted = models.BooleanField(default=False)
#     # Likert scale choices
#     LIKERT_CHOICES = [
#         (1, 'Strongly Disagree'),
#         (2, 'Disagree'),
#         (3, 'Neutral'),
#         (4, 'Agree'),
#         (5, 'Strongly Agree')
#     ]

#     # feedback form questions
#     question_1 = models.IntegerField(choices=LIKERT_CHOICES, verbose_name="The event was well organized")
#     question_2 = models.IntegerField(choices=LIKERT_CHOICES, verbose_name="I had a positive experience")
#     question_3 = models.IntegerField(choices=LIKERT_CHOICES, verbose_name="I would volunteer again for this event")
    
#     additional_comments = models.TextField("Additional Comments (optional)", blank=True)

#     submitted_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.volunteer.username} - Feedback for {self.event.name}"

# class Feedback(models.Model):
#     event = models.ForeignKey("events.Event", on_delete=models.CASCADE)
#     volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 stars
#     comments = models.TextField(blank=True, null=True)
#     submitted_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Feedback by {self.volunteer.full_name} for {self.event.name}"


# class Feedback(models.Model):
#     event = models.ForeignKey('events.Event', on_delete=models.CASCADE)  # Use app_label.ModelName
#     volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

#     # Likert scale questions with default values
#     LIKERT_CHOICES = [
#         ("Strongly Disagree", "Strongly Disagree"),
#         ("Disagree", "Disagree"),
#         ("Neutral", "Neutral"),
#         ("Agree", "Agree"),
#         ("Strongly Agree", "Strongly Agree"),
#     ]

#     question_1 = models.CharField(max_length=255, choices=LIKERT_CHOICES, default="Neutral")
#     question_2 = models.CharField(max_length=255, choices=LIKERT_CHOICES, default="Neutral")
#     question_3 = models.CharField(max_length=255, choices=LIKERT_CHOICES, default="Neutral")
#     question_4 = models.CharField(max_length=255, choices=LIKERT_CHOICES, default="Neutral")
#     question_5 = models.CharField(max_length=255, choices=LIKERT_CHOICES, default="Neutral")

#     additional_feedback = models.TextField(blank=True, null=True)
#     submitted = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Feedback from {self.volunteer.username} for {self.event.name}"
# from django.db import models
# from django.conf import settings

# class FeedbackForm(models.Model):
#     event = models.OneToOneField("Event", on_delete=models.CASCADE, related_name="feedback_form")
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     published = models.BooleanField(default=False)  # Set to True when published

#     question_1 = models.CharField(max_length=255, default="How would you rate the overall event experience?")
#     question_2 = models.CharField(max_length=255, default="How would you rate the registration process?")
#     question_3 = models.CharField(max_length=255, default="How would you rate the event location/venue?")
#     question_4 = models.CharField(max_length=255, default="How would you rate the event schedule and timing?")
#     question_5 = models.CharField(max_length=255, default="How would you rate the communication before, during, and after the event?")
    
#     additional_question_1 = models.TextField(blank=True, null=True)
#     additional_question_2 = models.TextField(blank=True, null=True)
    
#     notify_future_events = models.BooleanField(default=True)
#     allow_follow_up_contact = models.BooleanField(default=True)

#     def __str__(self):
#         return f"Feedback for {self.event.name}"

# class FeedbackResponse(models.Model):
#     feedback_form = models.ForeignKey(FeedbackForm, on_delete=models.CASCADE, related_name="responses")
#     volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
#     rating_1 = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
#     rating_2 = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
#     rating_3 = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
#     rating_4 = models.IntegerField(choices=[(i, i) or i in range(1, 6)])
#     rating_5 = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    
#     additional_answer_1 = models.TextField(blank=True, null=True)
#     additional_answer_2 = models.TextField(blank=True, null=True)

#     notify_future_events = models.BooleanField(default=False)
#     allow_follow_up_contact = models.BooleanField(default=False)

#     submitted_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Feedback from {self.volunteer.username} for {self.feedback_form.event.name}"
# User = get_user_model()

# class Feedback(models.Model):
#     event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name="feedback")
#     volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedback_submissions")
    
#     # Likert scale questions (1 to 5 rating)
#     event_experience = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Overall event experience")
#     registration_process = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Registration process")
#     venue_rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Event location/venue")
#     event_timing = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Event schedule and timing")
#     communication = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Communication before, during, and after the event")

#     # Open-ended feedback
#     liked_most = models.TextField(blank=True, null=True, verbose_name="What did you like most about the event?")
#     liked_least = models.TextField(blank=True, null=True, verbose_name="What did you like least about the event?")
#     improvement_suggestions = models.TextField(blank=True, null=True, verbose_name="Suggestions for improving future events")

#     # Follow-up questions
#     notify_future_events = models.BooleanField(default=False, verbose_name="Would you like to be notified about future events?")
#     follow_up_permission = models.BooleanField(default=False, verbose_name="Can we contact you for further clarification or follow-up?")

#     submitted_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Feedback by {self.volunteer.username} for {self.event.name}"


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