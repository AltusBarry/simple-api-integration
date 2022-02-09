from django.db import models
from django.core.validators import MaxValueValidator


class Character(models.Model):
    name = models.CharField(max_length=256)
    armour_class = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(15),
        ]
    )
    total_health_points = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(20),
        ]
    )
    weapon = models.ForeignKey("Equipment", on_delete=models.PROTECT)


class Equipment(models.Model):
    name = models.CharField(max_length=256)
    dice_sides = models.PositiveSmallIntegerField()
    number_of_dice = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.name} - {self.number_of_dice}d{self.dice_sides}"
