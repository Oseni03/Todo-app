from django.shortcuts import render
from django.conf import settings 
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, DjangoUnicodeDecodeError, force_bytes
from django.utils.http import urlsafe_base64_decode

from rest_framework import generics 
from rest_framework import status 
from rest_framework import permissions 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken 

from .serializers import (
    UserSerializer, LoginSerializer, 
    PasswordResetSerializer, 
    RequestPasswordResetSerializer)
from .renderers import CustomRenderer

import jwt

# Create your views here.
class UserCreationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer 
    permission_classes = [permissions.AllowAny]
    # renderer_classes = (CustomRenderer,)


class EmailVerificationView(generics.GenericAPIView):
    
    def get(self, request, token):
        try:
            # payload = jwt.decode(token, settings.SECRET_KEY) # OR

            payload = AccessToken(token)
            
            user = get_object_or_404(User, id=payload["user_id"])
            user.is_active=True 
            user.save()
            return Response({"message": "email verified"}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as exception:
            return Response(
                {"error": "Activation link expired"}, 
                status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as exception:
            return Response(
                {"error": "Invalid Token"}, 
                status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(generics.GenericAPIView):
    
    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"error": "Token is not valid, please request a new one!"}, status=status.HTTP_401_UNAUTHORIZED)
            data = {
                "data": UserSerializer(user).data,
                "uidb64": uidb64,
                "token": token,
            }
            return Response(data, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as exception:
            return Response({"error": "Token expired!"}, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordReset(generics.GenericAPIView):
    serializer_class = RequestPasswordResetSerializer 
    
    def post(self, request):            
        serializer = self.serializer_class(data=request.data, context={'request': request})
        # import pdb 
        # pdb.set_trace()
        serializer.is_valid(raise_exception=True)
        
        return Response({"success": "Password reset link is sent to your email"}, status=status.HTTP_200_OK)


class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer 
    
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"data": serializer.data}, status=status.HTTP_202_ACCEPTED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer 
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get("username")
        user = User.objects.get(username=username)
        serializer = UserSerializer(user)
        # import pdb 
        # pdb.set_trace()
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"data": "User logout successful!"}, status=status.HTTP_200_OK)


def check_email(request):
  email = request.POST.get("email")
  if get_user_model().objects.filter(email=email):
    return HttpResponse("<div style='color: red;'>This email already exit</div>")
  else:
    return HttpResponse("<div style='color: green;'>Available</div>")


def check_password(request):
  password = request.POST.get("password")
  password2 = request.POST.get("password2")
  if password != password2:
    return HttpResponse("<div style='color: red;'>Password not match</div>")
  else:
    return HttpResponse("<div style='color: green;'>Password match</div>")


def check_register_username(request):
  username = request.POST.get("username")
  if get_user_model().objects.filter(username=username):
    return HttpResponse("<div style='color: red;'>This username already exit</div>")
  else:
    return HttpResponse("<div style='color: green;'>Available</div>")


def check_username(request):
  username = request.POST.get("username")
  if get_user_model().objects.filter(username=username).exists():
    return HttpResponse("")
  else:
    return HttpResponse("<div style='color: red;'>This user does not exit</div>")
