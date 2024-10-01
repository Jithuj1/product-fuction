from django.contrib.auth import get_user_model
from rest_framework import serializers
from organization.serializers.organization import OrganizationSerializer
from user.models.user import AppUser
from user.models.role import Role
from organization.models.organization import Organization
from organization.models.member import Member
from django.db import transaction

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AppUser
        fields = (
            "email",
            "password",
            "profile",
            "status",
            "settings",
        )
        extra_kwargs = {
            "profile": {"required": True},
            "status": {"required": True},
        }

class MemberRoleSerializer(serializers.Serializer):
    role_name = serializers.CharField(required=True)
    role_description = serializers.CharField(required=False)
    manager_status = serializers.IntegerField(required=False)
    settings = serializers.JSONField(required=False)



class UserSignUpSerializer(serializers.Serializer):
    user = UserSerializer(required=True)
    organization = OrganizationSerializer(required=True)
    member_role = MemberRoleSerializer(required=True)
    

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        organization_data = validated_data.pop("organization")
        member_role_data = validated_data.pop("member_role")
        role_name = member_role_data.get("role_name")
        
        try:
            with transaction.atomic():
                """ the issue is not clear so I am not sure about the exact requirement
                currently creating user and organization directly and checking if the 
                role is exists then updating the details else creating new role 
                if the organization name is unique then it will more structured"""
                
                password = user_data.pop("password")
                user = AppUser.objects.create(**user_data)
                user.set_password(password)
                user.save()

                organization = Organization.objects.create(**organization_data)

                role_obj = Role.objects.filter(name=role_name).first()
                if role_obj:
                    # if role then updating details of organization and related things 
                    role_obj.description = member_role_data.get("role_description")
                    role_obj.settings = member_role_data.get("settings")
                    role_obj.org_id = organization
                    role_obj.save()
                else:
                    role_obj = Role.objects.create(
                        name=role_name,
                        description=member_role_data.get("role_description"),
                        org_id=organization,
                    )

                member = Member.objects.create(
                    user_id=user, 
                    org_id=organization, 
                    role_id=role_obj,
                    status=member_role_data.get("manager_status"),
                    settings=member_role_data.get("settings"),
                    )
            
        except Exception as e:
            raise serializers.ValidationError(f"Error creating role: {e}")

        return True
    


class UserRoleListSerializer(serializers.ModelSerializer):
    user_count = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = (
            "id",
            "name",
            "organization",
            "user_count",
        )

    def get_user_count(self, obj):
        return Member.objects.filter(role_id=obj.id).count()
    
    def get_organization(self, obj):
        return obj.org_id.name


class InviteEmailUserSerializer(serializers.Serializer):
    send_to = serializers.EmailField(required=True)
    subject = serializers.CharField(required=True)
    recipient_name = serializers.CharField(required=True)
    sender_name = serializers.CharField(required=True)

