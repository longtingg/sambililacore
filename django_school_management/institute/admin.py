from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import InstituteProfile, City, EducationBoard

# --- Resources ---
class InstituteProfileResource(resources.ModelResource):
    class Meta:
        model = InstituteProfile

class CityResource(resources.ModelResource):
    class Meta:
        model = City

# --- ModelAdmins ---
@admin.register(InstituteProfile)
class InstituteProfileAdmin(ImportExportModelAdmin):
    resource_class = InstituteProfileResource

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
