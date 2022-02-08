from functools import cached_property
from hashlib import md5
from random import randint
import requests

from django.core.cache import cache

from characters.models import Equipment
from encounters.models import Monster


class MonsterApi:
    base_url = "https://www.dnd5eapi.co"
    hero = None

    def __init__(self, hero, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hero = hero

    def _api_getter(self, url):
        cache_key = md5(url.encode("utf-8")).hexdigest()
        json = cache.get(cache_key)
        if json is None:
            try:
                response = requests.get(url)
                json = response.json()
                if response.status_code != 200:
                    return {}
            except requests.exceptions.ConnectionError:
                return {}
        cache.set(cache_key, json, 120)
        return json

    def _get_monster_list(self):
        monsters = self._api_getter(
            f"{self.base_url}/api/monsters?challenge_rating=0.25"
        )
        if monsters is None:
            # Cast into list of dicts. Maybe use values.
            queryset = Monster.objects.all()
            monsters = {"count": queryset.count(), "results": queryset}
        return monsters

    def _random_index(self):
        cache_key = "cached-monster-count"
        count = cache.get(cache_key)
        if count is None:
            count = self._get_monster_list().get("count", 0)
        cache.set(cache_key, count, 120)
        return randint(0, count - 1 if count > 0 else count)

    def _get_a_monster(self, index):
        try:
            data = self._get_monster_list()["results"][index]
        except IndexError:
            return Monster.objects.create(**DEFAULT_MONSTER)

        monster = Monster.objects.filter(index=data["index"]).first()
        if monster is None:
            monster_url = f"{self.base_url}{data['url']}"
            response_json = self._api_getter(monster_url)
            monster, created = Monster.objects.get_or_create(
                name=response_json["name"],
                index=response_json["index"],
                url=response_json["url"],
                armor_class=response_json["armor_class"],
                hit_points=response_json["hit_points"],
            )
        return monster

    @cached_property
    def monster(self):
        return self._get_a_monster(self._random_index())

    def roll(self, dice_sides, number_of_dice, ac):
        hit = randint(1, 20)
        damage = 0
        if hit > ac:
            for i in range(0, number_of_dice):
                damage += randint(1, dice_sides)
        return damage

    def fight(self):
        """ Fairly copy pasty, not a priority to fix.
        """
        monster_hp = self.monster.hit_points
        hero_hp = self.hero.total_health_points
        fight_log = []
        response = {
            "hero": self.hero.name, "monster": self.monster.name, "log": fight_log
        }
        winner = None
        while hero_hp > 0 or monster_hp > 0:
            damage = self.roll(self.hero.weapon.dice_sides, self.hero.weapon.number_of_dice, self.monster.armor_class)
            monster_hp -= damage
            fight_log.append(f"{self.hero.name} hit the {self.monster.name} for {damage} damage.")
            if monster_hp < 1:
                fight_log.append(f"The winner is {self.hero.name}")
                break
            damage = self.roll(self.monster.weapon.dice_sides, self.monster.weapon.number_of_dice, self.hero.armour_class)
            hero_hp -= damage
            fight_log.append(f"{self.monster.name} hit {self.hero.name} for {damage} damage.")
            if hero_hp < 1:
                fight_log.append(f"The winner is the {self.monster.name}")
                break
        return response
