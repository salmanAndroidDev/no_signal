from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name', 'role']

    fieldsets = (
        (None, {"fields": ('email', 'password')}),
        ('Personal Info', {"fields": ('name', 'role')}),
        ('Permissions',
         {"fields": ('is_active', 'is_staff', 'is_superuser', 'groups')}
         ),
        ('Important dates', {"fields": ('last_login',)})
    )
    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')}),
    )


admin.site.register(User, UserAdmin)
