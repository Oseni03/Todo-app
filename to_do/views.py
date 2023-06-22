from django.shortcuts import render
from django.views.decorators.http import require_POST 
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST 
from django.contrib import messages
from django.urls import reverse, reverse_lazy

from api.models import Task

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

class CreateUserView(generic.CreateView):
  template_name="accounts/register.html"


def login_view(request):
  if request.user.is_authenticated:
    return redirect(reverse("home"))
  return render(request, "accounts/login.html")

@login_required
def logout_view(request):
  logout(request)
  return redirect(reverse("core:home",))

