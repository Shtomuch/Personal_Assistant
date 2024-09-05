from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import CustomUser
from notes.models import Notes

from contacts.models import Contact
from files.models import UserFile


@receiver([post_save, post_delete], sender=Notes)
def update_user_last_updated(sender, instance, **kwargs):
    user = instance.user_id
    if user:
        user.updated_at = timezone.now()
        user.save(update_fields=["updated_at"])


@receiver([post_save, post_delete], sender=Contact)
def update_user_last_updated_contacts(sender, instance, **kwargs):
    user = instance.user  # Використовуємо правильне ім'я поля
    if user:
        user.updated_at = timezone.now()
        user.save(update_fields=["updated_at"])


@receiver([post_save, post_delete], sender=UserFile)
def update_user_last_updated_files(sender, instance, **kwargs):
    user = instance.user  # Використовуємо правильне ім'я поля
    if user:
        user.updated_at = timezone.now()
        user.save(update_fields=["updated_at"])
