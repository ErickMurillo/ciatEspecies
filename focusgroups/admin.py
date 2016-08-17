# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class CountryAdmin(ImportExportModelAdmin):
    model = Country
    list_display = ('id','name','region')

admin.site.register(Country,CountryAdmin)

class ProvinceAdmin(ImportExportModelAdmin):
    model = Province
    list_display = ('id','name','country')

admin.site.register(Province,ProvinceAdmin)

class CountyAdmin(ImportExportModelAdmin):
    model = County
    list_display = ('id','name','province')

admin.site.register(County,CountyAdmin)

class CommunityAdmin(ImportExportModelAdmin):
    model = Community
    list_display = ('id','name')

admin.site.register(Community,CommunityAdmin)

class ClimateAdmin(ImportExportModelAdmin):
    model = Climate
    list_display = ('id','name')

admin.site.register(Climate,ClimateAdmin)
# admin.site.register(Location)

class ScientistsAdmin(ImportExportModelAdmin):
    model = Scientists
    list_display = ('id','name')

admin.site.register(Scientists,ScientistsAdmin)

class OrganizationsAdmin(ImportExportModelAdmin):
    model = Organizations
    list_display = ('id','name')

admin.site.register(Organizations,OrganizationsAdmin)

class CRPAdmin(ImportExportModelAdmin):
    model = CRP
    list_display = ('id','name')

admin.site.register(CRP,CRPAdmin)

class LanguageAdmin(ImportExportModelAdmin):
    model = Language
    list_display = ('id','name')

admin.site.register(Language,LanguageAdmin)

class EthnicGroupAdmin(ImportExportModelAdmin):
    model = EthnicGroup
    list_display = ('id','name')

admin.site.register(EthnicGroup,EthnicGroupAdmin)

class FocusGroupAdmin(ImportExportModelAdmin):
    model = FocusGroup

admin.site.register(FocusGroup,FocusGroupAdmin)

class PartUsedAdmin(ImportExportModelAdmin):
    model = PartUsed
    list_display = ('id','name')

admin.site.register(PartUsed,PartUsedAdmin)

class UsesAdmin(ImportExportModelAdmin):
    model = Uses
    list_display = ('id','name')

admin.site.register(Uses,UsesAdmin)

class CookingMethodAdmin(ImportExportModelAdmin):
    model = CookingMethod
    list_display = ('id','name')

admin.site.register(CookingMethod,CookingMethodAdmin)

class FcaCodeAdmin(ImportExportModelAdmin):
    model = FcaCode

admin.site.register(FcaCode,FcaCodeAdmin)
