# local imports
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import NotAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from user.serializers.auth import (
    LoginSerializer,
    TokenRefreshSerializer
)
from utils.permissions import HasPermission
from user.serializers.auth import ChangePasswordSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from utils.permissions import IsNotAuthenticated


class LoginView(APIView):
    permission_classes = (IsNotAuthenticated,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(detail=serializer.errors)

        user = authenticate(request=request, **serializer.validated_data)
        if user is None:
            raise NotAuthenticated(detail="Invalid username or password")
        
        refresh_token = RefreshToken().for_user(user)
        access_token = refresh_token.access_token

        update_last_login(None, user)
        user.send_login_alert_email()

        resp_data = {
            "success": True,
            "data": {
                "access_token": str(access_token),
                "refresh_token": str(refresh_token),
                "user_data": {
                    "id": str(user.id),
                    "email": user.email,
                },
            },
        }
        return Response(resp_data, status=status.HTTP_200_OK)


class TokenRefreshView(APIView):
    permission_classes = (IsNotAuthenticated,)

    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(detail=serializer.errors)

        resp_data = {
            "success": True,
            "data": serializer.validated_data,
        }
        return Response(resp_data, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = (HasPermission,)

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(detail=serializer.errors)

        current_password = serializer.validated_data.get("current_password")
        new_password = serializer.validated_data.get("new_password")

        request.user.change_password(
            new_password=new_password, current_password=current_password
        )

        resp_data = {"success": True, "data": {}}
        return Response(resp_data, status=status.HTTP_200_OK)