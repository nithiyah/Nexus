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
