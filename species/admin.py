from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Species


class SpeciesAdmin(ImportExportModelAdmin):
    pass

# Register your models here.
admin.site.register(Species, SpeciesAdmin)
