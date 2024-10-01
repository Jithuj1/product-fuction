from django.db import models
from django.utils.translation import gettext_lazy as _

# custom member model.
class Member(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    org_id = models.ForeignKey(
        'organization.Organization',
        on_delete=models.CASCADE,
        null=False,
        help_text=_("Organization ID."),
    )
    user_id = models.ForeignKey(
        'user.AppUser',
        on_delete=models.CASCADE,
        null=False,
        help_text=_("User ID."),
    )
    role_id = models.ForeignKey(
        'user.Role',
        on_delete=models.CASCADE,
        null=False,
        help_text=_("Role ID."),
    )
    status = models.IntegerField(
        _("status"),
        default=0,
        null=False,
        help_text=_("Member status."),
    )
    settings = models.JSONField(
        _("settings"),
        default=dict,
        null=True,
        help_text=_("JSON field for member settings."),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Member")
        verbose_name_plural = _("Members")
        default_permissions = ()
        permissions = (
            ("add_member", "Create member"),
            ("view_member", "View member"),
            ("change_member", "Update member"),
            ("delete_member", "Delete member"),
        )