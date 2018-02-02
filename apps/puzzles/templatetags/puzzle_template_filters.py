from django import template
from django.urls import reverse

register = template.Library()

@register.filter
def solved_by(puzzle, user):
	return puzzle.solved_by_user(user)

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