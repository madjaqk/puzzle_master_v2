# Generated by Django 2.0 on 2018-02-02 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0010_auto_20180201_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puzzle',
            name='metapuzzles',
            field=models.ManyToManyField(blank=True, related_name='feeder_puzzles', to='puzzles.Puzzle'),
        ),
    ]
