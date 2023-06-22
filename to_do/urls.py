from django.urls import path, include
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    
    path("add-task/", views.add_task, name="add_task"),
    path("<int:task_id>/complete-task", views.complete_task, name="complete_task"),
    path("<int:task_id>/delete-task", views.delete_task, name="delete-task"),
]
