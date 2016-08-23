from django.shortcuts import render
from django.http import HttpResponse
import json as simplejson
from focusgroups.models import *

# Create your views here.
def index(request,template="index.html"):
    return render(request, template, locals())

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
