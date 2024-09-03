from django.contrib import admin
from .models import Notes, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ('title', 'user_id', 'created_at')
    search_fields = ('title', 'content', 'user_id__username')
    list_filter = ('created_at', 'tags')
    ordering = ('-created_at',)
    filter_horizontal = ('tags',)
