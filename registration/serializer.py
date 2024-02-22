import os

from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import User
from . import google
from google.oauth2 import id_token
from google.auth.transport import requests

from .register import register_social_user


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        auth_token = attrs['auth_token']
        try:
            idinfo = id_token.verify_oauth2_token(auth_token, requests.Request())
            if 'accounts.google.com' not in idinfo['iss']:
                raise ValidationError('not found')

        except Exception as e:

            raise ValidationError(str(e))
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except Exception as e:
            raise serializers.ValidationError(str(e))

        if user_data['aud'] != os.environ.get('GOOGLE_CLIENT_ID'):
            raise AuthenticationFailed('oops, who are you?')
        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'
        user, created = User.objects.get_or_create(email=email)
        if created:
            user.provider = provider
            user.set_unusable_password()
            user.save()
        attrs['refresh'], attrs['access'] = user.tokens()
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'user_type')

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['user_type'] = 'User' if res['user_type'] == 2 else 'Admin'
        return res


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')
