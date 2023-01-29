import re

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse


class PuzzleSetManager(models.Manager):
	def get_by_natural_key(self, name):
		return self.get(name=name)

class PuzzleSet(models.Model):
	name = models.CharField(max_length=200)
	folder = models.CharField(max_length=100)
	description = models.TextField(null=True, blank=True, default=None)
	top_level_puzzle = models.OneToOneField("Puzzle", on_delete=models.CASCADE, null=True, blank=True, default=None)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = PuzzleSetManager()

	def __str__(self):
		return self.name

	def natural_key(self):
		return (self.name,)


class PuzzleManager(models.Manager):
	def get_by_natural_key(self, short_name):
		return self.get(short_name=short_name)

class Puzzle(models.Model):
	name = models.CharField(max_length=200)
	short_name = models.CharField(max_length=100)
	answer = models.TextField()
	meta_order = models.SmallIntegerField(null=True, blank=True, default=None)
	metapuzzles = models.ManyToManyField("self", symmetrical=False, related_name="feeder_puzzles", blank=True)
	puzzle_set = models.ForeignKey(PuzzleSet, on_delete=models.CASCADE, related_name="puzzles")

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = PuzzleManager()

	def __str__(self):
		return f"<ID: {self.id}, puzzle: {'***' if self.feeder_puzzles.exists() else ''}{self.name}{'***' if self.feeder_puzzles.exists() else ''}, answer: {self.answer}>"

	def natural_key(self):
		return (self.short_name,)

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

	def __str__(self):
		return f"<User: {self.user}, Puzzle: {self.puzzle.name}, Answer: {self.answer}, {'CORRECT' if self.correct else 'INCORRECT'}>"

	@property
	def correct(self):
		return self.answer == self.puzzle.answer
