from django import forms
from django.forms import ModelForm
from redbosques_main.models import Rodal
#from datetimewidget.widgets import DateWidget, TimeWidget


'''class rodalFormFields(ModelForm):
    geometria = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    #datosrestringidos = forms.BooleanField(widget=forms.BooleanField(attrs={'class': 'form-control'}), required=True)
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    comautonom_cod = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    provincia_cod = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    municipio = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    propietario = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    #fecha = forms.DateField(input_formats=['%d/%m/%Y'],widget=DateTimeInput(bootstrap_version=3, options=dateTimeOptions))
    equipo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    lpeht = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    hic = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    regbio = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    espprinc_cod = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    espcomp_cod = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    espprinc_h0 = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    espcomp_h0 = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    numesparb = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    areabasal = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    volmadvivo = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    numestratos = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    numclasdiam = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    abundpiesexcep = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    volmmpie = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    volmmsuelo = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    volmmprop = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    nummicrohab = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    numfasessil = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    valagropasant = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    valforestant = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    valforestrec = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    valespinvas = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    valfragment = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    valcaza = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    valherbiv = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    valfrecuent = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    valdurabusos = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    otroespflora = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    otrohics = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    otroinfo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    usuario = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    rodalref = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    #fotoglobo = forms.FileInput(widget=forms.FileInput(attrs={'class': 'form-control'}), required=True)
    espprinc_fcc = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    espcomp_fcc = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)


    class Meta:
        model: Rodal
        fields = ('geom', 'datosrestringidos', 'nombre',
                  'comautonom_cod', 'provincia_cod', 'municipio',
                  'propietario', 'fecha', 'equipo', 'lpeht_cod',
                  'hic_cod', 'regbio_cod', 'espprinc_cod',
                  'espcomp_cod', 'espprincip_h0', 'espcomp_h0', 'numesparb',
                  'areabasal', 'volmadvivo', 'numestratos', 'numclasdiam', 'abundpiesexcep',
                  'volmmpie', 'volmmsuelo', 'volmmprop', 'nummicrohab', 'numfasessil',
                  'valagropasant', 'valforestant', 'valforestrec', 'valespinvas', 'valfragment',
                  'valcaza', 'valherbiv', 'valfrecuent', 'valdurabusos', 'otroespflora', 'otrohics', 'otroinfo',
                  'usuario', 'rodalref', 'fotoglobo', 'espprinc_fcc', 'espcomp_fcc')



'''
