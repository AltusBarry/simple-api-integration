from django.db import models

# Create your models here.

class Character(models.Model):
    name = models.CharField(max_length=256)
    armour_class = models.PositiveSmallIntegerField()
    total_health_points = models.PositiveSmallIntegerField()
    current_health_points = models.PositiveSmallIntegerField()
    weapon = models.ForeignKey("Equipment", on_delete=models.PROTECT)

class Equipment(models.Model):
    name = models.CharField(max_length=256)
    dice_sides = models.PositiveSmallIntegerField()
    number_of_dice = models.PositiveSmallIntegerField()
