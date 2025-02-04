from django import forms
from .models import Event

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
