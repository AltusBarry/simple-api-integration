from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from characters.models import Character, Equipment
from characters.serializers import CharacterSerializer, EquipmentSerializer
from characters.utils import sync_equipment


class CharacterViewSet(viewsets.ModelViewSet):
    """Displays character details."""

    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    """Displays equipment details."""

    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    @action(methods=["get"], detail=False)
    def sync_gear(self, request):
        success = sync_equipment()
        return JsonResponse({"success": success})
