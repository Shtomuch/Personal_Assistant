from django.db import models

# Create your models here.
from django.db import models
from ..users.models import CustomUser

class Contact(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='contacts')
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    email = models.EmailField(unique=True, verbose_name="Email Address")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number")
    address = models.CharField(
        max_length=255, verbose_name="Address", blank=True, null=True
    )
    birthday = models.DateField(verbose_name="Birthday", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
