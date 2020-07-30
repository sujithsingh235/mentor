from django.contrib import admin
from django.urls import path, reverse,include
from .views import *

urlpatterns = [
    path('<int:mentor_id>',request_view),
    path('my_request',my_request_view),
    path('my_request/<int:id>',request_brief_view)
]