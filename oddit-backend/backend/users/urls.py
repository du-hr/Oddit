from django.urls import path
from django.contrib import admin
from .views import UserCreateAPIView

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
]