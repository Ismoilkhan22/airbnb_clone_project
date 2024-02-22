from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .permissions import IsUser, IsAdmin
from .serializer import GoogleSocialAuthSerializer, LogoutSerializer, UserSerializer


class GoogleSocialAuthView(GenericAPIView):
    serializer_class = GoogleSocialAuthSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        """

        POST with "auth_token"

        Send an idtoken as from google to get user information

        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserView(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsUser)

    def get(self, request):
        email = request.user.email
        user = User.objects.filter(email=email)
        if not user:
            return Response({
                "error": "User not found"
            })
        else:
            serializer = UserSerializer(user)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


























