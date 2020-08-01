from django.urls import path
from .views import *


urlpatterns = [
    path('',government_schemes_view),
    path('<int:id>',scheme_explain_view),
    path('copyrights',copyrights)
]