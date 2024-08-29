from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
from PIL import Image


class CustomUser(AbstractUser):
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(
        null=True, blank=True, default=None, upload_to="profile_images"
    )  # аватар профілю

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save()
        if self.avatar:
            img = Image.open(self.avatar.path)

            if img.height > 250 or img.width > 250:
                new_img = (250, 250)
                img.thumbnail(new_img)
                img.save(self.avatar.path)
