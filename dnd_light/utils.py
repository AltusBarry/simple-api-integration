from random import randint
import requests

from django.core.cache import cache

from characters.models import Equipment
from encounters.models import Monster


def sync_equipment():
    # Hardcoded, should be env driven or a proper API helper written.
    url = "https://api.open5e.com/weapons/"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return False
    except requests.exceptions.ConnectionError:
        return False

    # We assume the response is consistent in this implementation of the code.
    json = response.json()
    for result in response.json()["results"]:
        dice = result.get("damage_dice")

        # If the key is missing an empty string or a specific case we don't
        # cover atm, skip the item.
        if not dice or "d" not in dice or not result.get("name"):
            continue
        number_of_dice, dice_sides = dice.split("d")

        # Might create duplicate items if data changes, data consistency not an
        # issue for this.
        Equipment.objects.get_or_create(
            name=result["name"],
            number_of_dice=number_of_dice,
            dice_sides=dice_sides,
        )
    return True


class Encounter:
    base_url = "https://www.dnd5eapi.co"

    def _api_fetch(self):
        url = f"{self.base_url}/api/monsters?challenge_rating=0.25"
        cache_key = md5(url.encode("utf-8")).hexdigest()
        json = cache.get(cache_key)
        if json is None:
            try:
                response = requests.get(url)
                if response.status_code != 200:
                    return {}
            except requests.exceptions.ConnectionError:
                return {}
        json = response.json()
        cache.set(cache_key, json, 60)
        return json

    def _random_int(self):
        cache_key = "cached-monster-count"
        count = cache.get(cache_key)
        if count is None:
            count = self._fetch_monsters().get("count", 0)
        cache.set(cache_key, count, 120)
        return randint(0, count - 1 if count > 0 else count)

    def _get_a_monster(self, index):
        try:
            monster = self.monsters[self._random_int]
        except IndexError:
            # create and return dummy monster
        monster_url = f"{self.base_url}{response.json()['results'][index]['url']}"
        self.index

    @property
    def monsters(self):
        monsters = self._api_fetch().get("results", None)
        if monsters is None:
            # Cast into list of dicts. Maybe use values.
            queryset = Monster.objects.all()
            monsters = {"count": queryset.count(), "results": queryset}
        return monsters
