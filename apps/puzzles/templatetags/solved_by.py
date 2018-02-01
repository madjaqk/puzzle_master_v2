from django import template

register = template.Library()

@register.filter
def solved_by(puzzle, user):
	return puzzle.solved_by_user(user)