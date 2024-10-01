from organization.models.organization import Organization
from rest_framework import serializers
from user.models.role import Role
from organization.models.member import Member


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = (
            "name",
            "status",
            "personal",
            "settings",
        )


class RoleGetSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False)

    def create(self, validated_data):
        name = validated_data.get("name")
        org_id = self.context.get("org_id")

        role_obj = Role.objects.filter(name=name, org_id=org_id).first()

        if role_obj:
            role_obj.description = validated_data.get("description")
            role_obj.save()
        else:
            role_obj = Role.objects.create(
                name=name, 
                description=validated_data.get("description"),
                org_id=org_id
            )

        return role_obj


class OrgWiseMemberListSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "status",
            "personal",
            "settings",
            "member_count",
        )

    def get_member_count(self, obj):
        return Member.objects.filter(org_id=obj.id).count()



class OrgRoleSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    class Meta:
        model = Role
        fields = (
            "id",
            "name",
            "description",
            "member_count",
        )

    def get_member_count(self, obj):
        return Member.objects.filter(
            role_id=obj.id, org_id=self.context.get("org_id")).count()


class OrgWiseRoleWiseMemberListSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "status",
            "personal",
            "settings",
            "role",
        )

    def get_role(self, obj):
        all_roles_in_org = Role.objects.filter(org_id=obj.id)
        serializer = OrgRoleSerializer(
            all_roles_in_org, many=True,
            context={"org_id": obj.id}
        )
        return serializer.data