from django.urls import path
from .views import file_list, download_file, delete_file, upload_file

urlpatterns = [
    path('upload/', upload_file, name='image_upload'),
    path('', file_list, name='file_list'),
    path('download/<int:file_id>/', download_file, name='download_file'),
    path('delete/<int:file_id>/', delete_file, name='delete_file'),
]