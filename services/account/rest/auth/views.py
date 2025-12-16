from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from services.account.rest.user.serializers import ProfileSerializer
from services.transaction.models.token import TokenTransaction

from .serializers import RegisterSerializer, TokenObtainPairSerializer

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)

__all__ = (
    "profile",
    "LoginView",
    "RefreshView",
)


@swagger_auto_schema(
    method="get",
    tags=["User"],
    operation_id="profile",
    operation_description="Retrieve current user profile",
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def profile(request):
    """
    Retrieve the profile of the currently authenticated user.
    """
    user = request.user
    serializer = ProfileSerializer(user)
    return Response(serializer.data)


class LoginView(TokenObtainPairView):
    """
    Login endpoint that returns JWT access and refresh tokens.
    """

    permission_classes = (AllowAny,)
    serializer_class = TokenObtainPairSerializer

    @swagger_auto_schema(
        tags=["Auth"],
        operation_id="login",
        operation_description="Login endpoint that returns JWT access and refresh tokens.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RefreshView(TokenRefreshView):
    """
    Refresh endpoint that returns a new JWT access token using a refresh token.
    """

    permission_classes = (AllowAny,)
    serializer_class = TokenRefreshSerializer

    @swagger_auto_schema(
        tags=["Auth"],
        operation_id="refresh_token",
        operation_description="Refresh endpoint that returns a new JWT access token using a refresh token.",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        tags=["Auth"],
        operation_id="register",
        operation_description="Register a new user account and return JWT tokens.",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save user (create)
        user = serializer.save()

        # generate token for first register = 50 token
        TokenTransaction.objects.create(
            user=user,
            amount=50,
            type=TokenTransaction.Choices.GIFT,
            note=f"Rewards for registering #{user.username}",
        )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        access["is_superuser"] = user.is_superuser

        return Response(
            {
                "refresh": str(refresh),
                "access": str(access),
            },
            status=status.HTTP_201_CREATED,
        )
