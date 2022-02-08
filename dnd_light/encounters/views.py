from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, mixins

from characters.models import Character
from characters.serializers import CharacterSerializer
from encounters.models import Monster
from encounters.serializers import MonsterSerializer
from encounters.utils import MonsterApi


class MonsterViewSet(viewsets.ModelViewSet):
    """Displays monster details."""

    queryset = Monster.objects.all()
    serializer_class = MonsterSerializer


class PlayOutEncounter(viewsets.GenericViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer

    def retrieve(self, request, pk):
        """
        EncounterViewSet hero/monster
        Return list of rolls or something
        """
        results = MonsterApi(Character.objects.get(pk=pk)).fight()
        return JsonResponse(results, safe=False)
