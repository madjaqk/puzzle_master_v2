# Generated by Django 2.0 on 2018-02-02 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0011_auto_20180201_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='puzzle',
            name='show_on_main_page',
            field=models.BooleanField(default=False),
        ),
    ]
