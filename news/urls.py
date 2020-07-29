from django.contrib import admin
from django.urls import path, reverse,include

from .views import *
urlpatterns = [
    path('',news_home_view,name="news_home"),
    path('request_news',request_news_view,name="request_news")
]