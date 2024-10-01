from django.urls import path
from organization.views.organization import (
    OrganizationMemberDeleteView, 
    UpdateMemberRoleView, 
    OrgWiseMemberListView, 
    OrgWiseRoleWiseMemberListView
)

urlpatterns = [
    path(
        "member/<str:member_id>/",
        OrganizationMemberDeleteView.as_view(),
        name="delete-organization-member"
    ),
    path(
        "member/<str:member_id>/update-role/",
        UpdateMemberRoleView.as_view(),
        name="update-member-role"
    ),
    path(
        "org-user-list/",
        OrgWiseMemberListView.as_view(),
        name="org-user-list"
    ),
    path(
        "org-role-wise-user-list/",
        OrgWiseRoleWiseMemberListView.as_view(),
        name="org-role-wise-user-list"
    )
]
