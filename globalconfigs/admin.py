from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# admin.site.register(FoodGroup)
# admin.site.register(NameOrder)
# admin.site.register(NameFamily)
# admin.site.register(NameGenus)
# admin.site.register(NameSpecies)
admin.site.register(NameCultivar)

# import export
class FoodGroupAdmin(ImportExportModelAdmin):
    model = FoodGroup
    list_display = ('id','name')

admin.site.register(FoodGroup,FoodGroupAdmin)

class NameOrderAdmin(ImportExportModelAdmin):
    model = NameOrder
    list_display = ('id','name')

admin.site.register(NameOrder,NameOrderAdmin)

class NameFamilyAdmin(ImportExportModelAdmin):
    model = NameFamily
    list_display = ('id','name')

admin.site.register(NameFamily,NameFamilyAdmin)
