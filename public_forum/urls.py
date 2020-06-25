from django.urls import path
from .views import *

urlpatterns = [
    path('',public_forum_view),
    path('create_new_question',new_question_view),
    path('<int:id>',question_brief_view),
    path('write_answer/<int:id>',write_answer_view),
    path('comments/<int:id>',comments_view),
    path('edit_answer/<int:id>/<int:question_id>',edit_answer_view),
    path('delete_answer',delete_answer_view)
]