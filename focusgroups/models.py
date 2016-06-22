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

	def __str__(self):
		return self.name


class Province(models.Model):
	country = models.ForeignKey(Country)
	name = models.CharField(max_length=250)
	latitud = models.FloatField()
	longitud = models.FloatField()

	def __str__(self):
		return self.name 


class Community(models.Model):
	province = models.ForeignKey(Province)
	name = models.CharField(max_length=250)
	latitud = models.FloatField()
	longitud = models.FloatField()

	def __str__(self):
		return self.name


class Climate(models.Model):
	name =  models.CharField(max_length=250)

	def __str__(self):
		return self.name


class Location(models.Model):
    """
    Description: Info about location all focus groups
    """
    region = models.IntegerField(choices=CHOICE_REGION)
    country = models.ForeignKey(Country)
    province = models.ForeignKey(Province)
    community = models.ForeignKey(Community)
    climate = models.ForeignKey(Climate)
    market_distance = models.FloatField(help_text='in km')
    population = models.FloatField()

    def __str__(self):
    	return self.get_region_display()


   	class Meta:
   		verbose_name = 'Location info'
   		verbose_name_plural = 'Location info'


CHOICE_GENDER = ((1,'Female'),(2, 'Male'),)


class Scientists(models.Model):
	country = models.ForeignKey(Country)
	name = models.CharField(max_length = 250)
	gender = models.IntegerField(choices=CHOICE_GENDER)

	def __str__(self):
		return self.name


class Organizations(models.Model):
	name = models.CharField(max_length = 250)

	def __str__(self):
		return self.name


class CRP(models.Model):
	name = models.CharField(max_length = 250)

	def __str__(self):
		return self.name


class Laguage(models.Model):
	name = models.CharField(max_length = 250)

	def __str__(self):
		return self.name


class EthnicGroup(models.Model):
	name = models.CharField(max_length = 250)
	language = models.ForeignKey(Laguage)

	def __str__(self):
		return self.name

    
class FocusGroup(models.Model):
	location = models.ForeignKey(Location)
	date = models.DateField()
	scientist = models.ForeignKey(Scientists)
	organization = models.ForeignKey(Organizations)
	crp = models.ForeignKey(CRP)
	ethnic_group = models.ForeignKey(EthnicGroup)



