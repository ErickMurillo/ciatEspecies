from django.shortcuts import render
from django.http import HttpResponse
import json as simplejson
from focusgroups.models import *
from informacion.models import *
from django.views.generic import DetailView

# Create your views here.
def index(request,template="index.html"):
    paises = FocusGroup.objects.all().distinct('country__name').count()
    comunidades = FocusGroup.objects.all().distinct('community__name').count()
    species = FocusGroup.objects.all().distinct('fcacode__species').count()
    focus_groups = FocusGroup.objects.all().count()
    proyectos = Proyectos.objects.all().order_by('-id')

    dicc = {}
    orgs = {}
    for obj in Country.objects.all():
        cientificos = Cientificos.objects.filter(pais = obj).order_by('-id')
        if cientificos:
            dicc[obj] = cientificos

        organzaciones = Organizaciones.objects.filter(pais = obj).order_by('-id')
        if organzaciones:
            orgs[obj] = organzaciones

    return render(request, template, locals())

class ProyectoDetailView(DetailView):
    model = Proyectos
    template_name = "proyecto_detail.html"

class OrganizacionDetailView(DetailView):
    model = Organizaciones
    template_name = "org_detail.html"

class CientificoDetailView(DetailView):
    model = Cientificos
    template_name = "cientificos_detail.html"

#obtener puntos en el mapa
def obtener_lista(request):
	if request.is_ajax():
		lista = []
		for objeto in FocusGroup.objects.all():
			dicc = dict(nombre=objeto.community.name, id=objeto.id,
						lon=float(objeto.community.longitud),
						lat=float(objeto.community.latitud)
						)
			lista.append(dicc)

		serializado = simplejson.dumps(lista)
		return HttpResponse(serializado, content_type = 'application/json')
