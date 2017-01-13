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
import collections
from django.utils import translation

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

    # if request.session['year']:
        # params['year'] = request.session['year']

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
            # request.session['year'] = form.cleaned_data['year']

            mensaje = "Todas las variables estan correctamente :)"
            request.session['activo'] = True
            centinela = 1
        else:
            centinela = 0

    else:
        form = FocusGroupForm()
        mensaje = "Existen alguno errores"
        try:
            del request.session['region']
            del request.session['country']
            del request.session['province']
            del request.session['comunidad']
            # del request.session['county']
            del request.session['community']
            #del request.session['gender']
            # del request.session['year']
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

    cur_language = translation.get_language()

    comu = {}
    for obj in comunnity:
        food = {}
        food_tabla = {}
        for x in FoodGroup.objects.all():
            lista = []
            tabla = []
            count_both = filtro.filter(fcacode__species__food_group = x,community = obj).distinct('fcacode__species').count()
            for gender in GENDER_CHOICES:
                #grafica
                conteo = filtro.filter(fcacode__species__food_group = x,community = obj,gender = gender[0]).distinct('fcacode__species').count()
                if conteo != 0:
                    lista.append(conteo)

                #tabla
                produced = filtro.filter(fcacode__species__food_group = x,community = obj,gender = gender[0],fcacode__presence_cultivated = 1).distinct('fcacode__species').count()
                sold = filtro.filter(fcacode__species__food_group = x,community = obj,gender = gender[0],fcacode__presence_sold = 1).distinct('fcacode__species').count()
                purchased = filtro.filter(fcacode__species__food_group = x,community = obj,gender = gender[0],fcacode__presence_purchased = 1).distinct('fcacode__species').count()
                consumed = filtro.filter(fcacode__species__food_group = x,community = obj,gender = gender[0],fcacode__presence_consumed = 1).distinct('fcacode__species').count()
                tabla.append((produced,sold,purchased,consumed))

            lista.append(count_both)
            if cur_language == 'en':
                food[x] = lista
                food_tabla[x] = tabla
            elif cur_language == 'es':
                food[x.es_name] = lista
                food_tabla[x.es_name] = tabla

        comu[obj] = (food,food_tabla)

    return render(request, template, locals())

def grupo_nutricional_pais(request,template="salidas/grupo_nutricional_pais.html"):
    filtro = _queryset_filtrado(request)

    country = request.session['country']
    GENDER_CHOICES = ((1,'Female'),(2, 'Male'))

    cur_language = translation.get_language()

    pais = {}
    for obj in country:
        food = {}
        food_tabla = {}
        for x in FoodGroup.objects.all():
            lista = []
            tabla = []
            count_both = filtro.filter(fcacode__species__food_group = x,country = obj).distinct('fcacode__species').count()
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

            lista.append(count_both)
            if cur_language == 'en':
                food[x] = lista
                food_tabla[x] = tabla
            elif cur_language == 'es':
                food[x.es_name] = lista
                food_tabla[x.es_name] = tabla
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
        total_hombres = filtro.filter(community = obj,gender = '2').distinct('fcacode__species').count()
        total_mujeres = filtro.filter(community = obj,gender = '1').distinct('fcacode__species').count()
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
        country_total_hombres = filtro.filter(country = obj,gender = '2').distinct('fcacode__species').count()
        country_total_mujeres = filtro.filter(country = obj,gender = '1').distinct('fcacode__species').count()
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
    rainfall_sold = {}
    rainfall_purchased = {}
    rainfall_consumed = {}
    temperature = {}
    temperature_sold = {}
    temperature_purchased = {}
    temperature_consumed = {}
    precipitation = {}
    precipitation_sold = {}
    precipitation_purchased = {}
    precipitation_consumed = {}
    altitude = {}
    altitude_sold = {}
    altitude_purchased = {}
    altitude_consumed = {}
    for obj in community:
        # species
        species = filtro.filter(community = obj,fcacode__presence_cultivated = 1).distinct('fcacode__species').count()
        species_sold = filtro.filter(community = obj,fcacode__presence_sold = 1).distinct('fcacode__species').count()
        species_purchased = filtro.filter(community = obj,fcacode__presence_purchased = 1).distinct('fcacode__species').count()
        species_consumed = filtro.filter(community = obj,fcacode__presence_consumed = 1).distinct('fcacode__species').count()

        #rainfll ----------------------------------------------------------------
        rain = filtro.filter(community = obj).aggregate(avg = Avg('rainfall'))['avg']
        #rainfll cultivado
        rainfall[obj] = (rain,species)
        #rainfll sold
        rainfall_sold[obj] = (rain,species_sold)
        #rainfll purchased
        rainfall_purchased[obj] = (rain,species_purchased)
        #rainfll purchased
        rainfall_consumed[obj] = (rain,species_consumed)

        #temperatura -------------------------------------------------------------------------
        temp = filtro.filter(community = obj).aggregate(avg = Avg('annual_mean_temperature'))['avg']
        #temp cultivado
        temperature[obj] = (temp,species)
        #temp sold
        temperature_sold[obj] = (temp,species_sold)
        #temp purchased
        temperature_purchased[obj] = (temp,species_purchased)
        #temp consumed
        temperature_consumed[obj] = (temp,species_consumed)

        #precipitacion----------------------------------------------------------------------------
        precitations = filtro.filter(community = obj).aggregate(avg = Avg('precipitation'))['avg']
        #precipitacion cultivado
        precipitation[obj] = (precitations,species)
        #precipitacion sold
        precipitation_sold[obj] = (precitations,species_sold)
        #precipitacion purchased
        precipitation_purchased[obj] = (precitations,species_purchased)
        #precipitacion consumed
        precipitation_consumed[obj] = (precitations,species_consumed)

        #altitude----------------------------------------------------------------------------
        altitud = filtro.filter(community = obj).aggregate(avg = Avg('altitude'))['avg']
        #altitude cultivado
        altitude[obj] = (altitud,species)
        #altitude sold
        altitude_sold[obj] = (altitud,species_sold)
        #altitude purchased
        altitude_purchased[obj] = (altitud,species_purchased)
        #altitude consumed
        altitude_consumed[obj] = (altitud,species_consumed)

    return render(request, template, locals())

def perfil_especies(request,template="salidas/perfil_especies.html"):
    filtro = _queryset_filtrado(request)
    cur_language = translation.get_language()

    country = request.session['country']

    lista = []

    esp = OrderedDict()
    for obj in filtro:
        if cur_language == 'en':
            especies = Species.objects.filter(fcacode__focus_groups = obj).values_list('id','scientific_name','food_group__name','cultivar')
        elif cur_language == 'es':
            especies = Species.objects.filter(fcacode__focus_groups = obj).values_list('id','scientific_name','food_group__es_name','cultivar')

        for especie in especies:
            lista = []
            scientific_name2 = FcaCode.objects.filter(focus_groups = obj,species = especie[0]).distinct('scientific_name2').values_list('scientific_name2', flat = True)
            english_name = FcaCode.objects.filter(focus_groups = obj,species = especie[0]).distinct('species_english_name').values_list('species_english_name', flat = True)
            french_name = FcaCode.objects.filter(focus_groups = obj,species = especie[0]).distinct('species_french_name').values_list('species_french_name', flat = True)
            vernacular_name = FcaCode.objects.filter(focus_groups = obj,species = especie[0]).distinct('species_vernacular_name').values_list('species_vernacular_name', flat = True)

            lista.append((scientific_name2,english_name,french_name,vernacular_name))

            esp[especie[1],especie[0],especie[2],especie[3]] = lista

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

    comunnity = FcaCode.objects.filter(species = object).distinct('focus_groups__community')
    conteo_comunnity = comunnity.count()
    porcent_comunnity = saca_porcentajes(conteo_comunnity,comunidades,False)

    dicc = {}
    for obj in country:
        comu = FcaCode.objects.filter(species = object,focus_groups__country = obj.focus_groups.country).distinct('focus_groups__community').values_list('focus_groups__community__name', flat=True)
        dicc[obj.focus_groups.country] = comu

    uses = FcaCode.objects.filter(species = object).distinct('uses').values_list('uses', flat = True)
    fotos = FotosSpecies.objects.filter(species = object)
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
    cur_language = translation.get_language()
    object = FocusGroup.objects.get(id = id)
    species = FcaCode.objects.filter(focus_groups = object.id).distinct('species').values_list(
                        'species_vernacular_name','fca_cultivated','fca_sold','fca_purchased','fca_consumed','species__food_group')

    lista = []
    for x in species:
        if x[5] != None:
            lista.append(x[5])
    lista = list(set(lista))

    if cur_language == 'en':
        food_groups = FoodGroup.objects.filter(id__in = lista).values_list('id','name')
    elif cur_language == 'es':
        food_groups = FoodGroup.objects.filter(id__in = lista).values_list('id','es_name')

    #consumo
    consume = collections.OrderedDict()
    produce = collections.OrderedDict()
    produce_1 = collections.OrderedDict()
    buy,buy_0,buy_1,buy_2,buy_3,buy_4,buy_5,buy_6 = {},{},{},{},{},{},{},{}
    fgd,fgd_1,fgd_2,fgd_3,fgd_4,fgd_5,fgd_6,fgd_7 = {},{},{},{},{},{},{},{}

    #venta
    venta = collections.OrderedDict()
    venta_produce = collections.OrderedDict()
    venta_produce_1 = collections.OrderedDict()
    fgdv,fgdv_1,fgdv_2,fgdv_3,fgdv_4,fgdv_5,fgdv_6,fgdv_7 = {},{},{},{},{},{},{},{}
    v_buy,v_buy_0,v_buy_1,v_buy_2,v_buy_3,v_buy_4,v_buy_5,v_buy_6 = {},{},{},{},{},{},{},{}

    for x in food_groups:
        # listas consumo
        list_1,list_2,list_3,list_4,list_5,list_6,list_7,list_8 = [],[],[],[],[],[],[],[]
        # listas venta
        ventalist_1,ventalist_2,ventalist_3,ventalist_4,ventalist_5,ventalist_6,ventalist_7,ventalist_8 = [],[],[],[],[],[],[],[]
        for sp in species:
            # tabla 1 consumo ---------------------------------------------------------------
            if (sp[1] == 1 or sp[1] == 3) and (sp[3] == None or sp[3] == 0 or sp[3] == 4) and (sp[4] == 1 or sp[4] == 3):
                if x[0] == sp[5]:
                    list_1.append(sp[0])

            if (sp[1] == 1 or sp[1] == 3) and (sp[3] == 1 or sp[3] == 3) and (sp[4] == 1 or sp[4] == 3):
                if x[0] == sp[5]:
                    list_2.append(sp[0])

            if (sp[1] == 4) and (sp[3] == None or sp[3] == 0 or sp[3] == 4) and (sp[4] == 1 or sp[4] == 3):
                if x[0] == sp[5]:
                    list_3.append(sp[0])

            if (sp[1] == 2 or sp[1] == 4) and (sp[3] == 1 or sp[3] == 3) and (sp[4] == 1 or sp[4] == 3):
                if x[0] == sp[5]:
                    list_4.append(sp[0])

            if (sp[1] == 0 or sp[1] == None) and (sp[3] == 1 or sp[3] == 3) and (sp[4] == 1 or sp[4] == 3):
                if x[0] == sp[5]:
                    list_5.append(sp[0])

            if (sp[1] == 1 or sp[1] == 3) and (sp[4] == 4):
                if x[0] == sp[5]:
                    list_6.append(sp[0])

            if (sp[1] == 4 or sp[1] == 3) and (sp[3] == None or sp[3] == 0 or sp[3] == 4) and (sp[4] == 4):
                if x[0] == sp[5]:
                    list_7.append(sp[0])

            if (sp[1] == 0 or sp[1] == None) and (sp[3] == 2 or sp[3] == 4) and (sp[4] == 2 or sp[4] == 4):
                if x[0] == sp[5]:
                    list_8.append(sp[0])

            # tabla 2 venta ------------------------------------------------------------------
            if (sp[1] == 1 or sp[1] == 3) and (sp[3] == 2 or sp[3] == 4) and (sp[2] == 1 or sp[2] == 3):
                if x[0] == sp[5]:
                    ventalist_1.append(sp[0])

            if (sp[1] == 1 or sp[1] == 3) and (sp[3] == 1 or sp[3] == 3) and (sp[2] == 1 or sp[2] == 3):
                if x[0] == sp[5]:
                    ventalist_2.append(sp[0])

            if (sp[1] == 1 or sp[1] == 3) and (sp[3] == 1 or sp[3] == 3) and (sp[2] == 2 or sp[2] == 4):
                if x[0] == sp[5]:
                    ventalist_3.append(sp[0])

            if (sp[1] == 1 or sp[1] == 3) and (sp[3] == 2 or sp[3] == 4) and (sp[2] == 2 or sp[2] == 4):
                if x[0] == sp[5]:
                    ventalist_4.append(sp[0])

            if (sp[1] == 1 or sp[1] == 3) and (sp[3] == 0 or sp[3] == None) and (sp[2] == 2 or sp[2] == 4):
                if x[0] == sp[5]:
                    ventalist_5.append(sp[0])

            if (sp[1] == 2 or sp[1] == 4) and (sp[3] == 0 or sp[3] == None) and (sp[2] == 2 or sp[2] == 4):
                if x[0] == sp[5]:
                    ventalist_6.append(sp[0])

            if (sp[1] == 2 or sp[1] == 4) and (sp[3] == 2 or sp[3] == 4) and (sp[2] == 2 or sp[2] == 4):
                if x[0] == sp[5]:
                    ventalist_7.append(sp[0])

            if (sp[1] == 2 or sp[1] == 4) and (sp[3] == 1 or sp[3] == 3) and (sp[2] == 2 or sp[2] == 4):
                if x[0] == sp[5]:
                    ventalist_8.append(sp[0])

        # tabla 1 consumo
        if list_1:
            fgd[x[1]] = list_1
        if list_2:
            fgd_1[x[1]] = list_2
        if list_3:
            fgd_2[x[1]] = list_3
        if list_4:
            fgd_3[x[1]] = list_4
        if list_5:
            fgd_4[x[1]] = list_5
        if list_6:
            fgd_5[x[1]] = list_6
        if list_7:
            fgd_6[x[1]] = list_7
        if list_8:
            fgd_7[x[1]] = list_8

        # tabla 2 venta
        if ventalist_1:
            fgdv[x[1]] = ventalist_1
        if ventalist_2:
            fgdv_1[x[1]] = ventalist_2
        if ventalist_3:
            fgdv_2[x[1]] = ventalist_3
        if ventalist_4:
            fgdv_3[x[1]] = ventalist_4
        if ventalist_5:
            fgdv_4[x[1]] = ventalist_5
        if ventalist_6:
            fgdv_5[x[1]] = ventalist_6
        if ventalist_7:
            fgdv_6[x[1]] = ventalist_7
        if ventalist_8:
            fgdv_7[x[1]] = ventalist_8

    if cur_language == 'en':
        #consumo
        buy['Few or none buy'] = fgd
        buy['Most buy'] = fgd_1
        buy_1['Few buy'] = fgd_2
        buy_2['Most buy'] = fgd_3
        buy_3['Most buy'] = fgd_4
        buy_4['Few or none buy'] = fgd_5
        buy_5['Few buy'] = fgd_6
        buy_6['Few buy'] = fgd_7

        produce['Most Produce or widely available in community'] = buy
        produce['Few Produce or available in small areas in community'] = buy_1
        produce['Few Produce or available in small and large areas in community'] = buy_2
        produce['Not Produced in Community'] = buy_3
        produce_1['Most Produce or widely available in community'] = buy_4
        produce_1['Few Produce or available in small areas in community'] = buy_5
        produce_1['Not Produced in Community'] = buy_6

        consume['Most consume/frequent'] = produce
        consume['Few consume/infrequent'] = produce_1

        #venta
        v_buy['Few or none buy'] = fgdv
        v_buy['Most buy'] = fgdv_1
        v_buy_0['Most buy'] = fgdv_2
        v_buy_0['Few buy'] = fgdv_3
        v_buy_0['None buy'] = fgdv_4
        v_buy_1['None buy'] = fgdv_5
        v_buy_1['Few buy'] = fgdv_6
        v_buy_1['Many buy'] = fgdv_7

        venta_produce['Most Produce'] = v_buy
        venta_produce_1['Most Produce'] = v_buy_0
        venta_produce_1['Few produce'] = v_buy_1

        venta['Sold by Most'] = venta_produce
        venta['Sold by few'] = venta_produce_1

    elif cur_language == 'es':
        #consumo
        buy['Pocos o ninguno compra'] = fgd
        buy['La mayoría compra'] = fgd_1
        buy_1['Pocos compran'] = fgd_2
        buy_2['La mayoria compra'] = fgd_3
        buy_3['La mayoria compra'] = fgd_4
        buy_4['Pocos o ninguno compra'] = fgd_5
        buy_5['Pocos compran'] = fgd_6
        buy_6['Pocos compran'] = fgd_7

        produce['La mayoria produce o ampliamente disponibles en la comunidad'] = buy
        produce['Pocos productos o disponibles en pequeñas áreas en la comunidad'] = buy_1
        produce['Pocos productos o disponibles en áreas pequeñas y grandes en la comunidad'] = buy_2
        produce['No producido en la comunidad'] = buy_3
        produce_1['La mayoría produce o ampliamente disponibles en la comunidad'] = buy_4
        produce_1['Pocos producen o disponibles en pequeñas áreas en la comunidad'] = buy_5
        produce_1['No producido en la comunidad'] = buy_6

        consume['La mayoria consume/con frecuencia'] = produce
        consume['Pocos consumen/poco frecuentes'] = produce_1

        #venta
        v_buy['Pocos o ninguno compra'] = fgdv
        v_buy['La mayoría compra'] = fgdv_1
        v_buy_0['La mayoria compra'] = fgdv_2
        v_buy_0['Pocos compran'] = fgdv_3
        v_buy_0['Ninguno compra'] = fgdv_4
        v_buy_1['Ninguno compra'] = fgdv_5
        v_buy_1['Pocos compran'] = fgdv_6
        v_buy_1['Muchos compran'] = fgdv_7

        venta_produce['La mayoria produce'] = v_buy
        venta_produce_1['La mayoria produce'] = v_buy_0
        venta_produce_1['Pocos producen'] = v_buy_1

        venta['Muchos venden'] = venta_produce
        venta['Pocos venden'] = venta_produce_1

    return render(request, template, locals())

def perfil_abd(request,template = "salidas/perfil_abd.html"):
    filtro = _queryset_filtrado(request)
    cur_language = translation.get_language()
    community = request.session['community']

    comu = {}
    asd = {}
    for obj in community:
        species = filtro.filter(community = obj).distinct('fcacode__species').values_list(
                            'fcacode__species_vernacular_name','fcacode__fca_cultivated','fcacode__fca_sold','fcacode__fca_purchased','fcacode__fca_consumed','fcacode__species__food_group')
        asd[obj] = species
        lista = []
        for x in species:
            if x[5] != None:
                lista.append(x[5])
        lista = list(set(lista))

        if cur_language == 'en':
            food_groups = FoodGroup.objects.filter(id__in = lista).values_list('id','name')
        elif cur_language == 'es':
            food_groups = FoodGroup.objects.filter(id__in = lista).values_list('id','es_name')

        # #consumo
        consume = collections.OrderedDict()
        produce = collections.OrderedDict()
        produce_1 = collections.OrderedDict()
        buy,buy_0,buy_1,buy_2,buy_3,buy_4,buy_5,buy_6 = {},{},{},{},{},{},{},{}
        fgd,fgd_1,fgd_2,fgd_3,fgd_4,fgd_5,fgd_6,fgd_7 = {},{},{},{},{},{},{},{}

        # #venta
        venta = collections.OrderedDict()
        venta_produce = collections.OrderedDict()
        venta_produce_1 = collections.OrderedDict()
        fgdv,fgdv_1,fgdv_2,fgdv_3,fgdv_4,fgdv_5,fgdv_6,fgdv_7 = {},{},{},{},{},{},{},{}
        v_buy,v_buy_0,v_buy_1,v_buy_2,v_buy_3,v_buy_4,v_buy_5,v_buy_6 = {},{},{},{},{},{},{},{}

        for x in food_groups:
        #     # listas consumo
            list_1,list_2,list_3,list_4,list_5,list_6,list_7,list_8 = [],[],[],[],[],[],[],[]
        #     # listas venta
            ventalist_1,ventalist_2,ventalist_3,ventalist_4,ventalist_5,ventalist_6,ventalist_7,ventalist_8 = [],[],[],[],[],[],[],[]
            for sp in species:
                # tabla 1 consumo ---------------------------------------------------------------
                if (sp[1] == 1 or sp[1] == 3) and (sp[3] == None or sp[3] == 0 or sp[3] == 4) and (sp[4] == 1 or sp[4] == 3):
                    if x[0] == sp[5]:
                        list_1.append(sp[0])

                if (sp[1] == 1 or sp[1] == 3) and (sp[3] == 1 or sp[3] == 3) and (sp[4] == 1 or sp[4] == 3):
                    if x[0] == sp[5]:
                        list_2.append(sp[0])

                if (sp[1] == 4) and (sp[3] == None or sp[3] == 0 or sp[3] == 4) and (sp[4] == 1 or sp[4] == 3):
                    if x[0] == sp[5]:
                        list_3.append(sp[0])

                if (sp[1] == 2 or sp[1] == 4) and (sp[3] == 1 or sp[3] == 3) and (sp[4] == 1 or sp[4] == 3):
                    if x[0] == sp[5]:
                        list_4.append(sp[0])

                if (sp[1] == 0 or sp[1] == None) and (sp[3] == 1 or sp[3] == 3) and (sp[4] == 1 or sp[4] == 3):
                    if x[0] == sp[5]:
                        list_5.append(sp[0])

                if (sp[1] == 1 or sp[1] == 3) and (sp[4] == 4):
                    if x[0] == sp[5]:
                        list_6.append(sp[0])

                if (sp[1] == 4 or sp[1] == 3) and (sp[3] == None or sp[3] == 0 or sp[3] == 4) and (sp[4] == 4):
                    if x[0] == sp[5]:
                        list_7.append(sp[0])

                if (sp[1] == 0 or sp[1] == None) and (sp[3] == 2 or sp[3] == 4) and (sp[4] == 2 or sp[4] == 4):
                    if x[0] == sp[5]:
                        list_8.append(sp[0])

        #         # tabla 2 venta ------------------------------------------------------------------
                if (sp[1] == 1 or sp[1] == 3) and (sp[3] == 2 or sp[3] == 4) and (sp[2] == 1 or sp[2] == 3):
                    if x[0] == sp[5]:
                        ventalist_1.append(sp[0])

                if (sp[1] == 1 or sp[1] == 3) and (sp[3] == 1 or sp[3] == 3) and (sp[2] == 1 or sp[2] == 3):
                    if x[0] == sp[5]:
                        ventalist_2.append(sp[0])

                if (sp[1] == 1 or sp[1] == 3) and (sp[3] == 1 or sp[3] == 3) and (sp[2] == 2 or sp[2] == 4):
                    if x[0] == sp[5]:
                        ventalist_3.append(sp[0])

                if (sp[1] == 1 or sp[1] == 3) and (sp[3] == 2 or sp[3] == 4) and (sp[2] == 2 or sp[2] == 4):
                    if x[0] == sp[5]:
                        ventalist_4.append(sp[0])

                if (sp[1] == 1 or sp[1] == 3) and (sp[3] == 0 or sp[3] == None) and (sp[2] == 2 or sp[2] == 4):
                    if x[0] == sp[5]:
                        ventalist_5.append(sp[0])

                if (sp[1] == 2 or sp[1] == 4) and (sp[3] == 0 or sp[3] == None) and (sp[2] == 2 or sp[2] == 4):
                    if x[0] == sp[5]:
                        ventalist_6.append(sp[0])

                if (sp[1] == 2 or sp[1] == 4) and (sp[3] == 2 or sp[3] == 4) and (sp[2] == 2 or sp[2] == 4):
                    if x[0] == sp[5]:
                        ventalist_7.append(sp[0])

                if (sp[1] == 2 or sp[1] == 4) and (sp[3] == 1 or sp[3] == 3) and (sp[2] == 2 or sp[2] == 4):
                    if x[0] == sp[5]:
                        ventalist_8.append(sp[0])

        #     # tabla 1 consumo
            if list_1:
                fgd[x[1]] = list_1
            if list_2:
                fgd_1[x[1]] = list_2
            if list_3:
                fgd_2[x[1]] = list_3
            if list_4:
                fgd_3[x[1]] = list_4
            if list_5:
                fgd_4[x[1]] = list_5
            if list_6:
                fgd_5[x[1]] = list_6
            if list_7:
                fgd_6[x[1]] = list_7
            if list_8:
                fgd_7[x[1]] = list_8

            # tabla 2 venta
            if ventalist_1:
                fgdv[x[1]] = ventalist_1
            if ventalist_2:
                fgdv_1[x[1]] = ventalist_2
            if ventalist_3:
                fgdv_2[x[1]] = ventalist_3
            if ventalist_4:
                fgdv_3[x[1]] = ventalist_4
            if ventalist_5:
                fgdv_4[x[1]] = ventalist_5
            if ventalist_6:
                fgdv_5[x[1]] = ventalist_6
            if ventalist_7:
                fgdv_6[x[1]] = ventalist_7
            if ventalist_8:
                fgdv_7[x[1]] = ventalist_8

        # #consumo
        if cur_language == 'en':
            #consumo
            buy['Few or none buy'] = fgd
            buy['Most buy'] = fgd_1
            buy_1['Few buy'] = fgd_2
            buy_2['Most buy'] = fgd_3
            buy_3['Most buy'] = fgd_4
            buy_4['Few or none buy'] = fgd_5
            buy_5['Few buy'] = fgd_6
            buy_6['Few buy'] = fgd_7

            produce['Most Produce or widely available in community'] = buy
            produce['Few Produce or available in small areas in community'] = buy_1
            produce['Few Produce or available in small and large areas in community'] = buy_2
            produce['Not Produced in Community'] = buy_3
            produce_1['Most Produce or widely available in community'] = buy_4
            produce_1['Few Produce or available in small areas in community'] = buy_5
            produce_1['Not Produced in Community'] = buy_6

            consume['Most consume/frequent'] = produce
            consume['Few consume/infrequent'] = produce_1

            #venta
            v_buy['Few or none buy'] = fgdv
            v_buy['Most buy'] = fgdv_1
            v_buy_0['Most buy'] = fgdv_2
            v_buy_0['Few buy'] = fgdv_3
            v_buy_0['None buy'] = fgdv_4
            v_buy_1['None buy'] = fgdv_5
            v_buy_1['Few buy'] = fgdv_6
            v_buy_1['Many buy'] = fgdv_7

            venta_produce['Most Produce'] = v_buy
            venta_produce_1['Most Produce'] = v_buy_0
            venta_produce_1['Few produce'] = v_buy_1

            venta['Sold by Most'] = venta_produce
            venta['Sold by few'] = venta_produce_1

        elif cur_language == 'es':
            #consumo
            buy['Pocos o ninguno compra'] = fgd
            buy['La mayoria compra'] = fgd_1
            buy_1['Pocos compran'] = fgd_2
            buy_2['La mayoria compra'] = fgd_3
            buy_3['La mayoria compra'] = fgd_4
            buy_4['Pocos o ninguno compra'] = fgd_5
            buy_5['Pocos compran'] = fgd_6
            buy_6['Pocos compran'] = fgd_7

            produce['La mayoria produce o ampliamente disponibles en la comunidad'] = buy
            produce['Pocos productos o disponibles en pequeñas áreas en la comunidad'] = buy_1
            produce['Pocos productos o disponibles en áreas pequeñas y grandes en la comunidad'] = buy_2
            produce['No producido en la comunidad'] = buy_3
            produce_1['La mayoria produce o ampliamente disponibles en la comunidad'] = buy_4
            produce_1['Pocos producen o disponibles en pequeñas áreas en la comunidad'] = buy_5
            produce_1['No producido en la comunidad'] = buy_6

            consume['La mayoria consume/con frecuencia'] = produce
            consume['Pocos consumen/poco frecuentes'] = produce_1

            #venta
            v_buy['Pocos o ninguno compra'] = fgdv
            v_buy['La mayoria compra'] = fgdv_1
            v_buy_0['La mayoria compra'] = fgdv_2
            v_buy_0['Pocos compran'] = fgdv_3
            v_buy_0['Ninguno compra'] = fgdv_4
            v_buy_1['Ninguno compra'] = fgdv_5
            v_buy_1['Pocos compran'] = fgdv_6
            v_buy_1['Muchos compran'] = fgdv_7

            venta_produce['La mayoria produce'] = v_buy
            venta_produce_1['La mayoria produce'] = v_buy_0
            venta_produce_1['Pocos producen'] = v_buy_1

            venta['Muchos venden'] = venta_produce
            venta['Pocos venden'] = venta_produce_1

        comu[obj] = (consume,venta)

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
