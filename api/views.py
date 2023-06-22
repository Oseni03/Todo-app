from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status 
from rest_framework.decorators import api_view, throttle_classes, action
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAdminUser)
from rest_framework.decorators import permission_classes
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .serializers import TaskSerializer
from .models import Task
from .permissions import IsOwner


# Create your views here.
class TaskViewset(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    serializer_class = TaskSerializer 
    # permission_classes = (IsOwner,)
    
    def get_queryset(self):
        return Task.objects.prefetch_related("user").filter(user=self.request.user)