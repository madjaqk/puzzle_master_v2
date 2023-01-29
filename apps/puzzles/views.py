import re
import unicodedata

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Puzzle, PuzzleAnswer, PuzzleSet

def index(request):
	return render(request, "puzzles/index.html", {"sets": PuzzleSet.objects.all()})

def show_puzzle(request, puzzle_id):
	puzzle = get_object_or_404(Puzzle, id=puzzle_id)
	context = {
		"puzzle": puzzle,
		"puzzle_url": f"puzzles/{puzzle.puzzle_set.folder}/{puzzle.short_name}.html",
		"stylesheet": f"puzzles/{puzzle.puzzle_set.folder}/style.css",
	}

	if request.user.is_authenticated:
		context["answer_submissions"] = PuzzleAnswer.objects.filter(user=request.user, puzzle=puzzle)

	return render(request, "puzzles/show_puzzle.html", context)

def check_answer(request):
	if request.method != "POST":
		return redirect("puzzles:index")

	puzz = get_object_or_404(Puzzle, id=request.POST["id"])

	# Convert accented characters to ASCII equivalents
	# This is rough, there's probably a more robust way to do this, but right now there's only one puzzle that could
	# plausibly have a non-ASCII character in the answer. -- JDB 2023-01-27
	submitted_answer = unicodedata.normalize("NFKD", request.POST["answer"].upper()).encode("ascii", "ignore").decode("utf-8")
	submitted_answer = re.sub(r"[^A-Z]", "", submitted_answer)

	if request.user.is_authenticated:
		PuzzleAnswer.objects.create(answer=submitted_answer, user=request.user, puzzle=puzz)

	if puzz.answer == submitted_answer:
		messages.success(request, f"Congratulations!  <b>{submitted_answer}</b> is correct!")
	else:
		messages.error(request, f"Sorry, but {submitted_answer} is not correct.")

	return redirect("puzzles:show_puzzle", request.POST["id"])
