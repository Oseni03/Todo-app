from django.urls import path, include
from django.views import generic
from django.contrib.auth.models import User
from . import views
from .forms import RegisterForm, LoginForm

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.CreateUserView.as_view(), name="register"),
    path("", views.home, name="home"),
]

htmx_url = [
  path("check-username/", views.check_username, name="check-ursername"),
  path("check-register_username/", views.check_register_username, name="check-register_username"),
  path("check-email/", views.check_email, name="check-email"),
  path("check-password/", views.check_password, name="check-password"),
  path("add-task/", views.add_task, name="add_task"),
  path("<int:task_id>/complete-task", views.complete_task, name="complete_task"),
  path("<int:task_id>/delete-task", views.delete_task, name="delete-task"),
]

urlpatterns += htmx_url