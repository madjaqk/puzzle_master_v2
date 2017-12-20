import re

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Metapuzzle(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField()
	templates_folder = models.CharField(max_length=100)
	answer = models.TextField()

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"<Metapuzzle: {self.name}, answer={self.answer}>"

class Puzzle(models.Model):
	name = models.CharField(max_length=200)
	short_name = models.CharField(max_length=100)
	answer = models.TextField()
	meta_order = models.SmallIntegerField(null=True, blank=True, default=None)
	metapuzzle = models.ForeignKey(Metapuzzle, on_delete=models.CASCADE, related_name="puzzles")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"<Puzzle: {self.name}, answer={self.answer}>"

	def sort_order(self):
		if self.meta_order is not None:
			return self.meta_order
		else:
			return re.sub("^(THE|A|AN) ", "", self.name.upper())

@receiver(pre_save, sender=Metapuzzle)
@receiver(pre_save, sender=Puzzle)
def standardize_answer(sender, instance, *args, **kwargs):
	instance.answer = re.sub(r"[^A-Z]", "", instance.answer.upper())