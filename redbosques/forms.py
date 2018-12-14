from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms import DateTimeField
#from datetimewidget.widgets import DateWidget, TimeWidget
from redbosques_main.models import Rodal, Tesaurus

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


class rodalFormFields(forms.ModelForm):
    geometria = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    #datosrestringidos = forms.BooleanField(widget=forms.BooleanField(attrs={'class': 'form-control'}), required=True)
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del rodal'}), required=True)
    comautonom_cod = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    provincia_cod = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    municipio = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Termino municipal'}), required=True)
    propietario = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Propietario'}), required=True)
    fecha = forms.DateField(widget=forms.widgets.TextInput(attrs={'class': 'datepicker'}))

    #fecha = forms.DateField(widget=DatePicker())

    equipo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Equipo de campo'}), required=True)
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
    otroespflora = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Otras especies de flora acompañante'}), required=True)
    otrohics = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Otras hábitats de interés comunitario'}), required=True)
    otroinfo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Otra información relevantek'}), required=True)
    usuario = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    rodalref = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    #fotoglobo = forms.FileInput(widget=forms.FileInput(attrs={'class': 'form-control'}), required=True)
    espprinc_fcc = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    espcomp_fcc = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)

    met = Tesaurus.objects.filter().order_by('nombre_es')
    metodos = []
    for m in met:
        metodos.append({m.nombre_es, m.cod})
    meto = [('null', 'Selecciona método')] + metodos

    metodo_cod = forms.ChoiceField(choices=meto,widget=forms.Select(attrs={'class': 'form-control'}))

    # viento_inicio = forms.ChoiceField(choices=CHOICES_WIND,widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Rodal
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


