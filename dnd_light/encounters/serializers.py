from encounters.models import Monster

from rest_framework import serializers


class MonsterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Monster
        fields = ["name", "armor_class", "hit_points", "weapon"]
