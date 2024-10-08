from django.db import models
from users.models import CustomUser
from .storage_backends import PublicMediaStorage, PrivateMediaStorage

CATEGORY_CHOICES = [
    ('image', 'Image'),
    ('document', 'Document'),
    ('video', 'Video'),
    ('other', 'Other'),
]

def user_directory_path(instance, filename):
    # Динамічний шлях для зберігання файлів користувача
    return f'user_{instance.user.id}/{filename}'

class UserFile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Прив'язка до користувача
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to=user_directory_path, storage=PublicMediaStorage())  # Використовуйте потрібне сховище
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title





class Upload(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(storage=PublicMediaStorage())


class UploadPrivate(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(storage=PrivateMediaStorage())
