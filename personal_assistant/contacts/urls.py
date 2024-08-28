from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_list, name='contact_list'),
    path('search/', views.contact_search, name='contact_search'),
    path('add/', views.contact_edit, name='contact_add'),
    path('edit/<int:pk>/', views.contact_edit, name='contact_edit'),
    path('delete/<int:pk>/', views.contact_delete, name='contact_delete'),
]