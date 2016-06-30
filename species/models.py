from __future__ import unicode_literals

from django.db import models
from globalconfigs.models import *

# Create your models here.

CHOICES_CULTIVAR = (
                        (1, 'Animal'),
                        (2, 'Plant'),
                    )

CHOICES_TYPE_SPECIES = (
                        (1, 'Annual'),
                        (2, 'Perrenial'),
                    )

class Species(models.Model):
    """
    Description: All info for Species
    """
    scientific_name = models.CharField(max_length=450)
    common_name = models.CharField(max_length=450, null=True, blank=True)
    scientific_name2 = models.CharField(max_length=450, null=True, blank=True)
    species_english_name = models.CharField(max_length=450, null=True, blank=True)
    species_french_name = models.CharField(max_length=450, null=True, blank=True)
    species_vernacular_name = models.CharField(max_length=450, null=True, blank=True)
    food_group = models.ForeignKey(FoodGroup, null=True, blank=True)
    name_order = models.ForeignKey(NameOrder, null=True, blank=True)
    name_family = models.ForeignKey(NameFamily, null=True, blank=True)
    name_genus = models.ForeignKey(NameGenus, null=True, blank=True)
    name_species = models.ForeignKey(NameSpecies, null=True, blank=True)
    cultivar = models.IntegerField(choices=CHOICES_CULTIVAR, null=True, blank=True)
    type_species = models.IntegerField(choices=CHOICES_TYPE_SPECIES, null=True, blank=True)

    def __str__(self):
        return self.scientific_name

    class Meta:
        verbose_name = 'Species'
        verbose_name_plural = 'Species'
        ordering = ['scientific_name']
        unique_together = ('scientific_name', 'common_name')



CHOICES_COOKING_METHOD = (
                        (1, 'Raw'),
                        (2, 'Not consumed'),
                        (3, 'Fresh'),
                        (4, 'Dried'),
                    )

class FctEspecies(models.Model):
    specie = models.ForeignKey(Species)
    cooking_method = models.IntegerField(choices=CHOICES_COOKING_METHOD)
    dry = models.FloatField()
    water = models.FloatField()
    energy = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    ash = models.FloatField()
    carbohidrate = models.FloatField()
    #otras ondas
    ca = models.FloatField()
    fe = models.FloatField()
    mg = models.FloatField()
    na = models.FloatField()
    zn = models.FloatField()
    vit_c = models.FloatField()
    b1 = models.FloatField()
    b2 = models.FloatField()
    b3 = models.FloatField()
    pnto = models.FloatField()
    b6 = models.FloatField()
    dfe = models.FloatField()
    fol = models.FloatField()
    folac = models.FloatField()
    b12 = models.FloatField()
    va_re = models.FloatField()
    va_rae = models.FloatField()
    retinol = models.FloatField()
    alcar = models.FloatField()
    becar = models.FloatField()
    becry = models.FloatField()
    phy = models.FloatField()
    lodine = models.FloatField()
    fe_heme = models.FloatField()
    fe_non_heme = models.FloatField()
    iron_animal = models.FloatField()

    def __str__(self):
        return self.specie

