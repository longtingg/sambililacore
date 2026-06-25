from rolepermissions.roles import assign_role
from rolepermissions.admin import RolePermissionsUserAdminMixin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin

from .models import CustomGroup, CommonUserProfile, SocialLink
from .forms import UserRegistrationForm, UserChangeForm

User = get_user_model()


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class CustomUserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserRegistrationForm
    model = User
    fieldsets = (
        ("SCES User", {"fields": ("approval_status", "requested_role", "institute", "phone_number", "nrc_number")}),
    ) + auth_admin.UserAdmin.fieldsets
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "email", "password1", "password2", "is_staff",
                "is_active", "is_superuser", "groups", "user_permissions",
                "phone_number", "nrc_number",
            )}
         ),
    )
    list_display = ["username", "email", "institute", "is_superuser", "approval_status", "requested_role"]
    list_filter = ["institute", "approval_status", "requested_role", "is_superuser"]
    list_editable = ["approval_status", "requested_role"]
    search_fields = ["username", "email", "phone_number", "nrc_number", "approval_status", "requested_role"]
    resource_class = UserResource
    autocomplete_fields = ["institute"]


class UserProfileResource(resources.ModelResource):
    class Meta:
        model = CommonUserProfile


class UserProfileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = UserProfileResource


class CustomGroupAdmin(GroupAdmin):
    list_display = ('id', 'name', 'group_creator')


admin.site.register(CommonUserProfile, UserProfileAdmin)
admin.site.register(CustomGroup, CustomGroupAdmin)
admin.site.register(User, CustomUserAdmin)
