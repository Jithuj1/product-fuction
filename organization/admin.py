from django.contrib import admin
from organization.models import Organization
from organization.models import Member

admin.site.register(Organization)
admin.site.register(Member)
