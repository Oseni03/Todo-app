from django.db import models
from django.contrib.auth.models import User

# Create your models here
class Task(models.Model):
    user = models.ForeignKey(
        User, related_name="tasks", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=250)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
    class Meta:
        ordering = ["-updated_at"] 
    
    def __str__(self):
        return str(self.name)