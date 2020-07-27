from django.contrib import admin
from django.urls import path, reverse,include

from .views import news_view
urlpatterns = [
    path('',news_view)
]