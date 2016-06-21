from __future__ import unicode_literals

from django.db import models

# Create your models here.

CHOICE_REGION = (
					(1, 'APAC'),
					(2, 'SSA'),
					(3, 'Mena'),
					(4, 'LatAm'),
				)

class Country(models.Model):
	name = models.CharField(max_length=250)
	latitud = models.FloatField()
	longitud = models.FloatField()

class Location(models.Model):
    """
    Description: Info about location all focus groups
    """
    region = models.IntField(choices=CHOICE_REGION)
    country = models.ForeignKey(Country)
    

    