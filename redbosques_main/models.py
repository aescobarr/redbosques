# Create your models here.
#from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User as DUser
import os
from django.core.exceptions import ValidationError
from redbosques.settings import MAX_UPLOAD_SIZE



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
    rodalref = models.BooleanField(blank=True, null=True)
    fotoglobo = models.CharField(max_length=100, blank=True, null=True)

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

    def __str__(self):
        return '%s' % (self.nombre)


class TeProvincia(models.Model):
    #id = models.AutoField()
    cod = models.CharField(primary_key=True, max_length=5)
    codigo = models.CharField(max_length=10, blank=True, null=True)
    parent = models.CharField(max_length=10, blank=True, null=True)
    nivel = models.CharField(max_length=10, blank=True, null=True)
    nombre_es = models.CharField(max_length=10, blank=True, null=True)
    nombre_ca = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'te_provincia'

    def __str__(self):
        return '%s' % (self.nombre_es)


class TeMunicipi(models.Model):
    id = models.IntegerField(primary_key=True)
    codigoine = models.CharField(max_length=5, blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    codprov = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'te_municipi'

    def __str__(self):
        return '%s' % (self.nombre)


class TeHic(models.Model):
    # id = models.AutoField()
    cod = models.CharField(primary_key=True, max_length=5)
    corine_cod = models.ForeignKey('TeLpeht', models.DO_NOTHING, db_column='corine_cod')
    nombre_es = models.CharField(max_length=100, blank=True, null=True)
    codnombre = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'te_hic'

    def __str__(self):
        return '%s' % (self.codnombre)


class TeLpeht(models.Model):
    # id = models.AutoField()
    cod = models.CharField(primary_key=True, max_length=50)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    seleccion = models.BooleanField(blank=True, null=True)
    codnombre = models.CharField(max_length=300, blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'te_lpeht'

    def __str__(self):
        return '%s' % (self.codnombre)


class TeRegbio(models.Model):
    # id = models.AutoField()
    cod = models.CharField(primary_key=True, max_length=14)
    nombre_es = models.CharField(max_length=100, blank=True, null=True)
    nombre_cat = models.CharField(max_length=100, blank=True, null=True)
    nombre_en = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'te_regbio'

    def __str__(self):
        return '%s' % (self.nombre_es)


class TeTaxon(models.Model):
    # cod = models.CharField(unique=True, max_length=100, blank=True, null=True)
    cod = models.CharField(primary_key=True, unique=True, max_length=100)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    exotico = models.BooleanField(blank=True, null=True)
    nopenin = models.BooleanField(blank=True, null=True)
    noparboreo = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'te_taxon'

    def __str__(self):
        return '%s' % (self.nombre)


class Tesaurus(models.Model):
    #id = models.AutoField()
    cod = models.CharField(primary_key=True, max_length=10)
    columna = models.CharField(max_length=15)
    nombre_es = models.CharField(max_length=100, blank=True, null=True)
    nombre_cat = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tesaurus'

    def __str__(self):
        return '%s' % (self.nombre_es)


class User(models.Model):
    #id = models.AutoField()
    usuario = models.CharField(primary_key=True, max_length=25)
    nombre = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'



class Rodal(models.Model):
    id = models.AutoField(primary_key=True, max_length=100)
    geom = models.GeometryField(blank=True, null=True, srid=25830)
    datosrestringidos = models.BooleanField(blank=True, null=True)
    metodo_cod = models.ForeignKey(Tesaurus, models.DO_NOTHING, db_column='metodo_cod')
    nombre = models.CharField(max_length=150)
    comautonom_cod = models.ForeignKey(TeProvincia, db_column='comautonom_cod', related_name='TeProvincia_comautonom_cod', on_delete=models.CASCADE)
    provincia_cod = models.ForeignKey(TeProvincia, db_column='provincia_cod', related_name='TeProvincia_prvincia_cod', on_delete=models.CASCADE, blank=True, null=True)
    municipio = models.CharField(max_length=150, blank=True, null=True)
    propietario = models.CharField(max_length=150, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    equipo = models.CharField(max_length=255, blank=True, null=True)
    lpeht_cod = models.ForeignKey(TeLpeht, models.DO_NOTHING, db_column='lpeht_cod')
    hic_cod = models.ForeignKey(TeHic, models.DO_NOTHING, db_column='hic_cod', blank=True, null=True)
    regbio_cod = models.ForeignKey(TeRegbio, models.DO_NOTHING, db_column='regbio_cod', blank=True, null=True)
    espprinc_cod = models.ForeignKey(TeTaxon, db_column='espprinc_cod', related_name='TeTaxon_espprinc_cod', on_delete=models.CASCADE, blank=True, null=True)
    espcomp_cod = models.ForeignKey(TeTaxon, db_column='espcomp_cod', related_name='TeTaxon_espcomp_cod', on_delete=models.CASCADE, blank=True, null=True)
    espprincip_h0 = models.IntegerField()
    espcomp_h0 = models.IntegerField(blank=True, null=True)
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
    usuario = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='usuario')
    rodalref = models.BooleanField(blank=True, null=True)
    fotoglobo = models.CharField(max_length=100, blank=True, null=True)
    espprinc_fcc = models.IntegerField(db_column='espprinc_fcc', blank=True, null=True)
    espcomp_fcc = models.IntegerField(db_column='espcomp_fcc', blank=True, null=True)
    municipio1 = models.ForeignKey('TeMunicipi', models.DO_NOTHING, db_column='municipio1', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rodal'

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
    rodalref = models.BooleanField(blank=True, null=True)
    fotoglobo = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'rodal_valorres_2'


class RodalValoresAmbito(models.Model):
    id_rodal = models.IntegerField(primary_key=True)
    hh = models.FloatField(blank=True, null=True)
    ie = models.FloatField(blank=True, null=True)
    nm = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'rodal_valores_ambito'



class WebMapaValAmb(models.Model):
    id_rodal = models.IntegerField(blank=True, null=False, primary_key=True)
    geom = models.GeometryField(blank=True, null=True)
    datosrestringidos = models.BooleanField(blank=True, null=True)
    nombre = models.CharField(max_length=150, blank=True, null=True)
    ccaa_nom = models.CharField(max_length=100, blank=True, null=True)
    ccaa_nombre = models.CharField(max_length=100, blank=True, null=True)
    habitat_cod = models.CharField(max_length=10, blank=True, null=True)
    habitat_nom = models.CharField(max_length=255, blank=True, null=True)
    tipobosque_cod = models.TextField(blank=True, null=True)
    tipobosque_nombre = models.CharField(max_length=255, blank=True, null=True)
    nivel = models.CharField(max_length=100, blank=True, null=True)
    eje_cod = models.TextField(blank=True, null=True)
    eje_nom = models.CharField(max_length=50, blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    rodalref = models.BooleanField(blank=True, null=True)
    fotoglobo = models.CharField(max_length=150, blank=True, null=True)
    hh = models.FloatField(blank=True, null=True)
    ie = models.FloatField(blank=True, null=True)
    nm = models.FloatField(blank=True, null=True)
    regbio_cod = models.CharField(max_length=100, blank=True, null=True)
    nombre_es = models.CharField(max_length=100, blank=True, null=True)
    foto = models.CharField(max_length=255, blank=True, null=True)


    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'web_mapa_val_amb'


class WebCompData(models.Model):
    id_view = models.BigIntegerField(blank=True, null=True)
    id_rodal = models.IntegerField(blank=True, null=False,primary_key=True)
    geom = models.GeometryField(blank=True, null=True)
    datosrestringidos = models.BooleanField(blank=True, null=True)
    nombre = models.CharField(max_length=150, blank=True, null=True)
    ccaa_nom = models.CharField(max_length=5, blank=True, null=True)
    ccaa_nombre = models.CharField(max_length=100, blank=True, null=True)
    habitat_cod = models.CharField(max_length=10, blank=True, null=True)
    tipobosque_cod = models.TextField(blank=True, null=True)
    tipobosque_nombre = models.CharField(max_length=150, blank=True, null=True)
    habitat_nom = models.CharField(max_length=255, blank=True, null=True)
    nivel = models.CharField(max_length=100, blank=True, null=True)
    eje_cod = models.TextField(blank=True, null=True)
    eje_nom = models.CharField(max_length=50, blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    rodalref = models.BooleanField(blank=True, null=True)
    fotoglobo = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'web_comp_data'



class WebCompDataValAmb(models.Model):
    id_rodal = models.IntegerField(blank=True, null=False, primary_key=True)
    geom = models.GeometryField(blank=True, null=True)
    datosrestringidos = models.BooleanField(blank=True, null=True)
    nombre = models.CharField(max_length=150, blank=True, null=True)
    ccaa_nom = models.CharField(max_length=100, blank=True, null=True)
    ccaa_nombre = models.CharField(max_length=100, blank=True, null=True)
    habitat_cod = models.CharField(max_length=10, blank=True, null=True)
    habitat_nom = models.CharField(max_length=255, blank=True, null=True)
    tipobosque_cod = models.TextField(blank=True, null=True)
    tipobosque_nombre = models.CharField(max_length=255, blank=True, null=True)
    nivel = models.CharField(max_length=100, blank=True, null=True)
    eje_cod = models.TextField(blank=True, null=True)
    eje_nom = models.CharField(max_length=50, blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    rodalref = models.BooleanField(blank=True, null=True)
    fotoglobo = models.CharField(max_length=150, blank=True, null=True)
    hh = models.FloatField(blank=True, null=True)
    ie = models.FloatField(blank=True, null=True)
    nm = models.FloatField(blank=True, null=True)
    regbio_cod = models.CharField(max_length=100, blank=True, null=True)
    nombre_es = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'web_comp_data_val_amb'


class BosqueCf(models.Model):
    rid = models.AutoField(primary_key=True)
    rast = models.RasterField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bosque_cf'


class BosqueSf(models.Model):
    rid = models.AutoField(primary_key=True)
    rast = models.RasterField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bosque_sf'


class BosquePs(models.Model):
    rid = models.AutoField(primary_key=True)
    rast = models.RasterField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bosque_ps'


class TeCategoria(models.Model):
    #id = models.IntegerField()
    variable_rodal = models.ForeignKey('TeIndicador', models.DO_NOTHING, db_column='variable_rodal')
    categoria = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'te_categoria'
        unique_together = (('variable_rodal', 'categoria'))

    def __str__(self):
        return '%s' % (self.categoria)


class TeIndicador(models.Model):
    id = models.IntegerField(blank=True, null=True)
    cod = models.CharField(primary_key=True, max_length=2)
    nombre_es = models.CharField(max_length=50, blank=True, null=True)
    nombre_ca = models.CharField(max_length=50, blank=True, null=True)
    descripcion_es = models.CharField(max_length=500, blank=True, null=True)
    descripcion_ca = models.CharField(max_length=500, blank=True, null=True)
    dateadded = models.DateTimeField()
    val_minimo = models.FloatField(blank=True, null=True)
    val_alerta = models.FloatField(blank=True, null=True)
    val_maximo = models.FloatField(blank=True, null=True)
    variable_rodal = models.CharField(unique=True, max_length=25, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'te_indicador'


def urlFotos(instance, filename):
    #print(str(instance.id_rodal.id))
    return os.path.join("fotos", str(instance.id_rodal.id), filename)

'''def validate_image(foto):
    print("hola")
    limit = MAX_UPLOAD_SIZE
    file_size = foto.file.size
    limit_kb = 2048/1024
    if file_size > limit:
        raise ValidationError("Max size of file is %s KB" % limit + " MB")'''






class FotosRodal(models.Model):
    id_foto = models.AutoField(primary_key=True)
    id_rodal = models.ForeignKey('Rodal', on_delete=models.CASCADE, db_column='id_rodal')
    nombre_foto = models.CharField(max_length=200, blank=True, null=True)
    #foto = models.FileField(upload_to='media/fotos/')
    #foto = models.ImageField(upload_to=urlFotos, validators=[validate_image])
    foto = models.ImageField(upload_to=urlFotos)
    fotoprincipal = models.BooleanField()


    class Meta:
        managed = False
        db_table = 'fotos_rodal'
        unique_together = (('id_foto', 'id_rodal', 'fotoprincipal'),)

    def delete(self, *args, **kwargs):
        self.foto.delete()
        super().delete(*args, **kwargs)

    '''def clean_foto(self):
        cleaned_data = self.cleaned_data
        foto = cleaned_data.get('foto')

        limit = MAX_UPLOAD_SIZE
        file_size = foto.file.size
        print(file_size)
        if file_size > limit:
            raise ValidationError("Max size of file is %s KB" % limit + " MB")'''

def urlDocs(instance, filename):
    return os.path.join("docs", str(instance.id_rodal.id), filename)

class DocsRodal(models.Model):
    id_doc = models.AutoField(primary_key=True)
    id_rodal = models.ForeignKey('Rodal', on_delete=models.CASCADE, db_column='id_rodal')
    nombre_doc = models.CharField(max_length=200, blank=True, null=True)
    doc = models.FileField(upload_to=urlDocs)

    class Meta:
        managed = False
        db_table = 'docs_rodal'
        unique_together = (('id_doc', 'id_rodal'),)

    def delete(self, *args, **kwargs):
        self.doc.delete()
        super().delete(*args, **kwargs)


class Institucion(models.Model):
    nombre = models.CharField(max_length=200)
    acronimo = models.CharField(max_length=20, blank=True)

    class Meta:
        managed = False
        verbose_name_plural = "instituciones"
        db_table = 'institucion'

    def __str__(self):
        return '%s - %s' % ( self.acronimo, self.nombre )


class DatosUsuario(models.Model):
    user = models.OneToOneField(DUser, on_delete=models.CASCADE)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE)
    admin_institucion = models.BooleanField(default=False)

    @property
    def user_first_name(self):
        return self.user.first_name

    @property
    def user_last_name(self):
        return self.user.last_name

    class Meta:
        managed = False
        verbose_name_plural = "datos usuario"
        db_table = 'datos_usuario'


class RodalProsp(models.Model):

    id = models.AutoField(primary_key=True, max_length=100)
    geom = models.GeometryField(blank=True, null=True, srid=25830)
    datosrestringidos = models.BooleanField(blank=True, null=True)
    metodo_cod = models.CharField(max_length=150)
    nombre = models.CharField(max_length=150)
    comautonom_cod = models.ForeignKey(TeProvincia, db_column='comautonom_cod', related_name='TeProvincia_comautonom_cod_RodalProsp', on_delete=models.CASCADE)
    provincia_cod = models.ForeignKey(TeProvincia, db_column='provincia_cod', related_name='TeProvincia_prvincia_cod_RodalProsp', on_delete=models.CASCADE, blank=True, null=True)
    municipio = models.CharField(max_length=150, blank=True, null=True)
    municipio1 = models.ForeignKey('TeMunicipi', models.DO_NOTHING, db_column='municipio1', blank=True, null=True)
    propietario = models.CharField(max_length=150, blank=True, null=True)
    lpeht_cod = models.ForeignKey('TeLpeht', models.DO_NOTHING, db_column='lpeht_cod')
    hic_cod = models.ForeignKey(TeHic, models.DO_NOTHING, db_column='hic_cod', blank=True, null=True)
    regbio_cod = models.ForeignKey('TeRegbio', models.DO_NOTHING, db_column='regbio_cod')
    fecha = models.DateField(blank=True, null=True)
    equipo = models.CharField(max_length=255, blank=True, null=True)
    tiempoempl = models.IntegerField(blank=True, null=True)
    tipobosque = models.CharField(max_length=150, blank=True, null=True)
    otroespflora = models.CharField(max_length=200, blank=True, null=True)
    otrohics = models.CharField(max_length=200, blank=True, null=True)
    otroinfo = models.CharField(max_length=200, blank=True, null=True)
    volarrodal = models.IntegerField(blank=True, null=True)
    valspparb = models.BooleanField()
    valmasa = models.BooleanField()
    valestratos = models.BooleanField()
    valarboexcep = models.BooleanField()
    valmmpie = models.BooleanField()
    valmmsuelo = models.BooleanField()
    valmicrohab = models.BooleanField()
    valhuecos = models.BooleanField()
    valregen = models.BooleanField()
    hhantigua = models.CharField(max_length=200, blank=True, null=True)
    hhreciente = models.CharField(max_length=200, blank=True, null=True)
    notes = models.CharField(max_length=200, blank=True, null=True)
    usuario = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='usuario')

    class Meta:
        managed = False
        db_table = 'rodal_prosp'


class WebMapaRodalProsp(models.Model):
    id_view = models.BigIntegerField(blank=True, null=True)
    id_rodal = models.IntegerField(blank=True, null=False, primary_key=True)
    geom = models.GeometryField(blank=True, null=True)
    datosrestringidos = models.BooleanField(blank=True, null=True)
    nombre = models.CharField(max_length=150, blank=True, null=True)
    ccaa_nom = models.CharField(max_length=5, blank=True, null=True)
    ccaa_nombre = models.CharField(max_length=1, blank=True, null=True)
    habitat_cod = models.CharField(max_length=10, blank=True, null=True)
    habitat_nom = models.CharField(max_length=255, blank=True, null=True)
    volarrodal = models.IntegerField(blank=True, null=True)
    tipobosque = models.CharField(max_length=1, blank=True, null=True)
    foto = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'web_mapa_Rodal_prosp'


def urlFotosProsp(instance, filename):
    #print(str(instance.id_rodal.id))
    return os.path.join("fotos_prosp", str(instance.id_rodal.id), filename)

def urlDocsProsp(instance, filename):
    return os.path.join("docs_prosp", str(instance.id_rodal.id), filename)

class FotosRodalProsp(models.Model):
    id_foto = models.AutoField(primary_key=True)
    id_rodal = models.ForeignKey('RodalProsp', models.DO_NOTHING, db_column='id_rodal')
    nombre_foto = models.CharField(max_length=200, blank=True, null=True)
    foto = models.ImageField(upload_to=urlFotosProsp)
    fotoprincipal = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'fotos_rodal_prosp'
        unique_together = (('id_foto', 'id_rodal', 'fotoprincipal'),)

    def delete(self, *args, **kwargs):
        self.foto.delete()
        super().delete(*args, **kwargs)


class DocsRodalProsp(models.Model):
    id_doc = models.AutoField(primary_key=True)
    id_rodal = models.ForeignKey('RodalProsp', models.DO_NOTHING, db_column='id_rodal')
    nombre_doc = models.CharField(max_length=200, blank=True, null=True)
    doc = models.FileField(upload_to=urlDocsProsp)

    class Meta:
        managed = False
        db_table = 'docs_rodal_prosp'
        unique_together = (('id_doc', 'id_rodal'),)


    def delete(self, *args, **kwargs):
        self.doc.delete()
        super().delete(*args, **kwargs)



class DatosGeneralesRodal(models.Model):
    id_rodal = models.IntegerField(primary_key=True)
    geom = models.GeometryField(blank=True, null=True)
    provincia = models.CharField(max_length=100, blank=True, null=True)
    com_aut = models.CharField(max_length=100, blank=True, null=True)
    nombre_rodal = models.CharField(max_length=150, blank=True, null=True)
    propietario = models.CharField(max_length=150, blank=True, null=True)
    datosrestringidos = models.BooleanField(blank=True, null=True)
    regbio_cod = models.CharField(max_length=4, blank=True, null=True)
    regbio = models.CharField(max_length=100, blank=True, null=True)
    lpeht = models.CharField(max_length=255, blank=True, null=True)
    hic = models.CharField(max_length=100, blank=True, null=True)
    lpeht_cod = models.CharField(max_length=10, blank=True, null=True)
    hic_cod = models.CharField(max_length=5, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    equipo = models.CharField(max_length=255, blank=True, null=True)
    otroespflora = models.CharField(max_length=255, blank=True, null=True)
    otrohics = models.CharField(max_length=255, blank=True, null=True)
    otroinfo = models.CharField(max_length=255, blank=True, null=True)
    municipio_id = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'datos_generales_rodal'


class RodalProspDatosgen(models.Model):
    id_rodal = models.IntegerField(primary_key=True)
    geom = models.GeometryField(blank=True, null=True)
    provincia = models.CharField(max_length=100, blank=True, null=True)
    com_aut = models.CharField(max_length=100, blank=True, null=True)
    nombre_rodal = models.CharField(max_length=150, blank=True, null=True)
    propietario = models.CharField(max_length=150, blank=True, null=True)
    datosrestringidos = models.BooleanField(blank=True, null=True)
    regbio_cod = models.CharField(max_length=10, blank=True, null=True)
    regbio = models.CharField(max_length=100, blank=True, null=True)
    lpeht = models.CharField(max_length=255, blank=True, null=True)
    hic = models.CharField(max_length=100, blank=True, null=True)
    lpeht_cod = models.CharField(max_length=10, blank=True, null=True)
    hic_cod = models.CharField(max_length=5, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    equipo = models.CharField(max_length=255, blank=True, null=True)
    otroespflora = models.CharField(max_length=255, blank=True, null=True)
    otrohics = models.CharField(max_length=255, blank=True, null=True)
    otroinfo = models.CharField(max_length=255, blank=True, null=True)
    municipio_id = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'rodal_prosp_datosgen'



class RodalProspValores(models.Model):
    id_rodal = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=150, blank=True, null=True)
    valspparb = models.BooleanField(blank=True, null=True)
    valmasa = models.BooleanField(blank=True, null=True)
    valestratos = models.BooleanField(blank=True, null=True)
    valarboexcep = models.BooleanField(blank=True, null=True)
    valmmpie = models.BooleanField(blank=True, null=True)
    valmmsuelo = models.BooleanField(blank=True, null=True)
    valmicrohab = models.BooleanField(blank=True, null=True)
    valhuecos = models.BooleanField(blank=True, null=True)
    valregen = models.BooleanField(blank=True, null=True)
    volarrodal = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'rodal_prosp_valores'


class Parcelaifn3Valorres(models.Model):
    id = models.IntegerField(primary_key=True)
    lpeht_cod = models.CharField(max_length=50, blank=True, null=True)
    calidadesta = models.IntegerField(blank=True, null=True)
    regbio_cod = models.CharField(max_length=4, blank=True, null=True)
    comautonom_cod = models.CharField(max_length=5, blank=True, null=True)
    fccarborea = models.IntegerField(blank=True, null=True)
    abtotal = models.FloatField(blank=True, null=True)
    tipobosque = models.IntegerField(blank=True, null=True)
    nivel = models.CharField(max_length=100, blank=True, null=True)
    indicador_cod = models.TextField(blank=True, null=True)
    version_calidadesta = models.IntegerField(blank=True, null=True)
    version_metrica = models.IntegerField(blank=True, null=True)
    version_indicador = models.IntegerField(blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    indic_null = models.FloatField(blank=True, null=True)
    parent_cod = models.CharField(max_length=2, blank=True, null=True)
    dato = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'parcelaifn3_valorres'
        unique_together = (('id', 'indicador_cod'))

class RodalValorres(models.Model):
    id = models.IntegerField(primary_key=True)
    lpeht_cod = models.CharField(max_length=10, blank=True, null=True)
    calidadesta = models.IntegerField(blank=True, null=True)
    regbio_cod = models.CharField(max_length=4, blank=True, null=True)
    comautonom_cod = models.CharField(max_length=2, blank=True, null=True)
    nivel = models.CharField(max_length=100, blank=True, null=True)
    indicador_cod = models.TextField(blank=True, null=True)
    version_calidadesta = models.IntegerField(blank=True, null=True)
    version_metrica = models.IntegerField(blank=True, null=True)
    version_indicador = models.IntegerField(blank=True, null=True)
    valor = models.FloatField(blank=True, null=True)
    indic_null = models.FloatField(blank=True, null=True)
    parent_cod = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        #db_table = 'rodal_valorres'
        db_table = u'"ifn\".\"rodal_valorres"'
        unique_together = (('id', 'indicador_cod'))
