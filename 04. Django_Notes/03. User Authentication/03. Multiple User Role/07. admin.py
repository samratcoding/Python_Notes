from django.contrib import admin
from .models import AppUser, Teacher, Student

admin.site.register(AppUser)
admin.site.register(Student)
admin.site.register(Student)
admin.site.site_header = 'AI Writing Project'   




# Custom Admin View for User Management
# Included password Reset Fields
from django.contrib.auth.admin import UserAdmin
class AppUserAdmin(UserAdmin):
    model = AppUser
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom Fields', {'fields': ('activation_code', 'password_reset_code', 'profile_image', 'credit')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


admin.site.register(AppUser, AppUserAdmin)
