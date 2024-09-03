from django.contrib import admin
from .models import UserFile, Upload, UploadPrivate

@admin.register(UserFile)
class UserFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'uploaded_at')
    search_fields = ('title', 'user__username', 'category')
    list_filter = ('category', 'uploaded_at')
    ordering = ('-uploaded_at',)

@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at')
    ordering = ('-uploaded_at',)

@admin.register(UploadPrivate)
class UploadPrivateAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at')
    ordering = ('-uploaded_at',)