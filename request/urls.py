from django.contrib import admin
from django.urls import path, reverse,include
from .views import *

urlpatterns = [
    path('<int:mentor_id>',request_view),
    path('mentee/<int:mentee_id>/my_request',my_request_view,name="my_request"),
    path('pay',include('pay.urls')),
    path('mentee/<int:mentee_id>/my_request/cancel',request_cancel_view),
    path('mentor/mentor_requests',mentor_requests_view),
    path('mentor/mentor_requests/<int:request_id>',request_brief_view),
    path('mentor/mentor_requests/<int:request_id>/<str:oper>/<int:mentee_id>',mentor_oper_view),

]