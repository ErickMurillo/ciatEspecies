from django.conf.urls import url, include
from focusgroups.views import *

urlpatterns = [
    url(r'^grupo-nutricional-comunidad/$', grupo_nutricional_comunidad, name='grupo-nutricional-comunidad'),
    url(r'^grupo-nutricional-pais/$', grupo_nutricional_pais, name='grupo-nutricional-pais'),
    url(r'^numero-especies/$', numero_especies, name='numero-especies'),
]
