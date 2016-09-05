# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from species.models import Species

# Create your models here.


CHOICE_REGION = (
					(1, 'APAC'),
					(2, 'LatAm'),
					(3, 'South Asia'),
					(4, 'Asia'),
					(5, 'Africa'),
				)


class Country(models.Model):
	region = models.IntegerField(choices=CHOICE_REGION)
	name = models.CharField(max_length=250)
	latitud = models.FloatField(blank=True,null=True)
	longitud = models.FloatField(blank=True,null=True)

	def __str__(self):
		return self.name


class Province(models.Model):
	country = models.ForeignKey(Country,blank=True,null=True)
	name = models.CharField(max_length=250)
	latitud = models.FloatField(blank=True,null=True)
	longitud = models.FloatField(blank=True,null=True)

	def __str__(self):
		return self.name

class County(models.Model):
	province = models.ForeignKey(Province,blank=True,null=True)
	name = models.CharField(max_length=250)
	latitud = models.FloatField(blank=True,null=True)
	longitud = models.FloatField(blank=True,null=True)

	def __str__(self):
		return self.name

class Community(models.Model):
	# county = models.ForeignKey(County,blank=True,null=True)
	province = models.ForeignKey(Province,blank=True,null=True)
	name = models.CharField(max_length=250)
	latitud = models.FloatField(blank=True,null=True)
	longitud = models.FloatField(blank=True,null=True)

	def __str__(self):
		return self.name.encode('ASCII', 'ignore')


class Climate(models.Model):
	name =  models.CharField(max_length=250)

	def __str__(self):
		return self.name


# class Location(models.Model):
#     """
#     Description: Info about location all focus groups
#     """
#     region = models.IntegerField(choices=CHOICE_REGION)
#     country = models.ForeignKey(Country)
#     province = models.ForeignKey(Province)
#     community = models.ForeignKey(Community)
#     climate = models.ForeignKey(Climate)
#     market_distance = models.FloatField(help_text='in km')
#     population = models.FloatField()
#
#     def __str__(self):
#     	return self.get_region_display()
#
#
#    	class Meta:
#    		verbose_name = 'Location info'
#    		verbose_name_plural = 'Location info'


CHOICE_GENDER = ((1,'Female'),(2, 'Male'),)


class Scientists(models.Model):
	# country = models.ForeignKey(Country)
	name = models.CharField(max_length = 250)
	# gender = models.IntegerField(choices=CHOICE_GENDER)

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


class Language(models.Model):
	name = models.CharField(max_length = 250)

	def __str__(self):
		return self.name


class EthnicGroup(models.Model):
	name = models.CharField(max_length = 250)
	# language = models.ForeignKey(Language)

	def __str__(self):
		return self.name

CHOICE_SEASONS = (
					(1, 'Year-Round (Y)'),
					(2, 'Lean Season (L)'),
				)
GENDER_CHOICES = ((1,'Female'),(2, 'Male'),(3,'Both'))

class FocusGroup(models.Model):
	country = models.ForeignKey(Country,blank=True,null=True)
	province = models.ForeignKey(Province,blank=True,null=True)
	# county = models.ForeignKey(County,blank=True,null=True)
	community = models.ForeignKey(Community,blank=True,null=True)
	date = models.DateField(blank=True,null=True)
	scientist = models.ForeignKey(Scientists,blank=True,null=True)
	organization = models.ForeignKey(Organizations,blank=True,null=True)
	crp = models.ForeignKey(CRP,blank=True,null=True)
	ethnic_group = models.ManyToManyField(EthnicGroup,blank=True)
	language = models.ManyToManyField(Language,blank=True)
	hh = models.CharField(max_length = 250,blank=True,null=True)
	area = models.FloatField(blank=True,null=True)
	frecuency = models.CharField(max_length = 250,blank=True,null=True)
	year_round = models.CharField(max_length = 250,blank=True,null=True)
	lean_season = models.CharField(max_length = 250,blank=True,null=True)
	climate = models.CharField(max_length = 250,blank=True,null=True)
	population = models.FloatField(blank=True,null=True)
	market_distance = models.TextField(help_text='in km',blank=True,null=True)
	gender = models.IntegerField(choices=GENDER_CHOICES,blank=True,null=True)
	method_observations = models.TextField(blank=True,null=True)

	def __str__(self):
		return u'%s - %s - %s - %s - %s' % (self.id,self.community,self.date,self.scientist,self.organization)


CHOICE_FCA = ((1, '1'),(2, '2'),(3, '3'),(4,'4'))
CHOICE_PRESENCE = ((0, '0'),(1, '1'))
CHOICE_SOURCE = ((1, 'Cultivated/Reared'),(2, 'Wild'),(3, 'Mixed/Both'))
CHOICE_SEASON = (('L', 'Lean'),('A', 'All year'))
CHOICE_OFF_SEASON = ((0, 'No'),(1, 'Yes'))


class PartUsed(models.Model):
	name = models.CharField(max_length=250)

	def __str__(self):
		return self.name

class Uses(models.Model):
	name = models.CharField(max_length=250)

	def __str__(self):
		return self.name

class CookingMethod(models.Model):
	name = models.CharField(max_length=250)

	def __str__(self):
		return self.name

class FcaCode(models.Model):
	focus_groups = models.ForeignKey(FocusGroup)
	species = models.ForeignKey(Species,null=True, blank=True)
	scientific_name2 = models.CharField(max_length=450, null=True, blank=True)
	species_english_name = models.CharField(max_length=450, null=True, blank=True)
	species_french_name = models.CharField(max_length=450, null=True, blank=True)
	species_vernacular_name = models.CharField(max_length=450, null=True, blank=True)
	fca_cultivated = models.IntegerField(choices=CHOICE_FCA, null=True, blank=True)
	fca_sold = models.IntegerField(choices=CHOICE_FCA, null=True, blank=True)
	fca_purchased = models.IntegerField(choices=CHOICE_FCA, null=True, blank=True)
	fca_consumed = models.IntegerField(choices=CHOICE_FCA, null=True, blank=True)
	presence_cultivated = models.IntegerField(choices=CHOICE_PRESENCE, null=True, blank=True)
	presence_sold = models.IntegerField(choices=CHOICE_PRESENCE, null=True, blank=True)
	presence_purchased = models.IntegerField(choices=CHOICE_PRESENCE, null=True, blank=True)
	presence_consumed = models.IntegerField(choices=CHOICE_PRESENCE, null=True, blank=True)
	source = models.IntegerField(choices=CHOICE_SOURCE, null=True, blank=True)
	season = models.CharField(max_length=2, choices=CHOICE_SEASON, null=True, blank=True)
	off_season = models.IntegerField(choices=CHOICE_OFF_SEASON, null=True, blank=True)
	lean_season = models.IntegerField(choices=CHOICE_OFF_SEASON, null=True, blank=True)
	parts_used = models.ManyToManyField(PartUsed,blank=True)
	uses = models.CharField(max_length=450, null=True, blank=True)
	cooking_method = models.CharField(max_length=450, null=True, blank=True)
	# notes = models.TextField()

	# def __str__(self):
	# 	return self.focus_groups

	class Meta:
		verbose_name='FCA Codes'
		verbose_name_plural='FCA Codes'
