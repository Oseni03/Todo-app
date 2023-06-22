from rest_framework import serializers 
from rest_framework.reverse import reverse
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from django.conf import settings 
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField(method_name="get_tokens", read_only=True)
    
    class Meta:
        model = User 
        fields = ("id", "username", "first_name", "last_name", "email", "password", "tokens")
        
    def get_tokens(self, obj):
        refresh = RefreshToken.for_user(obj)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("User with this username already exist!")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email already exist!")
        return value
    
    def create(self, validated_data):
        request = self.context.get("request")
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.is_active = False
        user.save()
        
        token = RefreshToken.for_user(user).access_token
        absUrl = reverse('accounts:verify-email', kwargs={'token': token}, request=request)
        email_body = f"""
        Hi, {user.username}
        Use the link below to verify your email
        {absUrl}
        Thank You.
        """
        email_subject= "Verify your email"
        user.email_user(
            email_subject, 
            email_body, 
            settings.EMAIL_HOST_USER
        )
        return user


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate(self, data):
        
        # import pdb 
        # pdb.set_trace()
        user = get_object_or_404(User, email=data.get("email"))
        token = PasswordResetTokenGenerator().make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        absUrl = reverse(
            'accounts:password_reset_confirm', 
            kwargs={
                'token': token, 
                "uidb64": uidb64
            }, 
            request=self.context.get("request")
        )
        email_body = f"""
        Hi, {user.username}
        Use the link below to reset your password
        
        {absUrl}
        
        Thank You.
        """
        email_subject= "Forgotten password reset"
        user.email_user(
            email_subject, 
            email_body, 
            settings.EMAIL_HOST_USER
        )
        return data


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, min_length=6, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    
    def validate(self, data):
        password = data.get("password")
        token = data.get("token")
        uidb64 = data.get("uidb64")
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("Reset link not valid!", 401)
            user.set_password(serializer.data.get("password1"))
            user.save()
            return UserSerializer(user).data
        except:
            raise AuthenticationFailed("Reset link not valid!", 401)
        return super().validate(data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, write_only=True)
    password = serializers.CharField(max_length=255, min_length=6, write_only=True)
    
    
    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        
        user = authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials, try again!")
        if not user.is_active:
            raise AuthenticationFailed("Email not verified!")
        return data
    