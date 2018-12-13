from django import forms
from django.forms import ModelForm
from redbosques_main.models import Rodal


class rodalForm(ModelForm):
    '''geometria = forms.CharField(label='geom')
    datosRestringidos = forms.BooleanField(label='restData')
    nombre = forms.CharField(label='nombre', max_length=150)
    comAut = forms.CharField(label='comAut')
    provincia = forms.CharField(label="provCod")
    municipio = forms.CharField(label="municipio")
    propietario = forms.CharField(label="propietario")
    fecha = forms.DateInput(label="fecha")
    equipo = forms.CharField(label="equipo")
    lpeht = forms.CharField(label="lpeht_cod")
    hic = forms.CharField(label="hic_cod")
    regbio = forms.CharField(label="regbio_cod")
    espprinc_cod = forms.CharField(label="espprinc_cod")
    espcomp_cod = forms.CharField(label="espcomp_cod")
    espprinc_h0 = forms.CharField(label="espprinc_h0")
    espcomp_h0 = forms.CharField(label="espcomp_cod_h0")'''

    class Meta:
        model: Rodal
        fields = ['geom','datosrestringidos', 'nombre',
                  'comautonom_cod', 'provincia_cod', 'municipio',
                  'propietario', 'fecha', 'equipo', 'lpeht_cod',
                  'hic_cod', 'regbio_cod', 'espprinc_cod',
                  'espcomp_cod', 'espprincip_h0', 'espcomp_h0' ]




