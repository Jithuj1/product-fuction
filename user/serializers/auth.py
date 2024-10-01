from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password


USER = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        data["username"] = data.get("username").lower()
        return data


class TokenRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs.pop("refresh_token")

        try:
            refresh_obj = RefreshToken(refresh_token)
        except Exception:
            raise serializers.ValidationError(
                {"refresh_token": "Token is invalid or expired"}
            )

        user = USER.objects.get(id=refresh_obj.payload.get("user_id"))

        data = (
            {
                "access_token": str(refresh_obj.access_token),
                "user_data": {
                    "id": str(user.id),
                    "email": user.email,
                },
            },
        )

        return data


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate_new_password(self, new_password):
        validate_password(new_password)

        return new_password