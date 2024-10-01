from utils.permissions import HasPermission
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from organization.models.member import Member
from organization.models.organization import Organization
from organization.serializers.organization import (
    RoleGetSerializer, 
    OrgWiseMemberListSerializer, 
    OrgWiseRoleWiseMemberListSerializer
)
from rest_framework.exceptions import ValidationError
from utils.pagination import CustomPagination
from datetime import datetime
from django.db.models import Q


class OrganizationMemberDeleteView(APIView):
    permission_classes = (HasPermission,)
    # permission_dict = {"POST": ["add_organization"]}

    def delete(self, request, member_id):
        member_obj = get_object_or_404(Member, id=member_id)
        member_obj.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class UpdateMemberRoleView(APIView):
    permission_classes = (HasPermission,)
    # permission_dict = {"post": ['change_member']}

    def put(self, request, member_id):
        member_obj = get_object_or_404(Member, id=member_id)

        serializer = RoleGetSerializer(
            data=request.data, context={"org_id": member_obj.org_id}
        )

        if not serializer.is_valid():
            raise ValidationError(detail=serializer.errors)

        role_obj = serializer.save()
        member_obj.role_id = role_obj
        member_obj.save()

        return Response(
            {"success": True, "data": "",}, 
            status=status.HTTP_201_CREATED
        )
    

class OrgWiseMemberListView(APIView):
    permission_classes = (HasPermission,)
    # permission_dict = {"get": ["view_organization"]}

    def get(self, request):
        q_object = Q()
        date_range = request.GET.get("date_range")
        from_to_date = date_range.split("|")

        try:
            start_date = datetime.strptime(from_to_date[0], "%Y-%m-%d")
            end_date = datetime.strptime(from_to_date[1], "%Y-%m-%d")
            q_object.add(Q(
                created_at__gte=start_date, created_at__lte=end_date), Q.AND)

        except ValueError:
            raise ValidationError(
                {"date_range": "Please provide dates in YYYY-MM-DD format"}
            )

        all_organizations = Organization.objects.filter(q_object)

        paginator = CustomPagination()  
        page = paginator.paginate_queryset(all_organizations, request)

        serializer = OrgWiseMemberListSerializer(page, many=True)

        response = paginator.get_paginated_response(
            object_name="organizations", data=serializer.data
        )
        return response
    

class OrgWiseRoleWiseMemberListView(APIView):
    permission_classes = (HasPermission,)
    # permission_dict = {"get": ["view_organization"]}

    def get(self, request):
        q_object = Q()
        date_range = request.GET.get("date_range")
        from_to_date = date_range.split("|")

        if date_range != "":
            try:        
                start_date = datetime.strptime(from_to_date[0], "%Y-%m-%d")
                end_date = datetime.strptime(from_to_date[1], "%Y-%m-%d")
                q_object.add(Q(created_at__gte=start_date, created_at__lte=end_date), Q.AND)
    
            except ValueError:
                raise ValidationError(
                    {"date_range": "Please provide dates in YYYY-MM-DD format"}
                )
        
        all_organizations = Organization.objects.filter(q_object)

        paginator = CustomPagination()
        page = paginator.paginate_queryset(all_organizations, request)

        serializer = OrgWiseRoleWiseMemberListSerializer(page, many=True)

        response = paginator.get_paginated_response(
            object_name="organizations", data=serializer.data
        )
        return response