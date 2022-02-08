# Generated by Django 4.0.2 on 2022-02-08 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('dice_sides', models.PositiveSmallIntegerField()),
                ('number_of_dice', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('armour_class', models.PositiveSmallIntegerField()),
                ('total_health_points', models.PositiveSmallIntegerField()),
                ('weapon', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='characters.equipment')),
            ],
        ),
    ]
