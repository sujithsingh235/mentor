from django.urls import path
from .views import *

urlpatterns = [
    path('',public_forum_view),
    path('create_new_question',new_question_view),
]