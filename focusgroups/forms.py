# -*- coding: UTF-8 -*-
from django.db import models
from models import *
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

CHOICE_REGION = (('','-------'),(1, 'APAC'),(2, 'LatAm'),(3, 'South Asia'),(4, 'Asia'),(5, 'Africa'),)

GENDER_CHOICES = (('','-------'),(1,'Female'),(2, 'Male'),(3,'Both'))

def fecha_choice():
    years = []
    for en in FocusGroup.objects.order_by('year').values_list('year', flat=True):
        years.append((en,en))
    return list(sorted(set(years)))

def country():
    foo = FocusGroup.objects.all().order_by('country__name').distinct().values_list('country__id', flat=True)
    return Country.objects.filter(id__in=foo)

class FocusGroupForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FocusGroupForm, self).__init__(*args, **kwargs)
        self.fields['region'] = forms.ChoiceField(choices=CHOICE_REGION,required=True,label=u'Region Geografico')
        self.fields['country'] = forms.ModelMultipleChoiceField(queryset=country(), required=True, label=u'Pais')
        self.fields['province'] = forms.ModelMultipleChoiceField(queryset=Province.objects.all(), required=True)
        # self.fields['county'] = forms.ModelMultipleChoiceField(queryset=County.objects.all(), required=False)
        self.fields['community'] = forms.ModelMultipleChoiceField(queryset=Community.objects.all(),required=True)
        self.fields['gender'] = forms.ChoiceField(choices=GENDER_CHOICES,required=False,label=u'Género')
        self.fields['year'] = forms.ChoiceField(choices=fecha_choice(),required=False,label=u'Año')

DATA_CHOICES = (('Solicitar datos','Solicitar datos'),('Afilizarse','Afilizarse'))
class EmailForm(forms.Form):
      name = forms.CharField(max_length=255,label=_("Send Options"))
      email = forms.EmailField(label=_("Correo"))
      project = forms.CharField(max_length=255,label=_("Proyecto"))
      tipo = forms.ChoiceField(choices=DATA_CHOICES,label=_("Tipo"))
      message = forms.CharField(widget=forms.Textarea,label=_("Descripción breve"))
