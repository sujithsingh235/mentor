from django.urls import path
from .views import *

urlpatterns = [
    path('page-<int:page>',public_forum_view),
    path('create_new_question',new_question_view),
    path('<int:id>',question_brief_view),
    path('write_answer/<int:id>',write_answer_view),
    path('comments/<int:id>',comments_view),
    path('edit_answer/<int:id>/<int:question_id>',edit_answer_view),
    path('delete_answer',delete_answer_view),
    path('add_like',add_like_view),
    path('remove_like',remove_like_view),
    path('my_questions',my_questions_view),
    path('my_answers',my_answers_view),
    path('fav_add',fav_view),
    path('fav_remove',fav_remove_view),
    path('my_favourite',my_favourite_view),
    path('report',report_view),
    path('get_tags',get_tags_view),
    path('delete_question/<int:id>',delete_question_view),
    path('tag_question_forum',tag_question_view)
]