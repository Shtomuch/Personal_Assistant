from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import CustomUser
from contacts.models import Contact


@receiver(
    [post_save, post_delete], sender=Contact
)  # для того, щоб колонка updated_at реагувала на зміни в контактах, ще не ясно чи працює
def update_user_last_updated(sender, instance, **kwargs):
    user = instance.user
    user.last_updated = timezone.now()
    user.save()
