import re

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Metapuzzle, Puzzle, PuzzleAnswer

def index(request):
	# More code here
	return render(request, "puzzles/index.html", {"metas": Metapuzzle.objects.all()})

def show_meta(request, meta_id):
	meta = get_object_or_404(Metapuzzle, id=meta_id)
	context = {
		"meta": meta,
		"meta_url": f"puzzles/{meta.templates_folder}/index.html",
	}
	return render(request, "puzzles/show_meta.html", context)

def show_puzzle(request, puzzle_id):
	puzzle = get_object_or_404(Puzzle, id=puzzle_id)
	context = {
		"puzzle": puzzle,
		"puzzle_url": f"puzzles/{puzzle.metapuzzle.templates_folder}/{puzzle.short_name}.html",
	}

	if request.user.is_authenticated:
		context["answer_submissions"] = PuzzleAnswer.objects.filter(user=request.user, puzzle=puzzle)
		context["solved"] = any(answer.correct for answer in context["answer_submissions"])

	return render(request, "puzzles/show_puzzle.html", context)

def check_answer(request):
	if request.method != "POST":
		return redirect("puzzles:index")

	# Yes, this uses the magic strings "meta" and "non-meta".  I wanted to write a single check_answer method instead of separate check_puzzle and check_metapuzzle functions, so I needed some way to distinguish what I was looking for; the strings here seemed better than a magic number status code.
	puzzle_types = {
		"meta": (Metapuzzle, "puzzles:show_meta"),
		"non-meta": (Puzzle, "puzzles:show_puzzle")
	}

	puzz_type, route = puzzle_types[request.POST["type"]]

	puzz = get_object_or_404(puzz_type, id=request.POST["id"])

	submitted_answer = re.sub(r"[^A-Z]", "", request.POST["answer"].upper())

	if request.user.is_authenticated and puzz_type == Puzzle:
		PuzzleAnswer.objects.create(answer=submitted_answer, user=request.user, puzzle=puzz)

	if puzz.answer == submitted_answer:
		messages.success(request, f"Congratulations!  <b>{submitted_answer}</b> is correct!")
	else:
		messages.error(request, f"Sorry, but {submitted_answer} is not correct.")

	return redirect(route, request.POST["id"])