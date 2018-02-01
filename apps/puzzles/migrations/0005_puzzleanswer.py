# Generated by Django 2.0 on 2018-02-01 04:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0004_metapuzzle_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='PuzzleAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('puzzle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submitted_answers', to='puzzles.Puzzle')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='puzzle_answers', to='puzzles.Puzzle')),
            ],
        ),
    ]
