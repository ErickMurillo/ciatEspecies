from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.register(Country)
admin.site.register(Province)
admin.site.register(County)
admin.site.register(Community)
admin.site.register(Climate)
# admin.site.register(Location)
admin.site.register(Scientists)
admin.site.register(Organizations)
admin.site.register(CRP)
admin.site.register(Language)
admin.site.register(EthnicGroup)

class FocusGroupAdmin(ImportExportModelAdmin):
    model = FocusGroup

admin.site.register(FocusGroup,FocusGroupAdmin)

admin.site.register(PartUsed)
admin.site.register(Uses)
admin.site.register(CookingMethod)
admin.site.register(FcaCode)
