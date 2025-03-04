from django import forms
from .models import Event, FeedbackForm, FeedbackResponse

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'start_time', 'end_time' ,'location', 'volunteers_needed', 'roles_responsibilities', 'category']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),

            # Allows for event organiserts to input time data 
            # Ensures accurate calculation of volunteer hours
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'category': forms.RadioSelect,  # Use radio buttons for single category selection
        }


class FeedbackFormForm(forms.ModelForm):
    class Meta:
        model = FeedbackForm
        fields = [
            "question_1", "question_2", "question_3", "question_4", "question_5",
            "additional_question_1", "additional_question_2",
            "notify_future_events", "allow_follow_up_contact"
        ]

class FeedbackResponseForm(forms.ModelForm):
    class Meta:
        model = FeedbackResponse
        fields = [
            "rating_1", "rating_2", "rating_3", "rating_4", "rating_5",
            "additional_answer_1", "additional_answer_2",
            "notify_future_events", "allow_follow_up_contact"
        ]