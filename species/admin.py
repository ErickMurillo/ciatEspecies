from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Species, FctEspecies, CookingMethod
from import_export import resources
from species.models import *

class FotosSpeciesInline(admin.TabularInline):
    model = FotosSpecies
    extra = 1

class SpeciesAdmin(ImportExportModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('id','scientific_name', 'food_group', 'cultivar', 'type_species')
    list_display_links = ('scientific_name', 'food_group')
    list_filter = ('cultivar', 'type_species')
    search_fields = ['scientific_name', 'common_name']
    inlines = [FotosSpeciesInline,]

# Register your models here.
admin.site.register(Species, SpeciesAdmin)

class FctEspeciesAdmin(ImportExportModelAdmin):
    model = FctEspecies
    empty_value_display = '-empty-'
    list_display = ('id','specie')

admin.site.register(FctEspecies,FctEspeciesAdmin)

class CookingMethodAdmin(ImportExportModelAdmin):
    model = CookingMethod
    list_display = ('id','name')

admin.site.register(CookingMethod,CookingMethodAdmin)

class SpeciesResource(resources.ModelResource):
    class Meta:
        model = Species
        fields = ('id','scientific_name','name_genus1','name_species1','common_name','food_group__name','name_order__name','name_family__name','cultivar','type_species',)
        export_order = ('id','scientific_name','name_genus1','name_species1','common_name','food_group__name','name_order__name','name_family__name','cultivar','type_species',)
