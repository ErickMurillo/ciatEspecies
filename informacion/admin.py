# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import *
from django import forms

# Register your models here.
class Archivos_Inline(admin.TabularInline):
	model = Archivos
	extra = 1

class ProyectosAdmin(admin.ModelAdmin):
    inlines = [Archivos_Inline,]
    search_fields = ['titulo',]
    date_hierarchy = 'fecha'

admin.site.register(Proyectos,ProyectosAdmin)
admin.site.register(ListaCorreo)
#admin.site.register(Cientificos)
#admin.site.register(Organizaciones)

#flatpages admin ckeditor begin-----------------------------------------------------
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.forms import FlatpageForm as FlatpageFormOld

from ckeditor_uploader.widgets import *

class FlatpageForm(FlatpageFormOld):
	content = forms.CharField(widget=CKEditorUploadingWidget())
	class Meta:
		model = FlatPage
		fields = '__all__'

class FlatPageAdmin(FlatPageAdminOld):
	form = FlatpageForm

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
#flatpages admin ckeditor end-----------------------------------------------------
