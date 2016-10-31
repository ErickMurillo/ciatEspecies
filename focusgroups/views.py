# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import json as simplejson
from focusgroups.models import *
from focusgroups.forms import *
from focusgroups.admin import *
from species.admin import *
from species.models import *
from globalconfigs.models import *
from django.db.models import Avg, Sum, F, Count
from collections import OrderedDict, Counter

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

    #por comunidad
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
        total_mujeres = produced_mujeres + sold_mujeres + purchased_mujeres + consumed_mujeres
        total_media = (total_hombres + total_mujeres) / float(2)
        total.append((total_media,total_hombres,total_mujeres))

        comu[obj] = (total,produced,sold,purchased,consumed)

    #por pais
    pais = {}
    for obj in country:
        #produced
        country_produced = []
        country_produced_hombres = filtro.filter(country = obj,gender = '2',fcacode__presence_cultivated = 1).distinct('fcacode__species').count()
        country_produced_mujeres = filtro.filter(country = obj,gender = '1',fcacode__presence_cultivated = 1).distinct('fcacode__species').count()
        country_produced_media = (country_produced_hombres + country_produced_mujeres) / float(2)
        country_produced.append((country_produced_media,country_produced_hombres,country_produced_mujeres))

        #sold
        country_sold = []
        country_sold_hombres = filtro.filter(country = obj,gender = '2',fcacode__presence_sold = 1).distinct('fcacode__species').count()
        country_sold_mujeres = filtro.filter(country = obj,gender = '1',fcacode__presence_sold = 1).distinct('fcacode__species').count()
        country_sold_media = (country_sold_hombres + country_sold_mujeres) / float(2)
        country_sold.append((country_sold_media,country_sold_hombres,country_sold_mujeres))

        #purchased
        country_purchased = []
        country_purchased_hombres = filtro.filter(country = obj,gender = '2',fcacode__presence_purchased = 1).distinct('fcacode__species').count()
        country_purchased_mujeres = filtro.filter(country = obj,gender = '1',fcacode__presence_purchased = 1).distinct('fcacode__species').count()
        country_purchased_media = (country_purchased_hombres + country_purchased_mujeres) / float(2)
        country_purchased.append((country_purchased_media,country_purchased_hombres,country_purchased_mujeres))

        #consumed
        country_consumed = []
        country_consumed_hombres = filtro.filter(country = obj,gender = '2',fcacode__presence_consumed = 1).distinct('fcacode__species').count()
        country_consumed_mujeres = filtro.filter(country = obj,gender = '1',fcacode__presence_consumed = 1).distinct('fcacode__species').count()
        country_consumed_media = (country_consumed_hombres + country_consumed_mujeres) / float(2)
        country_consumed.append((country_consumed_media,country_consumed_hombres,country_consumed_mujeres))

        #total
        country_total = []
        country_total_hombres = country_produced_hombres + country_sold_hombres + country_purchased_hombres + country_consumed_hombres
        country_total_mujeres = country_produced_mujeres + country_sold_mujeres + country_purchased_mujeres + country_consumed_mujeres
        country_total_media = (country_total_hombres + country_total_mujeres) / float(2)
        country_total.append((country_total_media,country_total_hombres,country_total_mujeres))
        pais[obj] = (country_total,country_produced,country_sold,country_purchased,country_consumed)

    return render(request, template, locals())

def numero_especies_comunidad(request,template="salidas/numero_especies_comunidad.html"):
    filtro = _queryset_filtrado(request)

    community = request.session['community']
    GENDER_CHOICES = ((1,'Mujeres'),(2, 'Hombres'))

    comu = {}
    rainfall = {}
    temperature = {}
    for obj in community:
        distancia_mercado = {}
        areas = {}
        for x in GENDER_CHOICES:
            menor_10 = filtro.filter(community = obj,gender = x[0],market_distance__range = (0,10)).count()
            entre_10_50 = filtro.filter(community = obj,gender = x[0],market_distance__range = (10.01,50)).count()
            mayor_50 = filtro.filter(community = obj,gender = x[0],market_distance__range = (50.01,1000)).count()
            distancia_mercado[x[1]] = (menor_10,entre_10_50,mayor_50)

            #areas
            hectarea_1 = filtro.filter(community = obj,gender = x[0],area__range = (0,1)).count()
            entre_1_2 = filtro.filter(community = obj,gender = x[0],area__range = (1.01,2.5)).count()
            entre_2_5 = filtro.filter(community = obj,gender = x[0],area__range = (2.51,5)).count()
            areas[x[1]] = (hectarea_1,entre_1_2,entre_2_5)

        comu[obj] = (distancia_mercado,areas)

        #precipitacion
        rain = filtro.filter(community = obj).aggregate(avg = Avg('rainfall'))['avg']
        rainfall[obj] = rain

        #temperatura
        temp = filtro.filter(community = obj).aggregate(avg = Avg('annual_mean_temperature'))['avg']
        temperature[obj] = temp

    return render(request, template, locals())

def perfil_especies(request,template="salidas/perfil_especies.html"):
    filtro = _queryset_filtrado(request)

    country = request.session['country']

    lista = []

    esp = OrderedDict()
    for obj in filtro:
        especies = Species.objects.filter(fcacode__focus_groups = obj).values_list('id','scientific_name')
        for especie in especies:
            lista = []
            scientific_name2 = FcaCode.objects.filter(focus_groups = obj,species = especie[0]).distinct('scientific_name2').values_list('scientific_name2', flat = True)
            english_name = FcaCode.objects.filter(focus_groups = obj,species = especie[0]).distinct('species_english_name').values_list('species_english_name', flat = True)
            french_name = FcaCode.objects.filter(focus_groups = obj,species = especie[0]).distinct('species_french_name').values_list('species_french_name', flat = True)
            vernacular_name = FcaCode.objects.filter(focus_groups = obj,species = especie[0]).distinct('species_vernacular_name').values_list('species_vernacular_name', flat = True)

            lista.append((scientific_name2,english_name,french_name,vernacular_name))

            esp[especie[1],especie[0]] = lista

    return render(request, template, locals())

def perfil_especies_detalle(request,id = None):
    template = "salidas/perfil_especies_detalle.html"
    filtro = _queryset_filtrado(request)

    paises = Country.objects.all().count()
    comunidades = Community.objects.all().count()

    object = Species.objects.get(id = id)
    scientific_name2 = FcaCode.objects.filter(species = object).distinct('scientific_name2').values_list('scientific_name2', flat = True)
    english_name = FcaCode.objects.filter(species = object).distinct('species_english_name').values_list('species_english_name', flat = True)
    french_name = FcaCode.objects.filter(species = object).distinct('species_french_name').values_list('species_french_name', flat = True)
    vernacular_name = FcaCode.objects.filter(species = object).distinct('species_vernacular_name').values_list('species_vernacular_name', flat = True)

    country = FcaCode.objects.filter(species = object).distinct('focus_groups__country')
    conteo_pais = country.count()
    porcent_pais = saca_porcentajes(conteo_pais,paises,False)

    comunnity = FcaCode.objects.filter(species = object).distinct('focus_groups__country')
    conteo_comunnity = comunnity.count()
    porcent_comunnity = saca_porcentajes(conteo_comunnity,comunidades,False)

    ########################
    #produced
    produced = []
    produced_hombres = FcaCode.objects.filter(species = object,focus_groups__gender = '2',presence_cultivated = 1).count()
    produced_mujeres = FcaCode.objects.filter(species = object,focus_groups__gender = '1',presence_cultivated = 1).count()
    produced_media = (produced_hombres + produced_mujeres) / float(2)
    produced.append((produced_media,produced_hombres,produced_mujeres))

    #sold
    sold = []
    sold_hombres = FcaCode.objects.filter(species = object,focus_groups__gender = '2',presence_sold = 1).count()
    sold_mujeres = FcaCode.objects.filter(species = object,focus_groups__gender = '1',presence_sold = 1).count()
    sold_media = (sold_hombres + sold_mujeres) / float(2)
    sold.append((sold_media,sold_hombres,sold_mujeres))

    #purchased
    purchased = []
    purchased_hombres = FcaCode.objects.filter(species = object,focus_groups__gender = '2',presence_purchased = 1).count()
    purchased_mujeres = FcaCode.objects.filter(species = object,focus_groups__gender = '1',presence_purchased = 1).count()
    purchased_media = (purchased_hombres + purchased_mujeres) / float(2)
    purchased.append((purchased_media,purchased_hombres,purchased_mujeres))

    #consumed
    consumed = []
    consumed_hombres = FcaCode.objects.filter(species = object,focus_groups__gender = '2',presence_consumed = 1).count()
    consumed_mujeres = FcaCode.objects.filter(species = object,focus_groups__gender = '1',presence_consumed = 1).count()
    consumed_media = (consumed_hombres + consumed_mujeres) / float(2)
    consumed.append((consumed_media,consumed_hombres,consumed_mujeres))

    return render(request, template, locals())

def perfil_focus_groups(request,template="salidas/perfil_focus_groups.html"):
    filtro = _queryset_filtrado(request)
    focus_groups = filtro

    return render(request, template, locals())

def perfil_focus_groups_detail(request,id = None):
    template = "salidas/perfil_fg_detalle.html"
    object = FocusGroup.objects.get(id = id)

    return render(request, template, locals())

def crear_rangos(request, lista, start=0, stop=0, step=0):
    dict_algo = OrderedDict()
    rangos = []
    contador = 0
    rangos = [(n, n+int(step)-1) for n in range(int(start), int(stop), int(step))]

    for desde, hasta in rangos:
        dict_algo['%s a %s' % (desde,hasta)] = len([x for x in lista if desde <= x <= hasta])

    return dict_algo

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

def saca_porcentajes(dato, total, formato=True):
	if dato != None:
		try:
			porcentaje = (dato/float(total)) * 100 if total != None or total != 0 else 0
		except:
			return 0
		if formato:
			return porcentaje
		else:
			return '%.2f' % porcentaje
	else:
		return 0
