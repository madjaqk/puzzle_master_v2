from django.urls import path
from . import views

app_name = "puzzles"

urlpatterns = [
	path("", views.index, name="index"),
	path("meta/<int:meta_id>", views.show_meta, name="show_meta"),
	path("puzzle/<int:puzzle_id>", views.show_puzzle, name="show_puzzle"),
	path("check", views.check_answer, name="check_answer"),
]