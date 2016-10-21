# -*- coding: utf-8 -*-
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

def grupo_nutricional_comunidad(request,template="salidas/grupo_nutricional.html"):
    filtro = _queryset_filtrado(request)

    # 1. Gráfica histograma y tabla de conteos de número de especies por
    # grupo nutricional entre comunidades seleccionada por el usuario
    comunnity = request.session['community']
    GENDER_CHOICES = ((1,'Female'),(2, 'Male'))

    comu = {}
    for obj in comunnity:
        food = {}
        food_tabla = {}
        for x in FoodGroup.objects.all():
            lista = []
            tabla = []
            for gender in GENDER_CHOICES:
                #grafica
                conteo = filtro.filter(fcacode__species__food_group = x,community = obj,gender = gender[0]).distinct('fcacode__species').count()
                lista.append(conteo)

                #tabla
                produced = filtro.filter(fcacode__species__food_group = x,community = obj,gender = gender[0],fcacode__presence_cultivated = 1).distinct('fcacode__species').count()
                sold = filtro.filter(fcacode__species__food_group = x,community = obj,gender = gender[0],fcacode__presence_sold = 1).distinct('fcacode__species').count()
                purchased = filtro.filter(fcacode__species__food_group = x,community = obj,gender = gender[0],fcacode__presence_purchased = 1).distinct('fcacode__species').count()
                consumed = filtro.filter(fcacode__species__food_group = x,community = obj,gender = gender[0],fcacode__presence_consumed = 1).distinct('fcacode__species').count()
                tabla.append((produced,sold,purchased,consumed))

            food[x] = lista
            food_tabla[x] = tabla
        comu[obj] = (food,food_tabla)

    return render(request, template, locals())

def grupo_nutricional_pais(request,template="salidas/grupo_nutricional_pais.html"):
    filtro = _queryset_filtrado(request)

    country = request.session['country']
    GENDER_CHOICES = ((1,'Female'),(2, 'Male'))

    pais = {}
    for obj in country:
        food = {}
        food_tabla = {}
        for x in FoodGroup.objects.all():
            lista = []
            tabla = []
            for gender in GENDER_CHOICES:
                #grafica
                conteo = filtro.filter(fcacode__species__food_group = x,country = obj,gender = gender[0]).distinct('fcacode__species').count()
                lista.append(conteo)

                #tabla
                produced = filtro.filter(fcacode__species__food_group = x,country = obj,gender = gender[0],fcacode__presence_cultivated = 1).distinct('fcacode__species').count()
                sold = filtro.filter(fcacode__species__food_group = x,country = obj,gender = gender[0],fcacode__presence_sold = 1).distinct('fcacode__species').count()
                purchased = filtro.filter(fcacode__species__food_group = x,country = obj,gender = gender[0],fcacode__presence_purchased = 1).distinct('fcacode__species').count()
                consumed = filtro.filter(fcacode__species__food_group = x,country = obj,gender = gender[0],fcacode__presence_consumed = 1).distinct('fcacode__species').count()
                tabla.append((produced,sold,purchased,consumed))

            food[x] = lista
            food_tabla[x] = tabla
        pais[obj] = (food,food_tabla)

    return render(request, template, locals())

def numero_especies(request,template="salidas/numero_especies.html"):
    filtro = _queryset_filtrado(request)

    country = request.session['country']
    community = request.session['community']

    comu = {}
    for obj in community:
        #produced
        produced = []
        produced_hombres = filtro.filter(community = obj,gender = '2',fcacode__presence_cultivated = 1).distinct('fcacode__species').count()
        produced_mujeres = filtro.filter(community = obj,gender = '1',fcacode__presence_cultivated = 1).distinct('fcacode__species').count()
        produced_media = (produced_hombres + produced_mujeres) / float(2)
        produced.append((produced_media,produced_hombres,produced_mujeres))

        #sold
        sold = []
        sold_hombres = filtro.filter(community = obj,gender = '2',fcacode__presence_sold = 1).distinct('fcacode__species').count()
        sold_mujeres = filtro.filter(community = obj,gender = '1',fcacode__presence_sold = 1).distinct('fcacode__species').count()
        sold_media = (sold_hombres + sold_mujeres) / float(2)
        sold.append((sold_media,sold_hombres,sold_mujeres))

        #purchased
        purchased = []
        purchased_hombres = filtro.filter(community = obj,gender = '2',fcacode__presence_purchased = 1).distinct('fcacode__species').count()
        purchased_mujeres = filtro.filter(community = obj,gender = '1',fcacode__presence_purchased = 1).distinct('fcacode__species').count()
        purchased_media = (purchased_hombres + purchased_mujeres) / float(2)
        purchased.append((purchased_media,purchased_hombres,purchased_mujeres))

        #consumed
        consumed = []
        consumed_hombres = filtro.filter(community = obj,gender = '2',fcacode__presence_consumed = 1).distinct('fcacode__species').count()
        consumed_mujeres = filtro.filter(community = obj,gender = '1',fcacode__presence_consumed = 1).distinct('fcacode__species').count()
        consumed_media = (consumed_hombres + consumed_mujeres) / float(2)
        consumed.append((consumed_media,consumed_hombres,consumed_mujeres))

        #total
        total = []
        total_hombres = produced_hombres + sold_hombres + purchased_hombres + consumed_hombres
        total_mujeres = produced_mujeres + sold_media + purchased_mujeres + consumed_mujeres
        total_media = (total_hombres + total_mujeres) / float(2)
        total.append((total_media,total_hombres,total_mujeres))

        comu[obj] = (total,produced,sold,purchased,consumed)


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
