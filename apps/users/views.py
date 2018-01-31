from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import MyAuthenticationForm

def login_page(request):
	# if request.method == "GET":
	context = {
		"register_form": UserCreationForm(),
		"login_form": MyAuthenticationForm()
	}
	return render(request, "users/login.html", context)

def register(request):
	if request.method != "POST":
		return redirect("users:login_page")

	form = UserCreationForm(request.POST)
	if form.is_valid():
		form.save()
		username = form.cleaned_data.get("username")
		raw_password = form.cleaned_data.get("password1")
		user = authenticate(username=username, password=raw_password)
		login(request, user)
		return redirect("puzzles:index") # Change this back to puzzles:index !!!
	else:
		for field, errors in form.errors.get_json_data().items():
			for error in errors:
				messages.error(request, error["message"])

	return redirect("users:login_page")

def login_user(request):
	if request.method != "POST":
		return redirect("users:login_page")

	user = authenticate(username=request.POST["username"], password=request.POST["password"])

	if user is not None:
		login(request, user)
		return redirect("puzzles:index")
	else:
		messages.error(request, "Username or password incorrect")
		return redirect("users:login_page")

def logout_user(request):
	logout(request)
	return redirect("users:login_page")