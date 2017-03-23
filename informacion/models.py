# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from sorl.thumbnail import ImageField
from focusgroups.models import Country

# Create your models here.
IDIOMA_CHOICES = ((1,'Español'),(2,'Ingles'),(3,'Español/Ingles'))

class Proyectos(models.Model):
    titulo = models.CharField(max_length=450)
    slug = models.SlugField(editable=False, max_length=450)
    fecha = models.DateField()
    imagen_principal = ImageField(upload_to='imagenes/',verbose_name='Imagen portada')
    imagen = ImageField(upload_to='imagenes/',verbose_name='Imagen detalle')
    idioma = models.IntegerField(choices = IDIOMA_CHOICES)

    contenido = RichTextUploadingField()

    def save(self, *args, **kwargs):
        self.slug = (slugify(self.titulo))
        super(Proyectos, self).save(*args, **kwargs)

    def __str__(self):
        return self.titulo.encode('utf-8')

    class Meta:
        verbose_name = "Proyecto/Publicación"
        verbose_name_plural = "Proyectos/Publicaciones"

class Archivos(models.Model):
    proyecto = models.ForeignKey(Proyectos)
    nombre_archivo = models.CharField(max_length=450)
    archivo = models.FileField(upload_to='documentos/')

    class Meta:
        verbose_name = "Archivo"
        verbose_name_plural = "Archivos"

class Cientificos(models.Model):
    nombre = models.CharField(max_length=450)
    foto = ImageField(upload_to='cientificos/')
    slug = models.SlugField(editable=False, max_length=450)
    cargo = models.CharField(max_length=200)
    correo = models.EmailField()
    telefono = models.CharField(max_length=200)
    pais = models.ForeignKey(Country)
    perfil = RichTextUploadingField()

    def save(self, *args, **kwargs):
        self.slug = (slugify(self.nombre))
        super(Cientificos, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre.encode('utf-8')

    class Meta:
        verbose_name = "Científico"
        verbose_name_plural = "Científicos"

class Organizaciones(models.Model):
    nombre = models.CharField(max_length=450)
    logo = ImageField(upload_to='organizaciones/',blank=True, null=True)
    direccion = models.CharField(max_length=450,blank=True, null=True)
    telefono = models.CharField(max_length=200,blank=True, null=True)
    slug = models.SlugField(editable=False, max_length=450)
    url = models.URLField(blank=True, null=True)
    pais = models.ForeignKey(Country)
    descripcion = RichTextUploadingField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = (slugify(self.nombre))
        super(Organizaciones, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre.encode('utf-8')

    class Meta:
        verbose_name = "Organización"
        verbose_name_plural = "Organizaciones"

class ListaCorreo(models.Model):
    correo = models.EmailField(max_length=50)

    class Meta:
        verbose_name = "Lista correo"
        verbose_name_plural = "Lista de correos"

    def __str__(self):
        return self.correo
