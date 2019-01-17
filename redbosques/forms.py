from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms import DateTimeField
from bootstrap_datepicker_plus import DatePickerInput
from redbosques_main.models import Rodal, Tesaurus, TeProvincia, Habitat, TeLpeht, TeHic, TeRegbio, TeTaxon

from bootstrap_datepicker.widgets import DatePicker

#from django.utils.translation import gettext as _


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control email', 'placeholder':'Nombre'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control email' , 'placeholder':'Apellidos'}), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control email', 'placeholder':'Correo electrónico'}), required=True)
    #username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control email', 'placeholder':'Nombre de usuairo'}))
    username = forms.HiddenInput()
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control email', 'placeholder':'Contraseña'}), required=True)
    #password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control email', 'placeholder':'Repita la contraseña'}), required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

    def clean_password(self):
        cleaned_data = self.cleaned_data
        password_2 = self.data['password_2']
        password = cleaned_data.get('password')
        if password != password_2:
            raise forms.ValidationError('Los passwords son diferentes\'ls')

        return password

    '''
    def clean_email(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get('email')
        return email


    def clean_username(self):
        cleaned_data = self.cleaned_data
        #username = self.data['username']
        email_username = cleaned_data.get('email')
        username = email_username
        return username
    '''

    '''def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = user.email

        if commit:
            user.save()

        return user'''


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control email',
            'placeholder':'Nombre de usuairo'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control password',
            'placeholder':'Contraseña'}
    ))


class rodalFormFields(ModelForm):
    datosrestringidos = forms.BooleanField(widget=forms.CheckboxInput(attrs={'id': 'datosRestringidos'}), required=False)
    #tipos Muestreo
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del rodal'}), required=True)

    municipio = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Termino municipal'}), required=True)
    propietario = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Propietario'}), required=True)
    #geom = forms.CharField(widget=forms.TextInput(attrs={'id': 'geometria', 'name': 'geometria', 'type': 'hidden'}), required=True)
    #geom = forms.CharField(widget=forms.TextInput(),required=True)
    fecha = forms.DateField(label="Fecha", widget=DatePickerInput(format='%d/%m/%Y', attrs={'placeholder': 'Fecha'}))
    equipo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Equipo de campo'}), required=True)
    #espprinc_cod = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    #espcomp_cod = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    espprincip_h0 = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control alturaDominanteEspeciePrincipal', 'id': 'altDomEspPrin'}), required=True)
    espcomp_h0 = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control alturaDominanteEspeciePrincipalAcomp', 'id': 'altDomEspPrinAcomp'}), required=True)
    espprinc_fcc = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control alturaDominanteEspeciePrincipalAcomp', 'id': 'cavCubespPrin'}), required=True)
    espcomp_fcc = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control alturaDominanteEspeciePrincipalAcomp', 'id': 'cavCubespPrinAcomp'}), required=True)
    #usuario = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    metodos = Tesaurus.objects.filter().order_by('cod', 'nombre_es')
    metodo_cod = forms.ModelChoiceField(queryset=metodos, widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Método", required=True )

    comunidades = TeProvincia.objects.filter(nivel='Com. autònoma').order_by('cod', 'nombre_es')
    comautonom_cod = forms.ModelChoiceField(queryset=comunidades, widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Comunidad Autónoma", required=True)

    provincias = TeProvincia.objects.filter(nivel='Província').order_by('cod', 'nombre_es')
    provincia_cod = forms.ModelChoiceField(queryset=provincias, widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Provincia", required=True)

    habLPEHT = TeLpeht.objects.filter(seleccion='True').order_by('nombre')
    lpeht_cod = forms.ModelChoiceField(queryset=habLPEHT, widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Hábitat CORINE (LPHE)", required=True)

    habitatsHIC = TeHic.objects.order_by('nombre_es')
    hic_cod = forms.ModelChoiceField(queryset=habitatsHIC, widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Hábitat de interés comunitario HIC", required=True)

    regionesBiogeo = TeRegbio.objects.order_by('nombre_es')
    regbio_cod = forms.ModelChoiceField(queryset=regionesBiogeo, widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Región biogeográfica", required=True)

    especies = TeTaxon.objects.order_by('nombre')
    espprinc_cod = forms.ModelChoiceField(queryset=especies, widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Especie principal", required=True)
    espcomp_cod = forms.ModelChoiceField(queryset=especies, widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Principal especie acompañante", required=True)

    #fotoglobo = forms.FileInput(widget=forms.FileInput(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = Rodal
        fields = ('datosrestringidos', 'nombre', 'comautonom_cod', 'provincia_cod', 'municipio', 'propietario',
                  'metodo_cod', 'fecha', 'equipo', 'lpeht_cod', 'hic_cod', 'regbio_cod', 'espprinc_cod', 'espcomp_cod',
                  'espprincip_h0', 'espcomp_h0', 'usuario', 'espprinc_fcc', 'espcomp_fcc')





class rodalFormFields2(ModelForm):

    numesparb = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control numEspArbDos'}), required=True)

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

    rodalref = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'boolRodRef'}), required=False)



    class Meta:
        model = Rodal
        fields = ('numesparb', 'areabasal', 'volmadvivo', 'numestratos', 'numclasdiam', 'abundpiesexcep', 'volmmpie',
                  'volmmsuelo', 'volmmprop', 'nummicrohab', 'numfasessil', 'valagropasant', 'valforestant',
                  'valforestrec', 'valespinvas', 'valfragment', 'valcaza', 'valherbiv', 'valfrecuent', 'valdurabusos',
                  'rodalref')



class rodalFormFields3(ModelForm):
    otroespflora = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Otras especies de flora acompañante', 'cols': 67, 'rows': 3}), required=False)
    otrohics = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Otras hábitats de interés comunitario', 'cols': 67, 'rows': 3}), required=False)
    otroinfo = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Otra información relevante', 'cols': 67, 'rows': 3}), required=False)

    class Meta:
        model = Rodal
        fields = ('otroespflora', 'otrohics', 'otroinfo')
