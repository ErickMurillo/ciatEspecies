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
    scientific_name = models.CharField(max_length=450, null=True, blank=True)
    name_genus1 = models.CharField(max_length=100,verbose_name='Name genus')
    name_species1 = models.CharField(max_length=100,verbose_name='Name species')
    common_name = models.CharField(max_length=450, null=True, blank=True)
    food_group = models.ForeignKey(FoodGroup, null=True, blank=True)
    name_order = models.ForeignKey(NameOrder, null=True, blank=True)
    name_family = models.ForeignKey(NameFamily, null=True, blank=True)
    # name_genus = models.ForeignKey(NameGenus, null=True, blank=True)
    # name_species = models.ForeignKey(NameSpecies, null=True, blank=True)
    cultivar = models.IntegerField(choices=CHOICES_CULTIVAR, null=True, blank=True)
    type_species = models.IntegerField(choices=CHOICES_TYPE_SPECIES, null=True, blank=True)

    def __str__(self):
        return self.scientific_name

    class Meta:
        verbose_name = 'Species'
        verbose_name_plural = 'Species'
        ordering = ['scientific_name']
        # unique_together = ('scientific_name', 'common_name')

    def save(self, *args, **kwargs):
		self.scientific_name = self.name_genus1 + ' ' + self.name_species1
		super(Species, self).save(*args, **kwargs)



# CHOICES_COOKING_METHOD = (
#                         (1, 'Raw'),
#                         (2, 'Not consumed'),
#                         (3, 'Fresh'),
#                         (4, 'Dried'),
#                     )

class CookingMethod(models.Model):
    name = models.CharField(max_length = 250)

    def __str__(self):
        return self.name

class FctEspecies(models.Model):
    specie = models.ForeignKey(Species)
    cooking_method = models.ForeignKey(CookingMethod,null=True, blank=True)
    optifood_group = models.FloatField(null=True, blank=True)
    optifood_sub_group = models.FloatField(null=True, blank=True)
    dry = models.FloatField(null=True, blank=True)
    water = models.FloatField(null=True, blank=True)
    energy = models.FloatField(null=True, blank=True)
    protein = models.FloatField(null=True, blank=True)
    fat = models.FloatField(null=True, blank=True)
    ash = models.FloatField(null=True, blank=True)
    carbohidrate = models.FloatField(null=True, blank=True)
    #otras ondas
    ca = models.FloatField(null=True, blank=True)
    fe = models.FloatField(null=True, blank=True)
    mg = models.FloatField(null=True, blank=True)
    na = models.FloatField(null=True, blank=True)
    zn = models.FloatField(null=True, blank=True)
    vit_c = models.FloatField(null=True, blank=True)
    b1 = models.FloatField(null=True, blank=True)
    b2 = models.FloatField(null=True, blank=True)
    b3 = models.FloatField(null=True, blank=True)
    pnto = models.FloatField(null=True, blank=True)
    b6 = models.FloatField(null=True, blank=True)
    dfe = models.FloatField(null=True, blank=True)
    fol = models.FloatField(null=True, blank=True)
    folac = models.FloatField(null=True, blank=True)
    b12 = models.FloatField(null=True, blank=True)
    va_re = models.FloatField(null=True, blank=True)
    va_rae = models.FloatField(null=True, blank=True)
    retinol = models.FloatField(null=True, blank=True)
    alcar = models.FloatField(null=True, blank=True)
    becar = models.FloatField(null=True, blank=True)
    becry = models.FloatField(null=True, blank=True)
    phy = models.FloatField(null=True, blank=True)
    lodine = models.FloatField(null=True, blank=True)
    fe_heme = models.FloatField(null=True, blank=True)
    fe_non_heme = models.FloatField(null=True, blank=True)
    iron_animal = models.FloatField(null=True, blank=True)
    sci_name = models.FloatField(null=True, blank=True)
    fct_source_code = models.CharField(max_length=50,null=True, blank=True)
    fct_source_descr = models.CharField(max_length=50,null=True, blank=True)
    vol_wt_source = models.FloatField(null=True, blank=True)
    vol_wt_descr_1 = models.FloatField(null=True, blank=True)
    vol_wt_calc_1 = models.FloatField(null=True, blank=True)
    vol_wt_source_2 = models.FloatField(null=True, blank=True)
    vol_wt_descr_2 = models.FloatField(null=True, blank=True)
    vol_wt_calc_2 = models.FloatField(null=True, blank=True)
    ret_code = models.FloatField(null=True, blank=True)
    ret_descr = models.FloatField(null=True, blank=True)

    # def __str__(self):
    #     return self.specie
