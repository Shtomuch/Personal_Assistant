from django.urls import path
from notes.views import creationView, updateView, deleteView, showView

urlpatterns = [
    path('create/', creationView, name='order_url'),
    path('show/', showView, name='show_url'),
    path('update/<int:f_id>', updateView, name= 'update_url'),
    path('delete/<int:f_id>', deleteView, name= 'delete_url'),
]