from django.shortcuts import render
from rest_framework import viewsets

from eikan.models import Games
from apiv1.serializers import GamesSerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Games.objects.all()
    serializer_class = GamesSerializer
