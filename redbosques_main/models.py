# Create your models here.
#from django.db import models
from django.contrib.gis.db import models


class WebMapa(models.Model):
    id_rodal = models.IntegerField(blank=True, null=False,primary_key=True)
    geom = models.GeometryField(blank=True, null=True)
    datosrestringidos = models.BooleanField(blank=True, null=True)
    nombre = models.CharField(max_length=150, blank=True, null=True)
    ccaa_nom = models.CharField(max_length=5, blank=True, null=True)
    ccaa_nombre = models.CharField(max_length=100, blank=True, null=True)
    habitat_cod = models.CharField(max_length=10, blank=True, null=True)
    habitat_nom = models.CharField(max_length=255, blank=True, null=True)
    nivel = models.CharField(max_length=100, blank=True, null=True)
    eje_cod = models.TextField(blank=True, null=True)
    eje_nom = models.CharField(max_length=50, blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'web_mapa'


class Habitat(models.Model):
    #id = models.AutoField()
    cod = models.CharField(primary_key=True, max_length=50)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    seleccion = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'te_lpeht'
