from django.conf.urls import url, include
from focusgroups.views import *

urlpatterns = [
    url(r'^nutritional-group-by-community/$', grupo_nutricional_comunidad, name='nutritional-group-by-community'),
    url(r'^nutritional-group-by-country/$', grupo_nutricional_pais, name='nutritional-group-by-country'),
    url(r'^number-of-species/$', numero_especies, name='number-of-species'),
    url(r'^relationship-between-number-of-species-environmental-and-economic-factors/$', numero_especies_comunidad, name='relationship'),
    url(r'^profile-spicies/$', perfil_especies, name='profile-spicies'),
    url(r'^profile-spicies/(?P<id>\d+)/$', perfil_especies_detalle, name='profile-spicies-detalle'),
    url(r'^profile-focus-groups/$', perfil_focus_groups, name='perfil_focus_groups'),
    url(r'^profile-focus-groups/(?P<id>\d+)/$', perfil_focus_groups_detail, name='profile-focus-groups-detail'),
    url(r'^profile-abd/$', perfil_abd, name='profile-abd'),
    url(r'^tables-abd/$', tables_abd, name='tables-abd'),
]
