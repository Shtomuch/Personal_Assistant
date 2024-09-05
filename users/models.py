from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
from PIL import Image


class CustomUser(AbstractUser):
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


