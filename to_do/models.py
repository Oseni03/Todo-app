from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Create your models here
class Task(models.Model):
    user = models.ForeignKey(
        User, related_name="tasks", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=250)
    done = models.BooleanField(default=False)
  
    class Meta:
        ordering = ["name"] 
    
    def __str__(self):
        return self.name