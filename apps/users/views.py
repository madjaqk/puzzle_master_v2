from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from social_django.models import UserSocialAuth

from .forms import MyAuthenticationForm

def login_page(request):
	oauth_buttons = [
		("facebook", "users/img/facebook_login.png"),
		("twitter", "users/img/sign-in-with-twitter-gray.png"),
		("github", "users/img/GitHub_Logo.png"),
	]

	context = {
		"register_form": UserCreationForm(),
		"login_form": MyAuthenticationForm(),
		"oauth_buttons": oauth_buttons
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

@login_required
def settings(request):
	user = request.user

	other_sites = ["github", "twitter", "facebook"]
	other_site_logins = []

	for site in other_sites:
		try:
			other_site_logins.append(user.social_auth.get(provider=site))
		except UserSocialAuth.DoesNotExist:
			other_site_logins.append(None)

	context = {f"{site}_login": site_login for site, site_login in zip (other_sites, other_site_logins)}

	context["can_disconnect"] = user.social_auth.count() > 1 or user.has_usable_password()

	return render(request, "users/settings.html", context)

@login_required
def password(request):
	if request.user.has_usable_password():
		PasswordForm = PasswordChangeForm
	else:
		PasswordForm = AdminPasswordChangeForm

	if request.method == "POST":
		form = PasswordForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, "Your password was successfully updated!")
		else:
			for field, errors in form.errors.get_json_data().items():
				for error in errors:
					messages.error(request, error["message"])

		return redirect("users:password")
	else:
		form = PasswordForm(request.user)

	return render(request, "users/password.html", {"form": form})

def privacy(request):
	return render(request, "users/privacy.html")