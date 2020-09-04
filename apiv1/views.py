from django.shortcuts import render
from rest_framework import generics

from eikan.models import Games
from apiv1.serializers import GamesSerializer


class GamesList(generics.ListAPIView):
    queryset = Games.objects.all()
    serializer_class = GamesSerializer
