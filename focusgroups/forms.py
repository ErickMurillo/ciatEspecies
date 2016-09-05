# -*- coding: UTF-8 -*-
from django.db import models
from models import *
from django import forms

CHOICE_REGION = (('','-------'),(1, 'APAC'),(2, 'LatAm'),(3, 'South Asia'),(4, 'Asia'),(5, 'Africa'),)

GENDER_CHOICES = (('','-------'),(1,'Female'),(2, 'Male'),(3,'Both'))

def country():
    foo = FocusGroup.objects.all().order_by('country__name').distinct().values_list('country__id', flat=True)
    return Country.objects.filter(id__in=foo)

class FocusGroupForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(FocusGroupForm, self).__init__(*args, **kwargs)
        self.fields['region'] = forms.ChoiceField(choices=CHOICE_REGION,required=True,label=u'Region Geografico')
        self.fields['country'] = forms.ModelMultipleChoiceField(queryset=country(), required=False, label=u'Pais')
        self.fields['province'] = forms.ModelMultipleChoiceField(queryset=Province.objects.all(), required=False)
        # self.fields['county'] = forms.ModelMultipleChoiceField(queryset=County.objects.all(), required=False)
        self.fields['community'] = forms.ModelMultipleChoiceField(queryset=Community.objects.all(),required=False)
        self.fields['gender'] = forms.ChoiceField(choices=GENDER_CHOICES,required=True,label=u'Género')
