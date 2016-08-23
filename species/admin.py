from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Species, FctEspecies
from import_export import resources

class SpeciesAdmin(ImportExportModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('id','scientific_name', 'food_group', 'cultivar', 'type_species')
    list_display_links = ('scientific_name', 'food_group')
    list_filter = ('cultivar', 'type_species')
    search_fields = ['scientific_name', 'common_name']

# Register your models here.
admin.site.register(Species, SpeciesAdmin)
admin.site.register(FctEspecies)

class SpeciesResource(resources.ModelResource):
    class Meta:
        model = Species
        fields = ('id', 'scientific_name', 'food_group__name',)
