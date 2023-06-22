from rest_framework import routers
from . import views 

app_name = "api"

router = routers.DefaultRouter(trailing_slash=False)
router.register("tasks", views.TaskViewset, basename="tasks")

urlpatterns = router.urls