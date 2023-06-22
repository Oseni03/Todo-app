from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("to_do.urls", namespace="core")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("api/", include("api.urls", namespace="api")),
]
