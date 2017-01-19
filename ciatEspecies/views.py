from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
import json as simplejson
from focusgroups.models import *
from informacion.models import *
from django.views.generic import DetailView, ListView
from focusgroups.forms import *
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMultiAlternatives

# Create your views here.
def set_lang(request, lang_code):
    if not lang_code in ['en', 'es']:
        raise Http404

    next = request.GET.get('next', '/')
    if not next:
        next = request.META.get('HTTP_REFERER', '/')
    response = HttpResponseRedirect(next)

    if hasattr(request, 'session'):
        request.session['django_language'] = lang_code
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)

    return response

def index(request,template="index.html"):
    paises = FocusGroup.objects.all().distinct('country__name').count()
    comunidades = FocusGroup.objects.all().distinct('community__name').count()
    species = FocusGroup.objects.all().distinct('fcacode__species').count()
    focus_groups = FocusGroup.objects.all().count()
    proyectos = Proyectos.objects.order_by('-id')

    dicc = {}
    orgs = {}
    for obj in Country.objects.all():
        cientificos = Scientists.objects.filter(pais = obj).order_by('-id')
        if cientificos:
            dicc[obj] = cientificos

        organzaciones = Organizations.objects.filter(pais = obj).order_by('-id')
        if organzaciones:
            orgs[obj] = organzaciones

    return render(request, template, locals())

class ProyectoDetailView(DetailView):
    queryset = Proyectos.objects.order_by('-id')
    template_name = "proyecto_detail.html"

class OrganizacionDetailView(DetailView):
    model = Organizations
    template_name = "org_detail.html"

class CientificoDetailView(DetailView):
    model = Scientists
    template_name = "cientificos_detail.html"

class PublicacionListView(ListView):
    model = Proyectos
    template_name = "publicacion-list.html"

class CientificosListView(ListView):
    queryset = Scientists.objects.order_by('-id')
    template_name = "cientificos-list.html"

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

def afiliarse(request, template="afiliarse.html"):
    arreglo_mail = ['erickmurillo22@gmail.com',]
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            project = form.cleaned_data['project']
            tipo = form.cleaned_data['tipo']
            message = form.cleaned_data['message']
        #     try:
        #         text_content = render_to_string('notify.txt',{'name': name,'email': email,'project':project,'tipo':tipo,'message':message})
        #         send_mail('ABD Species', text_content, 'noreply@abd-data.org', arreglo_mail)
        #
        #         enviado = 1
        #
        #     except:
        #         enviado = 2
        # else:
		# 	enviado = 0

        try:
            subject, from_email, to = 'ABD Species', 'noreply@abd-data.org', arreglo_mail
            text_content =  'Nombre: ' + str(name) + ', '  + \
                            'Telefono: ' + str(project) + ', ' + \
                            'Correo: ' + str(email) + ', ' + \
                            'Mensaje: ' + str(message)

            html_content = 'Nombre: ' + str(name) + ', '  + \
                            'Telefono: ' + str(project) + ', ' + \
                            'Correo: ' + str(email) + ', ' + \
                            'Mensaje: ' + str(message)

            msg = EmailMultiAlternatives(subject, text_content, from_email, arreglo_mail)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return HttpResponseRedirect('/')
        except:
            pass

    else:
        form = EmailForm()
    return render(request, template, locals())
