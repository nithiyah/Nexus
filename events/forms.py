from django import forms
from .models import Event, FeedbackForm, FeedbackResponse

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'location', 'volunteers_needed', 'roles_responsibilities', 'category']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'category': forms.RadioSelect,  # Use radio buttons for single category selection
        }
# # from django import forms
# # from events.models import Event

# class EventForm(forms.ModelForm):
#     class Meta:
#         model = Event
#         fields = ['name', 'description', 'date', 'location', 'volunteers_needed', 'roles_responsibilities', 'category']

#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop('request', None)  # Capture request object
#         super(EventForm, self).__init__(*args, **kwargs)

#     def save(self, commit=True):
#         event = super(EventForm, self).save(commit=False)
#         if self.request and self.request.user.is_authenticated:
#             event.organisation = self.request.user  # Assign the logged-in organization
#         if commit:
#             event.save()
#         return event
# class FeedbackForm(forms.ModelForm):
#     class Meta:
#         model = Feedback
#         fields = ['rating', 'comments']
#         widgets = {
#             'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
#             'comments': forms.Textarea(attrs={'rows': 4}),
#         }


# class FeedbackForm(forms.ModelForm):
#     class Meta:
#         model = Feedback
#         fields = ['question_1', 'question_2', 'question_3', 'question_4','question_5','additional_feedback']
#         widgets = {
#             'question_1': forms.RadioSelect(choices=Feedback.LIKERT_CHOICES),
#             'question_2': forms.RadioSelect(choices=Feedback.LIKERT_CHOICES),
#             'question_3': forms.RadioSelect(choices=Feedback.LIKERT_CHOICES),
#             'question_4': forms.RadioSelect(choices=Feedback.LIKERT_CHOICES),
#             'question_5': forms.RadioSelect(choices=Feedback.LIKERT_CHOICES),
#             'additional_feedback': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any additional feedback?'}),
#         }






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