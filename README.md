# simple-api-integration
Go to the repo root, same directory as this README is located in.

Ensure docker compose is installed.

Then run:

    docker-compose up

The compose file exposes the drf endpoints on http://localhost:8000

We have no frontend apart from the default drf interactive api views. No authentication was added.

Urls of interest:
-----------------

    http://localhost:8000/characters/:
        Create and view characters

    http://localhost:8000/equipment/
        Would be used to populate equipment list dropdowns for character create. Contains the ids for the character weapon index.

    http://localhost:8000/equipment/sync_gear/
        Pulls a list of gear from an external api and stores it in our local db.

    http://localhost:8000/encounters/<character_pk>/
        Does a simple little dice roll battle and returns the roll log.
        Fetches a random monster from an external api and pits the indicated character against it.


# Endpoints

Character endpoint
------------------

    http://localhost:8000/characters/
    GET example: [
        {
            "id": 1,
            "name": "Peanut",
            "armour_class": 10,
            "total_health_points": 15,
            "weapon": "http://localhost:8000/equipment/1/"
        },
        {
            "id": 2,
            "name": "Alex",
            "armour_class": 10,
            "total_health_points": 3,
            "weapon": "http://localhost:8000/equipment/16/"
        }
    ]
    POST example: {
            "name": "Peanut",
            "armour_class": 13,
            "total_health_points": 15,
            "weapon": 1
        }
    GET detail http://localhost:8000/characters/<pk>/: {
        "id": 1,
        "name": "Peanut",
        "armour_class": 10,
        "total_health_points": 15,
        "weapon": "http://localhost:8000/equipment/1/"
    }

Equipment endpoint
------------------

    http://localhost:8000/equipment/
    GET example: [
        {
            "id": 1,
            "name": "Wooden sword",
            "dice_sides": 1,
            "number_of_dice": 1
        },
        {
            "id": 2,
            "name": "Club",
            "dice_sides": 4,
            "number_of_dice": 1
        },
    ]

Endpoint to trigger gear sync
-----------------------------

    http://localhost:8000/equipment/sync_gear/
    GET example: {"success": "Sync completed"}

Monster endpoint
----------------

    http://localhost:8000/monsters/
    GET example: [
        {
            "name": "Training dummy",
            "armor_class": 1,
            "hit_points": 20
        },
        {
            "name": "Giant Poisonous Snake",
            "armor_class": 14,
            "hit_points": 11
        }
    ]

Encounter endpoint
------------------

    http://localhost:8000/encounters/<hero_id>/
    GET example: {
    "hero":"Peanut",
    "monster":"Giant Poisonous Snake",
    "log":[
        "Peanut hit the Giant Poisonous Snake for 1 damage.",
        "Giant Poisonous Snake hit Peanut for 0 damage.",
        "Peanut hit the Giant Poisonous Snake for 1 damage.",
        "Giant Poisonous Snake hit Peanut for 2 damage.",
        "Peanut hit the Giant Poisonous Snake for 1 damage.",
        "Giant Poisonous Snake hit Peanut for 0 damage.",
        "Peanut hit the Giant Poisonous Snake for 0 damage.",
        "Giant Poisonous Snake hit Peanut for 0 damage.",
        "Peanut hit the Giant Poisonous Snake for 0 damage.",
        "Giant Poisonous Snake hit Peanut for 0 damage.",
        "Peanut hit the Giant Poisonous Snake for 0 damage.",
        "Giant Poisonous Snake hit Peanut for 6 damage.",
        "Peanut hit the Giant Poisonous Snake for 1 damage.",
        "Giant Poisonous Snake hit Peanut for 0 damage.",
        "Peanut hit the Giant Poisonous Snake for 0 damage.",
        "Giant Poisonous Snake hit Peanut for 0 damage.",
        "Peanut hit the Giant Poisonous Snake for 1 damage.",
        "Giant Poisonous Snake hit Peanut for 0 damage.",
        "Peanut hit the Giant Poisonous Snake for 0 damage.",
        "Giant Poisonous Snake hit Peanut for 4 damage.",
        "Peanut hit the Giant Poisonous Snake for 1 damage.",
        "Giant Poisonous Snake hit Peanut for 0 damage.",
        "Peanut hit the Giant Poisonous Snake for 0 damage.",
        "Giant Poisonous Snake hit Peanut for 6 damage.",
        "The winner is the Giant Poisonous Snake"
        ]
    }


Testing
-------
Step into the Django project directory

    cd dnd_light/

Create a virtual environment using python 3.8.

	virtualenv ve -p python3.8

Activate the virtual environment

	source ./ve/bin/activate

Install requirements

	pip install -r requirements.txt

Run the tests with coverage

	coverage run manage.py test
	coverage report -m

