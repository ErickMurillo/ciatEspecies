from django.contrib import admin
from .models import *
from import_export.admin import ImportExportActionModelAdmin

# admin.site.register(FoodGroup)
# admin.site.register(NameOrder)
# admin.site.register(NameFamily)
# admin.site.register(NameGenus)
# admin.site.register(NameSpecies)
admin.site.register(NameCultivar)

# import export
class FoodGroupAdmin(ImportExportActionModelAdmin):
    model = FoodGroup

admin.site.register(FoodGroup,FoodGroupAdmin)

class NameOrderAdmin(ImportExportActionModelAdmin):
    model = NameOrder

admin.site.register(NameOrder,NameOrderAdmin)

class NameFamilyAdmin(ImportExportActionModelAdmin):
    model = NameFamily

admin.site.register(NameFamily,NameFamilyAdmin)
