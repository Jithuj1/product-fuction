from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError
from utils.email import EmailSender


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Normal user creation.
        Returns: User instance
        """
        if not email:
            raise ValueError(_("The Email must be set"))

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Superuser creation.
        Returns User instance
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


# custom user model.
class AppUser(AbstractBaseUser, PermissionsMixin):
    # Default Fields
    # AbstractBaseUser: password and last_login.
    # PermissionsMixin: is_superuser, groups and user_permissions.

    id = models.AutoField(primary_key=True, editable=False)
    email = models.EmailField(
        _("email address"),
        unique=True,
        help_text=_("Required. 254 characters or fewer."),
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    password = models.CharField(
        _("password"),
        max_length=128,
        help_text=_("Required. 128 characters or fewer."),
    )
    profile = models.JSONField(
        _("profile"),
        default=dict,
        help_text=_("JSON field for user profile."),
    )
    status = models.IntegerField(
        _("status"),
        default=0,
        help_text=_("User status."),
    )
    settings = models.JSONField(
        _("settings"),
        default=dict,
        null=True,
        help_text=_("JSON field for user settings."),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='appuser_groups',  # Changed related_name to avoid conflict
        blank=True,
        help_text=_("The groups this user belongs to."),
        verbose_name=_("groups"),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='appuser_user_permissions',  # Changed related_name to avoid conflict
        blank=True,
        help_text=_("Specific permissions for this user."),
        verbose_name=_("user permissions"),
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = UserManager()
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        default_permissions = ()
        permissions = (
            ("add_user", "Create user"),
            ("view_user", "View user"),
            ("change_user", "Update user"),
            ("delete_user", "Delete user"),
        )

    def change_password(self, new_password, current_password=None):
        """
        Raises Errors if needed and Updates the password of user.
        Returns None
        """
        if current_password:
            if self.check_password(current_password) is False:
                raise ValidationError({"current_password": "Wrong Password, Try Again"})
            if current_password == new_password:
                raise ValidationError(
                    {"new_password": "Current and New passwords cannot be same"}
                )

        self.set_password(new_password)
        self.save()
        email = EmailSender()
        email.send_email(self.email, "Password Changed", "Your password has been successfully changed.")

    def send_login_alert_email(self):
        email = EmailSender()
        email.send_email(
            self.email, 
            "Login Alert", 
            "Your account has been logged in from a new device."
        )
        


