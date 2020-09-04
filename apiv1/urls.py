from django.urls import path, include
from rest_framework import routers
from apiv1.views import *

app_name = 'apiv1'
urlpatterns = [
    path('games/', GamesList.as_view()),
]
