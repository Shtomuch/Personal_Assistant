from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone_number")
    search_fields = ("first_name", "last_name", "email", "phone_number")
    fieldsets = (
        (None, {"fields": ("first_name", "last_name", "email", "phone_number")}),
        (
            "Additional Information",
            {"fields": ("address", "birthday"), "classes": ("collapse",)},
        ),
    )
