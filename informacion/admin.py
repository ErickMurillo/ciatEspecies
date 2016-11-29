from django.contrib import admin
from .models import *

# Register your models here.
class Archivos_Inline(admin.TabularInline):
	model = Archivos
	extra = 1

class ProyectosAdmin(admin.ModelAdmin):
    inlines = [Archivos_Inline,]
    search_fields = ['titulo',]
    date_hierarchy = 'fecha'

admin.site.register(Proyectos,ProyectosAdmin)
admin.site.register(Cientificos)
admin.site.register(Organizaciones)
