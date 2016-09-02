# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources,fields
from import_export.widgets import ManyToManyWidget

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
    empty_value_display = '-empty-'
    list_display = ('id','community','date','scientist','organization')

admin.site.register(FocusGroup,FocusGroupAdmin)

class PartUsedAdmin(ImportExportModelAdmin):
    model = PartUsed
    list_display = ('id','name')

admin.site.register(PartUsed,PartUsedAdmin)

# class UsesAdmin(ImportExportModelAdmin):
#     model = Uses
#     list_display = ('id','name')
#
# admin.site.register(Uses,UsesAdmin)
#
# class CookingMethodAdmin(ImportExportModelAdmin):
#     model = CookingMethod
#     list_display = ('id','name')

# admin.site.register(CookingMethod,CookingMethodAdmin)

class FcaCodeAdmin(ImportExportModelAdmin):
    model = FcaCode
    empty_value_display = '-empty-'
    list_display = ('id','focus_groups','species')

admin.site.register(FcaCode,FcaCodeAdmin)

class FocusGroupResource(resources.ModelResource):
    class Meta:
        model = FocusGroup
        fields = ('id','country__name','province__name','county__name','community__name','date','scientist__name','organization__name',
                    'crp__name','ethnic_group__name','language','hh','area','frecuency','year_round','lean_season','climate',
                    'population','market_distance','gender','method_observations',)

        export_order = ('id','country__name','province__name','county__name','community__name','date','scientist__name','organization__name',
                    'crp__name','ethnic_group__name','language','hh','area','frecuency','year_round','lean_season','climate',
                    'population','market_distance','gender','method_observations',)
