import re

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse

class Puzzle(models.Model):
	name = models.CharField(max_length=200)
	short_name = models.CharField(max_length=100)
	description = models.TextField(null=True, blank=True, default=None)
	show_on_main_page = models.BooleanField(default=False)
	answer = models.TextField()
	meta_order = models.SmallIntegerField(null=True, blank=True, default=None)
	metapuzzles = models.ManyToManyField("self", symmetrical=False, related_name="feeder_puzzles", blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"<Puzzle: {'***' if self.show_on_main_page else ''}{self.name}{'***' if self.show_on_main_page else ''}, answer={self.answer}>"

	@property
	def sort_order(self):
		if self.meta_order is not None:
			return self.meta_order
		else:
			return re.sub("^(THE|A|AN) ", "", self.name.upper())

	def solved_by_user(self, user):
		if not user.is_authenticated:
			return False

		return PuzzleAnswer.objects.filter(puzzle=self, user=user, answer=self.answer).exists()

@receiver(pre_save, sender=Puzzle)
def standardize_answer(sender, instance, *args, **kwargs):
	instance.answer = re.sub(r"[^A-Z]", "", instance.answer.upper())

class PuzzleAnswer(models.Model):
	answer = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="puzzle_answers")
	puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE, related_name="submitted_answers")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	@property
	def correct(self):
		return self.answer == self.puzzle.answer