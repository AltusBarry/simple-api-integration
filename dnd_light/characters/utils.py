from hashlib import md5
from random import randint
import requests

from django.core.cache import cache

from characters.constants import DEFAULT_EQUIPMENT
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

        # If the key is missing, an empty string or a specific case we don't
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
