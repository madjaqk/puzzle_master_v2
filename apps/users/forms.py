from django import forms
from django.contrib.auth.forms import AuthenticationForm

class MyAuthenticationForm(AuthenticationForm):
	"""Basically the same as the built-in, but with a different ID on the username field so that I can put both this and a UserCreationForm on the same template.
	"""
	username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={"id": "authentication_username", "autofocus": True}))