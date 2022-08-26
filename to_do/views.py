from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET 
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic

from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm
from .models import Task

# Create your views here.
def home(request):
  if request.user.is_authenticated:
    tasks = Task.objects.filter(user=request.user)
  else:
    tasks = None
  context = {
    "tasks": tasks,
  }
  return render(request, "to_do/home.html", context)


class CreateUserView(SuccessMessageMixin, generic.CreateView):
  template_name="auth/register.html"
  form_class=RegisterForm
  model=User 
  success_url="login/"
  
  def form_invalid(self, form):
    result = super(CreateUserView, self).form_invalid(form)
    for error in form.errors:
        messages.error(self.request, error)
    return result

  def form_valid(self, form):
    user = form.save(commit=False)
    user.set_password(user.password)
    user.save()
    return super(CreateUserView, self).form_valid(form) 


def login_view(request):
  if request.user.is_authenticated:
    return redirect(reverse("home"))
  form = LoginForm()
  if request.method == "POST":
    form = LoginForm(request.POST)
    if form.is_valid():
      username = form.data["username"]
      password = form.data["password"]
      user = authenticate(username=username, password=password)
      if user:
        if user.is_active:
          messages.success(request, 'Login successful.')
          login(request, user)
          return redirect(reverse("home",))
      else:
        messages.info(request, "Invalid login credentials")
    elif form.errors:
      for error in form.errors:
        messages.error(request, error)
  context= {
    "form": form,
  }
  return render(request, "auth/login.html", context)


@login_required
def logout_view(request):
  logout(request)
  return redirect(reverse("home",))


@require_POST
def check_username(request):
  username = request.POST.get("username")
  if get_user_model().objects.filter(username=username):
    return HttpResponse("")
  else:
    return HttpResponse("<div style='color: red;'>This user does not exit</div>")


@require_POST
def check_register_username(request):
  username = request.POST.get("username")
  if get_user_model().objects.filter(username=username):
    return HttpResponse("<div style='color: red;'>This username already exit</div>")
  else:
    return HttpResponse("<div style='color: green;'>Available</div>")


@require_POST
def check_email(request):
  email = request.POST.get("email")
  if get_user_model().objects.filter(email=email):
    return HttpResponse("<div style='color: red;'>This email already exit</div>")
  else:
    return HttpResponse("<div style='color: green;'>Available</div>")


@require_POST
def check_password(request):
  password = request.POST.get("password")
  password2 = request.POST.get("password2")
  if password != password2:
    return HttpResponse("<div style='color: red;'>Password not match</div>")
  else:
    return HttpResponse("<div style='color: green;'>Password match</div>")


@require_POST
def add_task(request):
  taskname = request.POST.get("taskname")
  if len(taskname) > 1:
    task = Task.objects.create(name=taskname, user=request.user)
    task.save()
  
  tasks = Task.objects.filter(user=request.user)
  context = {
    "tasks": tasks,
  }
  return render(request, "to_do/partials/tasks.html", context)


def complete_task(request, task_id):
  task = Task.objects.get(id=task_id)
  if task.done == True:
    task.done = False 
  else:
    task.done = True 
  task.save()
  
  tasks = Task.objects.filter(user=request.user)
  context = {
    "tasks": tasks,
  }
  return render(request, "to_do/partials/tasks.html", context)


def delete_task(request, task_id):
  Task.objects.filter(id=task_id).delete()
  tasks = Task.objects.filter(user=request.user)
  context = {
    "tasks": tasks,
  }
  return render(request, "to_do/partials/tasks.html", context)
