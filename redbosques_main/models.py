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


class Rodal(models.Model):
    geom = models.GeometryField(blank=True, null=True)
    datosrestringidos = models.BooleanField(blank=True, null=True)
    #metodo_cod = models.ForeignKey('Tesaurus', models.DO_NOTHING, db_column='metodo_cod')
    nombre = models.CharField(max_length=150)
    #comautonom_cod = models.ForeignKey('TeProvincia', models.DO_NOTHING, db_column='comautonom_cod')
    #provincia_cod = models.ForeignKey('TeProvincia', models.DO_NOTHING, db_column='provincia_cod', blank=True, null=True)
    municipio = models.CharField(max_length=150, blank=True, null=True)
    propietario = models.CharField(max_length=150, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    equipo = models.CharField(max_length=255, blank=True, null=True)
    #lpeht_cod = models.ForeignKey('TeLpeht', models.DO_NOTHING, db_column='lpeht_cod')
    #hic_cod = models.ForeignKey('TeHic', models.DO_NOTHING, db_column='hic_cod', blank=True, null=True)
    #regbio_cod = models.ForeignKey('TeRegbio', models.DO_NOTHING, db_column='regbio_cod', blank=True, null=True)
    #espprinc_cod = models.ForeignKey('TeTaxon', models.DO_NOTHING, db_column='espprinc_cod', blank=True, null=True)
    #espcomp_cod = models.ForeignKey('TeTaxon', models.DO_NOTHING, db_column='espcomp_cod', blank=True, null=True)
    #espprincip_h0 = models.IntegerField()
    #espcomp_h0 = models.IntegerField(blank=True, null=True)
    numesparb = models.IntegerField(blank=True, null=True)
    areabasal = models.FloatField(blank=True, null=True)
    volmadvivo = models.FloatField(blank=True, null=True)
    numestratos = models.IntegerField(blank=True, null=True)
    numclasdiam = models.IntegerField(blank=True, null=True)
    abundpiesexcep = models.FloatField(blank=True, null=True)
    volmmpie = models.FloatField(blank=True, null=True)
    volmmsuelo = models.FloatField(blank=True, null=True)
    volmmprop = models.FloatField(blank=True, null=True)
    nummicrohab = models.FloatField(blank=True, null=True)
    numfasessil = models.IntegerField(blank=True, null=True)
    valpropbosc56 = models.IntegerField(blank=True, null=True)
    valagropasant = models.IntegerField(blank=True, null=True)
    valforestant = models.IntegerField(blank=True, null=True)
    valforestrec = models.IntegerField(blank=True, null=True)
    valespinvas = models.IntegerField(blank=True, null=True)
    valfragment = models.IntegerField(blank=True, null=True)
    valcaza = models.IntegerField(blank=True, null=True)
    valherbiv = models.IntegerField(blank=True, null=True)
    valfrecuent = models.IntegerField(blank=True, null=True)
    valdurabusos = models.IntegerField(blank=True, null=True)
    otroespflora = models.CharField(max_length=500, blank=True, null=True)
    otrohics = models.CharField(max_length=500, blank=True, null=True)
    otroinfo = models.CharField(max_length=500, blank=True, null=True)
    notes = models.CharField(max_length=500, blank=True, null=True)
    dateadded = models.DateTimeField(blank=True, null=True)
    volmmtotal = models.FloatField(blank=True, null=True)
    #usuario = models.ForeignKey('User', models.DO_NOTHING, db_column='usuario', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rodal'


'''class RodalValorres(models.Model):
    _id = models.IntegerField()
    lpeht_cod = models.CharField(max_length=10, blank=True, null=True)
    calidadesta = models.IntegerField(blank=True, null=True)
    regbio_cod = models.CharField(max_length=4, blank=True, null=True)
    comautonom_cod = models.CharField(max_length=2, blank=True, null=True)
    nivel = models.CharField(max_length=100, blank=True, null=True)
    indicador_cod = models.TextField(blank=True)
    version_calidadesta = models.IntegerField(blank=True, null=True)
    version_metrica = models.IntegerField(blank=True, null=True)
    version_indicador = models.IntegerField(blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    indic_null = models.FloatField(blank=True, null=True)
    parent_cod = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'rodal_valorres' '''


class RodalValorres2(models.Model):
    id_indicador_rodal = models.TextField(primary_key=True)
    id_rodal = models.IntegerField(blank=True, null=False)
    lpeht_cod = models.CharField(max_length=10, blank=True, null=True)
    calidadesta = models.IntegerField(blank=True, null=True)
    regbio_cod = models.CharField(max_length=4, blank=True, null=True)
    comautonom_cod = models.CharField(max_length=2, blank=True, null=True)
    nivel = models.CharField(max_length=10, blank=True, null=True)
    indicador_cod = models.TextField(blank=True, null=True)
    version_calidadesta = models.IntegerField(blank=True, null=True)
    version_metrica = models.IntegerField(blank=True, null=True)
    version_indicador = models.IntegerField(blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    indic_null = models.FloatField(blank=True, null=True)
    parent_cod = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'rodal_valorres_2'
