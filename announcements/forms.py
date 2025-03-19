from django import forms
from .models import Announcement, AnnouncementComment

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'event']

class AnnouncementCommentForm(forms.ModelForm):
    class Meta:
        model = AnnouncementComment
        fields = ['comment']
