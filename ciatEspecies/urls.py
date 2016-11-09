"""ciatEspecies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from .views import *
from focusgroups.views import *
from utils import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^jet/', include('jet.urls', 'jet')),
    #url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    url(r'^admin/', admin.site.urls),
    # url(r'^report_builder/', include('report_builder.urls'))
    url(r'^mapa-index/$', obtener_lista, name='obtener-lista'),
    url(r'^filtros/$', filtros, name='filtros'),
    url(r'^especies/', include('focusgroups.urls')),
    url(r'^ajax/countries/$', get_country, name='get-country'),
    url(r'^ajax/provinces/$', get_province, name='get-province'),
    url(r'^ajax/communities/$', get_community, name='get-community'),
    url(r'^xls/$', save_as_xls),
    # url(r'^export-focusgroup/$', export_focusgroup_csv, name='export-focusgroup-csv'),
    # url(r'^export-species/$', export_species_csv, name='export-species-csv'),
]
