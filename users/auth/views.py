import uuid

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.hashers import make_password
from django.utils import timezone

from datetime import timedelta

from .serializers import (
    RegisterSerializer,
    LoginUserSerializer,
)

from ..models import Users


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        data['username'] = str(uuid.uuid4())
        data['password'] = make_password(data['password'])

        user = Users.objects.create(
            **data
        )

        return Response(dict(
            user_id=user.id,
            status=status.HTTP_201_CREATED
        ))


class LoginUserAPIView(generics.CreateAPIView):
    permission_classes = ()
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        # Check user in order to login by email
        user = Users.objects.filter(
            email=data['email'],
            is_deleted=False
        ).first()

        if user:
            if user.check_password(data['password']):
                iat = timezone.now()
                exp = iat + timedelta(hours=1)
                token = RefreshToken.for_user(user)
                token = dict(
                    token=str(token.access_token),
                    refresh=str(token),
                    exp=str(exp),
                    iat=str(iat)
                )
                return Response(dict(
                    token=token
                ))
        raise ValidationError(dict(
            message="Email or password wrong."
        ))