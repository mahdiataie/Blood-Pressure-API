from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .models import CustomUser
from .serializer import UserRegistrationSerializer


class UserRegistrationView(CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Custom success message
        success_message = "User registration successful."

        return Response(
            {"success": success_message},
            status=status.HTTP_201_CREATED
        )
    permission_classes = (AllowAny,)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        # Include user name and user type in the response data
        response_data = {
            'token': token.key,
            'user_name': user.email,
            'user_type': user.user_type,
        }
        return Response(response_data, status=status.HTTP_200_OK)
