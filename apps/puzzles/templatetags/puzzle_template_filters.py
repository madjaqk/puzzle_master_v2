from django import template
from django.urls import reverse

from apps.puzzles.models import Puzzle

register = template.Library()

@register.filter(name="range")
def filter_range(start, end):
	return list(str(i) for i in range(start, end))

@register.filter
def solved_by(puzzle, user):
	return puzzle.solved_by_user(user)

@register.filter
def user_solved(user, puzzle_id):
	return Puzzle.objects.get(id=puzzle_id).solved_by_user(user)

@register.filter
def as_ul(meta, user):
	output = ["<ul>"]

	for puzzle in sorted(meta.feeder_puzzles.all(), key=lambda x: x.sort_order):
		middle = f"<a href=\"{reverse('puzzles:show_puzzle', args=[puzzle.id])}\">{puzzle.name}</a>"
		if puzzle.solved_by_user(user):
			final = f"<li><span class='solved'>{middle}</span> <strong>{puzzle.answer}</strong></li>"
		else:
			final = f"<li>{middle}</li>"
		output.append(final)

	output.append("</ul>")
	
	return "\n".join(output)

@register.filter
def puzzle_ids_to_ol(ids, user):
	# Takes ids as a space-separated string due to Django templating restrictions
	output = ["<ol>"]
	
	for puzz_id in ids.split():
		puzzle = Puzzle.objects.get(id=puzz_id)
		middle = f"<a href=\"{reverse('puzzles:show_puzzle', args=[puzz_id])}\">{puzzle.name}</a>"
		if puzzle.solved_by_user(user):
			final = f"<li><span class='solved'>{middle}</span> <strong>{puzzle.answer}</strong></li>"
		else:
			final = f"<li>{middle}</li>"
		output.append(final)
	
	output.append("</ol>")

	return "\n".join(output)