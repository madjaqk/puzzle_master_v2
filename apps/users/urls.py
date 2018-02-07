from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
	path("", views.login_page, name="login_page"),
	path("register", views.register, name="register"),
	path("login", views.login_user, name="login"),
	path("logout", views.logout_user, name="logout"),
	path("settings", views.settings, name="settings"),
	path("password", views.password, name="password"),
	path("privacy", views.privacy, name="privacy"),
]