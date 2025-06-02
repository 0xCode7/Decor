from logging import raiseExceptions

from .serializer import RegisterSerializer
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({
                "errors": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        return Response({
            "user": RegisterSerializer(user).data,
            'token': str(access_token)
        }, status=status.HTTP_201_CREATED)
