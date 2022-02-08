from characters.models import Character, Equipment

from rest_framework import serializers


class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Character
        fields = ["name", "armour_class", "total_health_points", "weapon"]


class EquipmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Equipment
        fields = ["name", "dice_sides", "number_of_dice"]
