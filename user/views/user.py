from user.serializers.user import UserSignUpSerializer, UserRoleListSerializer, InviteEmailUserSerializer
from rest_framework.serializers import ValidationError
from utils.permissions import HasPermission
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import Role
from utils.pagination import CustomPagination
from utils.email import EmailSender
from django.urls import reverse
from django.conf import settings


class UserSignUpView(APIView):
    permission_classes = (HasPermission,)
    permission_dict = {"post": ['add_user']}

    def post(self, request):
        serializer = UserSignUpSerializer(
            data=request.data, context={"request": request}
        )
        if not serializer.is_valid():
            raise ValidationError(detail=serializer.errors)

        serializer.save()

        return Response(
            {"success": True, "data": "", },
            status=status.HTTP_201_CREATED
        )


class UserRoleListView(APIView):
    permission_classes = (HasPermission,)
    permission_dict = {}

    def get(self, request):
        all_users = Role.objects.all()

        paginator = CustomPagination()
        page = paginator.paginate_queryset(all_users, request)

        serializer = UserRoleListSerializer(page, many=True)

        response = paginator.get_paginated_response(
            object_name="roles", data=serializer.data
        )
        return response


class InviteEmailView(APIView):
    permission_classes = (HasPermission,)
    # permission_dict = {"POST": ['add_user']}

    def post(self, request):
        serializer = InviteEmailUserSerializer(
            data=request.data, context={"request": request}
        )
        if not serializer.is_valid():
            raise ValidationError(detail=serializer.errors)

        recipient_name = serializer.data["recipient_name"]
        sender_name = serializer.data["sender_name"]

        link = settings.HOSTED_URL + reverse("signup")
        content = f"Hello {recipient_name}, You have been invited to join our platform by {
            sender_name} using the following link: {link}."

        email = EmailSender()
        response = email.send_email(
            serializer.data["send_to"],
            serializer.data["subject"],
            content
        )

        if response["success"]:
            return Response(response, status=status.HTTP_200_OK)
        else:
            raise ValidationError(detail=response["message"])
