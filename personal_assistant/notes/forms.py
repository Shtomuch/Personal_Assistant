from django import forms
from django.forms import CheckboxSelectMultiple

from notes.models import Notes, Tag

class NoteForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ["title", "content", "tags"]
        widgets = {
            'tag': CheckboxSelectMultiple()
        }

class TagCreateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]

