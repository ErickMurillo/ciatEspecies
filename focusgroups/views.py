from django.shortcuts import render
from django.http import HttpResponse
import json as simplejson
from focusgroups.models import *
from focusgroups.forms import *
from focusgroups.admin import *
from species.admin import *
from globalconfigs.models import *

# Create your views here.
def _queryset_filtrado(request):
    params = {}

    if request.session['region']:
        params['country__region'] = request.session['region']

    if request.session['country']:
        params['country__in'] = request.session['country']

    if request.session['province']:
        params['province__in'] = request.session['province']

    # if request.session['county']:
    #     params['county__in'] = request.session['county']

    if request.session['community']:
        params['community__in'] = request.session['community']

        # if request.session['gender']:
        #     params['gender'] = request.session['gender']

	unvalid_keys = []
	for key in params:
		if not params[key]:
			unvalid_keys.append(key)

	for key in unvalid_keys:
		del params[key]

	return FocusGroup.objects.filter(**params)

def filtros(request,template="consulta.html"):
    if request.method == 'POST':
        mensaje = None
        form = FocusGroupForm(request.POST)
        if form.is_valid():
            request.session['region'] = form.cleaned_data['region']
            request.session['country'] = form.cleaned_data['country']
            request.session['province'] = form.cleaned_data['province']
            # request.session['county'] = form.cleaned_data['county']
            request.session['community'] = form.cleaned_data['community']
            #request.session['gender'] = form.cleaned_data['gender']

            mensaje = "Todas las variables estan correctamente :)"
            request.session['activo'] = True
            centinela = 1
        else:
            centinela = 0

    else:
        form = FocusGroupForm()
        mensaje = "Existen alguno errores"
        centinela = 0
        try:
            del request.session['region']
            del request.session['country']
            del request.session['province']
            del request.session['comunidad']
            # del request.session['county']
            del request.session['community']
            #del request.session['gender']
        except:
            pass

    focusgroups = FocusGroup.objects.all()
    species = Species.objects.all()

    return render(request, template, locals())

def grupo_nutricional(request,template="salidas/grupo_nutricional.html"):
    filtro = _queryset_filtrado(request)

    comunnity = request.session['community']

    comu = {}
    for obj in comunnity:
        food = {}
        for x in FoodGroup.objects.all():
            lista = []
            for gender in GENDER_CHOICES:
                print filtro
                conteo = filtro.filter(fcacode__species__food_group = x,community = obj,gender = gender[0]).count()
                lista.append(conteo)
            food[x] = lista
        comu[obj] = food

    return render(request, template, locals())

#ajax
def get_country(request):
	ids = request.GET.get('ids', '')
	if ids:
		lista = ids.split(',')
	results = []
	countries = Country.objects.filter(region__in = lista).order_by('name').values('id', 'name')

	return HttpResponse(simplejson.dumps(list(countries)), content_type = 'application/json')

def get_province(request):
    ids = request.GET.get('ids', '')
    dicc = {}
    resultado = []
    if ids:
        lista = ids.split(',')
        for id in lista:
            try:
                country = Country.objects.get(id = id)
                provinces = Province.objects.filter(country__id = country.id).order_by('name')
                lista1 = []
                for province in provinces:
                    prov = {}
                    prov['id'] = province.id
                    prov['name'] = province.name
                    lista1.append(prov)
                    dicc[country.name] = lista1
            except:
                pass

    resultado.append(dicc)

    return HttpResponse(simplejson.dumps(resultado), content_type = 'application/json')

def get_community(request):
    ids = request.GET.get('ids', '')
    dicc = {}
    resultado = []
    if ids:
        lista = ids.split(',')
        for id in lista:
            try:
                province = Province.objects.get(id = id)
                communities = Community.objects.filter(province__id = province.id).order_by('name')
                lista1 = []
                for community in communities:
                    comu = {}
                    comu['id'] = community.id
                    comu['name'] = community.name
                    lista1.append(comu)
                    dicc[province.name] = lista1
            except:
                pass

    resultado.append(dicc)

    return HttpResponse(simplejson.dumps(resultado), content_type = 'application/json')

#export in template
def export_focusgroup_csv(request):
    treenode_resource = FocusGroupResource()
    dataset = treenode_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="FocusGroups.xls"'

    return response

def export_species_csv(request):
    treenode_resource = SpeciesResource()
    dataset = treenode_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Species.xls"'

    return response
