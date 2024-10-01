from django.db import models
from django.utils.translation import gettext_lazy as _

# custom role model.
class Role(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(
        _("name"),
        max_length=254,
        help_text=_("Required. 254 characters or fewer."),
        null=False,
    )
    description = models.CharField(
        _("description"),
        max_length=254,
        help_text=_("Optional. 254 characters or fewer."),
        null=True,
    )
    org_id = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        null=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")
        default_permissions = ()
        permissions = (
            ("add_role", "Create role"),
            ("view_role", "View role"),
            ("change_role", "Update role"),
            ("delete_role", "Delete role"),
        )
