# Generated by Django 4.0.2 on 2022-02-09 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("characters", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Monster",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=256)),
                ("index", models.SlugField()),
                ("url", models.CharField(max_length=256)),
                ("armor_class", models.PositiveSmallIntegerField()),
                ("hit_points", models.PositiveSmallIntegerField()),
                (
                    "weapon",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="characters.equipment",
                    ),
                ),
            ],
        ),
    ]
