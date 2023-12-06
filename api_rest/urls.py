from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions

from . import views

urlpatterns = [
    path('', views.get_voos, name='get_all_voos'),
    path('voos/<int:id>', views.get_by_id),
    path('data/', views.voos_manager)
]
