# files/forms.py
from django import forms
from .models import UserFile

from django import forms
from .models import UserFile


class UploadForm(forms.ModelForm):
    class Meta:
        model = UserFile
        fields = ['title', 'file', 'category']

    def clean_file(self):
        file = self.cleaned_data.get('file')

        # Перевірка розміру файлу
        if file.size > 10 * 1024 * 1024:  # 10 МБ
            raise forms.ValidationError('Розмір файлу не повинен перевищувати 10МБ')

        return file

#default_auto_field = 'django.db.models.BigAutoField'