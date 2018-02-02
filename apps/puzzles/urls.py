from django.urls import path
from . import views

app_name = "puzzles"

urlpatterns = [
	path("", views.index, name="index"),
	path("puzzle/<int:puzzle_id>", views.show_puzzle, name="show_puzzle"),
	path("check", views.check_answer, name="check_answer"),
]