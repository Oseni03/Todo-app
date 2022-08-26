from django import forms
from django.contrib.auth.models import User

from .models import Task

class RegisterForm(forms.ModelForm):
  password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={"class": "form-control"}))
  
  class Meta:
    model = User 
    fields = ("username", "first_name", "last_name", "email", "password", "password2")
    
    widgets = {
      "username ": forms.TextInput(attrs={"class": "form-control"}),
      'first_name': forms.TextInput(attrs={"class": "form-control"}), 
      'last_name': forms.TextInput(attrs={"class": "form-control"}), 
      'email': forms.EmailInput(attrs={"class": "form-control"}), 
      'password': forms.PasswordInput(attrs={"class": "form-control"}),
      'password2': forms.PasswordInput(attrs={"class": "form-control"}),
    }


class LoginForm(forms.Form):
  username = forms.CharField(max_length=25, widget=forms.TextInput(attrs={"class": "form-control"}))
  password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
  remember_me = forms.BooleanField(required= False, widget=forms.CheckboxInput())


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("name",)
        labels = {
            "name": "Add new task:",
        }