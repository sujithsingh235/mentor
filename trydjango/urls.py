"""trydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, reverse,include
# Created Apps
from chat.views import *
from homepage.views import *
from user_signup.views import *
from public_forum.views import public_forum_view

urlpatterns = [
# Homepage Views
    path('',homepage_view),
    path('mentee_home/',mentee_home,name='mentee_home'),
    path('mentor_home/',mentor_home,name='mentor_home'),
    path('search_mentor/',search_mentor,name='search_mentor'),
    path('search_mentor/mentor_detail/<int:mentor_id>/',mentor_detail,name='mentor_detail'),
    path('mentor_request/<int:mentor_id>/',send_req,name='send_request'),
    path('my_requests/',my_requests,name='my_requests'),
    path('accept_request/',accept_req,name='accept_request'),
# User_signup View
	path('signup/mentee/', mentee_signup_view),
    path('signup/mentor/',mentor_signup_view),
    path('sub_field/',sub_field_view),
    path('email/verify/<str:role>/<str:username>/',email_verify,name="email_verify"),
    path('user_login/',user_login,name='user_login'),
    path('logout/',logout,name='logout'),
    path('temp_view/',temp_view),
    path('temp_view2/',temp_view2,name='temp_view2'),
# Public Forum Views
    path('public/forum/',include('public_forum.urls')),
# Admin
    path('admin/', admin.site.urls),
]
