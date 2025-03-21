from django import forms
from .models import Announcement, AnnouncementComment

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'event']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Important Event Update'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your announcement here...',
                'rows': 5
            }),
            'event': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

class AnnouncementCommentForm(forms.ModelForm):
    class Meta:
        model = AnnouncementComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control comment-textarea',
                'placeholder': 'Write your comment...',
                'rows': 4,
            })
        }
        