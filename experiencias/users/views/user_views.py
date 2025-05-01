from django.shortcuts import render
from users.serializers import UserSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema




# Create your views here.

@extend_schema(
    summary="Register a new user",
    description="Create a new user account with the provided details.",
    tags=["Users"]
)
class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        print(serializer.data)
        return Response(
            {"message": "User created successfully"},
            status=status.HTTP_201_CREATED,
            headers=headers
        )
