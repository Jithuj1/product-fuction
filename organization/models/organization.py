from django.db import models
from django.utils.translation import gettext_lazy as _


# custom user model.
class Organization(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(
        _("name"),
        max_length=254,
        help_text=_("Required. 254 characters or fewer."),
    )
    status = models.IntegerField(
        _("status"),
        default=0,
        help_text=_("User status."),
    )
    personal = models.BooleanField(
        _("personal"),
        default=False,
        null=True,
        help_text=_("Personal user."),
    )
    settings = models.JSONField(
        _("settings"),
        default=dict,
        null=True,
        help_text=_("JSON field for user settings."),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")
        default_permissions = ()
        permissions = (
            ("add_organization", "Create organization"),
            ("view_organization", "View organization"),
            ("change_organization", "Update organization"),
            ("delete_organization", "Delete organization"),
        )

    