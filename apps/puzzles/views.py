from django.shortcuts import render, redirect, get_object_or_404

from .models import Metapuzzle, Puzzle

def index(request):
	# More code here
	return render(request, "puzzles/index.html", {"metas": Metapuzzle.objects.all()})

def show_meta(request, meta_id):
	meta = get_object_or_404(Metapuzzle, id=meta_id)
	return render(request, "puzzles/show_meta.html", {"meta": meta})