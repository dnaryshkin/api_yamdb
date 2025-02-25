from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomizedUser

UserAdmin.fieldsets += (
    ('Роль', {'fields': ('role',)}),
)

admin.site.register(CustomizedUser, UserAdmin)
