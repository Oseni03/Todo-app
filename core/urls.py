from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("to_do.urls"))
]

auth_urlpatterns = [
    path('auth/password-reset/', 
    auth_views.PasswordResetView.as_view(
      template_name="auth/reset_password.html"), 
      name="password_reset"),
    
    path('auth/reset-password-sent/', 
    auth_views.PasswordResetDoneView.as_view(
      template_name="auth/password_reset_sent.html"), 
      name="password_reset_done"),
    
    path('reset/<uidb64>/<token>/', 
    auth_views.PasswordResetConfirmView.as_view(
      template_name="auth/password_reset_confirm.html"), 
      name="password_reset_confirm"),
    
    path('auth/password-reset-complete/',
    auth_views.PasswordResetCompleteView.as_view(
      template_name="auth/password_reset_complete.html"),
      name="password_reset_complete"),
]


urlpatterns += auth_urlpatterns