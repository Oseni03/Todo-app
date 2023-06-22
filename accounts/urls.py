from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

app_name = "accounts"

urlpatterns = [
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("register", views.UserCreationView.as_view(), name="register"),
    path("verify-email/<token>", views.EmailVerificationView.as_view(), name="verify-email"),
    path('password-change', views.RequestPasswordReset.as_view(),name="password_change"),
    path('reset/<uidb64>/<token>', views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password-reset', views.PasswordResetView.as_view(),name="password_reset"),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # path("check-username/", views.check_username, name="check-ursername"),
    # path("check-register_username/", views.check_register_username, name="check-register_username"),
    # path("check-email/", views.check_email, name="check-email"),
    # path("check-password/", views.check_password, name="check-password"),
    
]