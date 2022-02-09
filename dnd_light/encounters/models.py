from django.db import models

from characters.models import Equipment


class Monster(models.Model):
    name = models.CharField(max_length=256)
    index = models.SlugField()
    url = models.CharField(max_length=256)
    armor_class = models.PositiveSmallIntegerField()
    hit_points = models.PositiveSmallIntegerField()

    # Make use of character equipment due to dnd monster actions being too
    # complex for what we need.
    weapon = models.ForeignKey(Equipment, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        # Random equipment piece on every save. Slow query, but our data set is
        # small.
        self.weapon = Equipment.objects.order_by("?").first()
        super().save()
