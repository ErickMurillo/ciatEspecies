from __future__ import unicode_literals

from django.db import models

# Create your models here.

class FoodGroup(models.Model):
    """
    Description: Model Description
    """
    name = models.CharField(max_length=250)
    es_name = models.CharField(max_length=250,null=True,blank=True)

    def __str__(self):
    	return self.name

class NameOrder(models.Model):
    """
    Description: Model Description
    """
    name = models.CharField(max_length=250)

    def __str__(self):
    	return self.name

class NameFamily(models.Model):
    """
    Description: Model Description
    """
    name = models.CharField(max_length=250)

    def __str__(self):
    	return self.name

class NameGenus(models.Model):
    """
    Description: Model Description
    """
    name = models.CharField(max_length=250)

    def __str__(self):
    	return self.name

class NameSpecies(models.Model):
    """
    Description: Model Description
    """
    name = models.CharField(max_length=250)

    def __str__(self):
    	return self.name

class NameCultivar(models.Model):
    """
    Description: Model Description
    """
    name = models.CharField(max_length=250)

    def __str__(self):
    	return self.name
