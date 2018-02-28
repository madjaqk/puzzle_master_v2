from django.contrib import admin

from .models import PuzzleSet, Puzzle, PuzzleAnswer

admin.site.register(Puzzle)
admin.site.register(PuzzleSet)
admin.site.register(PuzzleAnswer)