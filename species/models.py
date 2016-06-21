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
