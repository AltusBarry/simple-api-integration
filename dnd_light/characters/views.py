from rest_framework import viewsets
from rest_framework import permissions

from characters.models import Character, Equipment
from characters.serializers import CharacterSerializer, EquipmentSerializer


class CharacterViewSet(viewsets.ModelViewSet):
    """Displays character details."""

    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    """Displays character details."""

    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
