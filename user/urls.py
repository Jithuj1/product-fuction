from user.views.user import UserSignUpView, UserRoleListView, InviteEmailView
from user.views.auth import LoginView, TokenRefreshView, ChangePasswordView
from django.urls import path

urlpatterns = [
    path("signup/", UserSignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("role-wise-users/", UserRoleListView.as_view(), name="role-wise-users"),
    path("invite-email/", InviteEmailView.as_view(), name="invite-email"),
]