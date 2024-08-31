from django.urls import path
from notes.views import CreateNoteView, UpdateNoteView, DeleteNoteView, ShowNoteView, MainView, AddTagView

urlpatterns = [
    path('', MainView.as_view(), name='main_url'),
    path('create/', CreateNoteView.as_view(), name='create_url'),
    path('show/<int:f_id>', ShowNoteView.as_view(), name='show_url'),
    path('update/<int:f_id>', UpdateNoteView.as_view(), name= 'update_url'),
    path('delete/<int:f_id>', DeleteNoteView.as_view(), name= 'delete_url'),
    path('create_tag/', AddTagView.as_view(), name='tag_create_url')
]