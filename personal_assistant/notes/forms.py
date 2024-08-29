from django import forms
from notes.models import Notes

class NoteForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = '__all__'
        labels = {
            "title": "Title",
            "content": "Content",
            "tags": "Tags"
        }