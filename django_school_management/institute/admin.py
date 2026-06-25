from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import InstituteProfile, City, EducationBoard


class InstituteProfileResource(resources.ModelResource):
    class Meta:
        model = InstituteProfile


class CityResource(resources.ModelResource):
    class Meta:
        model = City


@admin.register(InstituteProfile)
class InstituteProfileAdmin(ImportExportModelAdmin):
    resource_class = InstituteProfileResource
    list_display = ('name', 'slug', 'is_active', 'active', 'province', 'exam_board', 'onboarding_completed')
    list_filter = ('is_active', 'active', 'province', 'exam_board', 'institute_type')
    search_fields = ('name', 'slug', 'district')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active',)
    readonly_fields = ('slug',)
    fieldsets = (
        ('Identity', {
            'fields': ('name', 'slug', 'institute_type', 'is_active', 'active', 'onboarding_completed'),
        }),
        ('Location', {
            'fields': ('country', 'province', 'district', 'exam_board'),
        }),
        ('Branding', {
            'fields': ('logo', 'logo_small', 'site_favicon', 'site_header', 'site_title', 'super_admin_index_title'),
        }),
        ('Details', {
            'fields': ('motto', 'description', 'date_of_establishment', 'curriculum', 'current_session', 'created_by'),
        }),
    )


@admin.register(City)
class CityAdmin(ImportExportModelAdmin):
    resource_class = CityResource
    list_display = ('name', 'country', 'code')
    list_filter = ('country',)
    search_fields = ('name', 'code')


@admin.register(EducationBoard)
class EducationBoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'country')
    list_filter = ('country',)
    search_fields = ('name', 'code')
