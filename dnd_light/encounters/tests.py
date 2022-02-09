from unittest import mock
import requests
import responses

from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APIRequestFactory

from encounters.utils import MonsterApi
from characters.models import Character, Equipment

LIST_RESPONSE = {
    "count": 4,
    "results": [
        {"index": "acolyte", "name": "Acolyte", "url": "/api/monsters/acolyte"},
        {
            "index": "axe-beak",
            "name": "Axe Beak",
            "url": "/api/monsters/axe-beak",
        },
        {"index": "boar", "name": "Boar", "url": "/api/monsters/boar"},
        {"index": "elk", "name": "Elk", "url": "/api/monsters/elk"},
    ],
}
DETAIL_RESPONSE = {
    "index": "axe-beak",
    "name": "Axe Beak",
    "size": "Large",
    "type": "beast",
    "subtype": None,
    "alignment": "unaligned",
    "armor_class": 11,
    "hit_points": 19,
    "hit_dice": "3d10",
    "speed": {"walk": "50 ft."},
    "strength": 14,
    "dexterity": 12,
    "constitution": 12,
    "intelligence": 2,
    "wisdom": 10,
    "charisma": 5,
    "proficiencies": [],
    "damage_vulnerabilities": [],
    "damage_resistances": [],
    "damage_immunities": [],
    "condition_immunities": [],
    "senses": {"passive_perception": 10},
    "languages": "",
    "challenge_rating": 0.25,
    "xp": 50,
    "actions": [
        {
            "name": "Beak",
            "desc": "Melee Weapon Attack: +4 to hit, reach 5 ft., one target. Hit: 6 (1d8 + 2) slashing damage.",
            "attack_bonus": 4,
            "damage": [
                {
                    "damage_type": {
                        "index": "slashing",
                        "name": "Slashing",
                        "url": "/api/damage-types/slashing",
                    },
                    "damage_dice": "1d8+2",
                }
            ],
        }
    ],
    "url": "/api/monsters/axe-beak",
}


def mocked_get(url, *args, **kwargs):
    class StubResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if "challenge_rating=0.25" in url:
        return StubResponse(LIST_RESPONSE, 200)
    else:
        return StubResponse(DETAIL_RESPONSE, 200)

    return MockResponse(None, 404)


class TestEncounters(TestCase):
    client_class = APIClient
    fixtures = ["fixtures.json"]

    @mock.patch.object(MonsterApi, "roll", return_value=20)
    @mock.patch("requests.get", side_effect=mocked_get)
    def test_monster_api_util(self, mocked, mocked_2):
        hero = Character.objects.create(
            name="Jerry",
            armour_class=10,
            total_health_points=20,
            weapon=Equipment.objects.first(),
        )
        monster_api = MonsterApi(hero)
        monster = monster_api.monster
        self.assertEqual(monster.id, 2)
        self.assertEqual(monster.name, "Axe Beak")
        results = monster_api.fight()
        self.assertDictEqual(
            results,
            {
                "hero": "Jerry",
                "monster": "Axe Beak",
                "log": [
                    "Jerry hit the Axe Beak for 20 damage.",
                    "The winner is Jerry",
                ],
            },
        )

    @mock.patch.object(MonsterApi, "roll", return_value=5)
    @mock.patch("requests.get", side_effect=mocked_get)
    def test_encounter_api(self, mocked, mocked_2):
        hero = Character.objects.create(
            name="Paul",
            armour_class=10,
            total_health_points=20,
            weapon=Equipment.objects.first(),
        )
        url = reverse("encounters-detail", kwargs={"pk": hero.id})
        response = self.client.get(url)
        self.assertDictEqual(
            response.json(),
            {
                "hero": "Paul",
                "monster": "Axe Beak",
                "log": [
                    "Paul hit the Axe Beak for 5 damage.",
                    "Axe Beak hit Paul for 5 damage.",
                    "Paul hit the Axe Beak for 5 damage.",
                    "Axe Beak hit Paul for 5 damage.",
                    "Paul hit the Axe Beak for 5 damage.",
                    "Axe Beak hit Paul for 5 damage.",
                    "Paul hit the Axe Beak for 5 damage.",
                    "The winner is Paul",
                ],
            },
        )
        hero = Character.objects.create(
            name="Pete",
            armour_class=3,
            total_health_points=5,
            weapon=Equipment.objects.first(),
        )
        url = reverse("encounters-detail", kwargs={"pk": hero.id})
        response = self.client.get(url)
        self.assertDictEqual(
            response.json(),
            {
                "hero": "Pete",
                "monster": "Axe Beak",
                "log": [
                    "Pete hit the Axe Beak for 5 damage.",
                    "Axe Beak hit Pete for 5 damage.",
                    "The winner is the Axe Beak",
                ],
            },
        )
