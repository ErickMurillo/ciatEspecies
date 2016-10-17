from django.conf.urls import url, include
from focusgroups.views import *

urlpatterns = [
    url(r'^grupo-nutricional/$', grupo_nutricional, name='grupo-nutricional'),
]
