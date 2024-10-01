from django.contrib import admin
from user.models import AppUser
from user.models import Role

admin.site.register(AppUser)
admin.site.register(Role)
