from django.urls import path
from .views import *


urlpatterns = [
    path('api/hisobot/', HisobotView.as_view()),
]
