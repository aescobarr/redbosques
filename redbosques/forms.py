from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.forms import DateTimeField
from bootstrap_datepicker_plus import DatePickerInput
from redbosques_main.models import Rodal, Tesaurus, TeProvincia, Habitat, TeLpeht, TeHic, TeRegbio, TeTaxon, TeCategoria, TeIndicador, FotosRodal, DocsRodal, TeMunicipi, RodalProsp, FotosRodalProsp, DocsRodalProsp
from redbosques_main import validators
from django.core.exceptions import ValidationError
from bootstrap_datepicker.widgets import DatePicker
from django.contrib import messages
from redbosques.settings import MAX_UPLOAD_SIZE, MAX_UPLOAD_DOC_SIZE
import itertools
from django.forms import Textarea

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
            raise forms.ValidationError('Has introducido dos passwords diferentes. Por favor, vuelve a intentarlo')

        return password


    def clean_email(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe un usuario registrado con este correo-e. Por favor, elige otro.')
        return email

    '''
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
            'placeholder': 'Nombre de usuario'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control password',
            'placeholder':'Contraseña'}
    ))


class rodalFormFields(forms.ModelForm):

    datosrestringidos = forms.BooleanField(widget=forms.CheckboxInput(attrs={'id': 'datosRestringidos'}), required=False)
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del rodal'}), required=True)
    propietario = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Propietario'}), required=True)
    metodos = Tesaurus.objects.filter().order_by('cod', 'nombre_es')
    metodo_cod = forms.ModelChoiceField(queryset=metodos, widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Método", required=True)
    fecha = forms.DateField(label="Fecha", widget=DatePickerInput(format='%d/%m/%Y', attrs={'placeholder': 'Fecha'}))
    equipo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Equipo de campo'}), required=True)

    habLPEHT = TeLpeht.objects.filter(seleccion='True').filter(cod__contains='.').order_by('nombre')
    lpeht_cod = forms.ModelChoiceField(queryset=habLPEHT, widget=forms.Select(attrs={'class': 'form-control', 'value': ''}), empty_label="Hábitat CORINE (LPHE)", required=True)


    habitatsHIC = TeHic.objects.order_by('nombre_es')
    hic_cod = forms.ModelChoiceField(queryset=habitatsHIC, widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Hábitat de interés comunitario HIC", required=True)
    regionesBiogeo = TeRegbio.objects.order_by('nombre_es')
    regbio_cod = forms.ModelChoiceField(queryset=regionesBiogeo, widget=forms.Select(attrs={'class': 'form-control'}),empty_label="Región biogeográfica", required=True)
    especies = TeTaxon.objects.order_by('nombre')
    espprinc_cod = forms.ModelChoiceField(queryset=especies, widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Especie principal", required=True)
    espprincip_h0 = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control alturaDominanteEspeciePrincipal', 'id': 'altDomEspPrin'}), required=True)
    espprinc_fcc = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control alturaDominanteEspeciePrincipalAcomp dotDel', 'id': 'cavCubespPrin'}), required=True)

    espcomp_cod = forms.ModelChoiceField(queryset=especies, widget=forms.Select(attrs={'class': 'form-control', 'onchange':'disEnEspecieAcomp()'}), empty_label="Principal especie acompañante", required=False)
    espcomp_h0 = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control alturaDominanteEspeciePrincipalAcomp', 'id': 'altDomEspPrinAcomp'}), required=False)
    espcomp_fcc = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control alturaDominanteEspeciePrincipalAcomp dotDel', 'id': 'cavCubespPrinAcomp'}), required=False)

    # municipio1 = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control id_municipio', 'type': 'hidden', 'value': ''}))
    # comautonom_cod = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control id_comAutonoma', 'type': 'hidden', 'value': ''}), required=True)
    # provincia_cod = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control id_provincia', 'type': 'hidden', 'value': ''}), required=True)



    def clean_espcomp_cod(self):
        cleaned_data = self.cleaned_data
        espcomp_cod_val = cleaned_data.get('espcomp_cod')
        espcomp_h0_val = cleaned_data.get('espcomp_h0')
        espcomp_fcc_val = cleaned_data.get('espcomp_fcc')

        if espcomp_cod_val is None:
            print("No se ha seleccionado nada")
        else:
            return espcomp_cod_val



    def clean_lpeht_cod(self):
        cleaned_data = self.cleaned_data
        lpeht_cod_nombre = cleaned_data.get('lpeht_cod')
        #print(type(lpeht_cod_nombre).__name__)
        lpeht_cod_val = TeLpeht.objects.get(cod=lpeht_cod_nombre.cod, seleccion=True)
        #lpeht_cod_val = TeLpeht.objects.get(nombre=lpeht_cod_nombre, seleccion=True)

        return lpeht_cod_val



    def clean_espprincip_h0(self):
        cleaned_data = self.cleaned_data
        espprincip_h0_val = cleaned_data.get('espprincip_h0')

        espprincip_h0 = TeIndicador.objects.get(variable_rodal='espprincip_h0')

        if isinstance(espprincip_h0_val, float):
            raise ValidationError("El valor tiene que ser un número entero.")
        else:
            if espprincip_h0_val < espprincip_h0.val_minimo:
                raise ValidationError('El valor es inferior al permitido. valores permitidos(' + str(espprincip_h0.val_minimo) + '-' + str(espprincip_h0.val_maximo) + ')')
            elif espprincip_h0_val > espprincip_h0.val_maximo:
                raise ValidationError("El valor es mayor al permitido.")
            else:
                return espprincip_h0_val



    def clean_espprinc_fcc(self):
        cleaned_data = self.cleaned_data
        espprinc_fcc_val = cleaned_data.get('espprinc_fcc')
        espprinc_fcc = TeIndicador.objects.get(variable_rodal='espprinc_fcc')

        if espprinc_fcc_val < espprinc_fcc.val_minimo:
            raise ValidationError("El valor es inferior al permitido.")
        elif espprinc_fcc_val > espprinc_fcc.val_maximo:
            raise ValidationError("El valor es mayor al permitido.")
        else:
            return espprinc_fcc_val


    def clean_espcomp_fcc(self):
        cleaned_data = self.cleaned_data
        espcomp_fcc_val = cleaned_data.get('espcomp_fcc')
        espprinc_fcc_val = cleaned_data.get('espprinc_fcc')
        espcomp_cod_val = cleaned_data.get('espcomp_cod')

        if espcomp_fcc_val is None and espcomp_cod_val is not None:
            raise ValidationError("El campo de Altura dominante de la principal especie acompañante es obligatorio")
        elif espcomp_fcc_val is not None and espprinc_fcc_val is not None:
            if((espcomp_fcc_val + espprinc_fcc_val) <= 100 ):
                espcomp_fcc = TeIndicador.objects.get(variable_rodal='espcomp_fcc')

                if espcomp_fcc_val < espcomp_fcc.val_minimo:
                    raise ValidationError("El valor es inferior al permitido.")
                elif espcomp_fcc_val > espcomp_fcc.val_maximo:
                    raise ValidationError("El valor es mayor al permitido.")
                else:
                    return espcomp_fcc_val
            else:
                raise ValidationError("La suma del porcentaje de cavidad cubierta de la especie principal i de la especie acompañante no puede sumar mas de 100%.")

            #raise ValidationError("Los valores introducidos no son correctos.")


    def clean_espcomp_h0(self):
        cleaned_data = self.cleaned_data
        espcomp_h0_val = cleaned_data.get('espcomp_h0')
        espcomp_cod_val = cleaned_data.get('espcomp_cod')

        espcomp_h0 = TeIndicador.objects.get(variable_rodal='espcomp_h0')

        if espcomp_h0_val is None and espcomp_cod_val is not None:
            raise ValidationError("El campo de Altura dominante de la principal especie acompañante es obligatorio")
        elif isinstance(espcomp_h0_val, float):
            raise ValidationError("El valor tiene que ser un número entero.")
        elif espcomp_h0_val is not None:
            if espcomp_h0_val < espcomp_h0.val_minimo:
                raise ValidationError("El valor es inferior al permitido.")
            elif espcomp_h0_val > espcomp_h0.val_maximo:
                raise ValidationError("El valor es mayor al permitido.")
            else:
                return espcomp_h0_val



    class Meta:
        model = Rodal
        fields = ('datosrestringidos', 'nombre', 'comautonom_cod', 'provincia_cod', 'propietario', 'metodo_cod',
                  'fecha', 'equipo', 'lpeht_cod', 'hic_cod', 'regbio_cod', 'espprinc_cod', 'espcomp_cod',
                  'espprincip_h0', 'espcomp_h0', 'espprinc_fcc', 'espcomp_fcc', 'municipio1')
        widgets = {
            'comautonom_cod': forms.HiddenInput(),
            'provincia_cod': forms.HiddenInput(),
            'municipio1': forms.HiddenInput()
        }


class rodalFormFields2(forms.ModelForm):

    numesparb = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control numEspArbDos'}), required=True)
    areabasal = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control numEspArbDos dotDel'}), required=True)
    volmadvivo = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control numEspArbDos calculo dotDel'}), required=True)
    numestratos = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control numEspArbDos dotDel'}), required=True)
    numclasdiam = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control numEspArbDos'}), required=True)
    abundpiesexcep = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control numEspArbDos dotDel'}), required=True)
    volmmpie = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control numEspArbDos calculo dotDel'}), required=True)
    volmmsuelo = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control numEspArbDos calculo dotDel'}), required=True)
    volmmprop = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control numEspArbDos'}), required=True)
    volmmtotal = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control numEspArbDos dotDel'}), required=True)
    nummicrohab = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control numEspArbDos'}), required=True)
    numfasessil = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control numEspArbDos'}), required=True)
    rodalref = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'boolRodRef'}), required=False)




    # valagropasant = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control id_valagropasant', 'type':'hidden', 'value': ''}), required=True)
    # valforestant = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control id_valforestant', 'type': 'hidden', 'value': ''}), required=True)
    # valforestrec = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control id_valforestrec', 'type': 'hidden', 'value': ''}), required=True)
    # valespinvas = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control id_valespinvas', 'type': 'hidden', 'value': ''}), required=True)
    # valfragment = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control id_valfragment', 'type': 'hidden', 'value': ''}), required=True)
    # valcaza = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control id_valcaza', 'type': 'hidden', 'value': ''}), required=True)
    # valherbiv = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control id_valherbiv', 'type': 'hidden', 'value': ''}), required=True)
    # valdurabusos = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control id_valdurabusos', 'type': 'hidden', 'value': ''}), required=True)
    # valfrecuent = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control id_valfrecuent', 'type': 'hidden', 'value': ''}), required=True)
    # valpropbosc56 = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control id_valpropbosc56', 'type': 'hidden', 'value': ''}), required=True)'''




    def clean_numesparb(self):
        cleaned_data = self.cleaned_data
        numesparb_val = cleaned_data.get('numesparb')

        numesparb1 = TeIndicador.objects.get(variable_rodal='numesparb')

        if numesparb_val < numesparb1.val_minimo:
            raise ValidationError("El valor es inferior al permitido.")
        elif numesparb_val > numesparb1.val_maximo:
            raise ValidationError("El valor es mayor al permitido.")
        else:
            return numesparb_val

    def clean_areabasal(self):
        cleaned_data = self.cleaned_data
        areabasal_val = cleaned_data.get('areabasal')

        areabasal = TeIndicador.objects.get(variable_rodal='areabasal')

        if areabasal_val < areabasal.val_minimo:
            raise ValidationError("El valor es inferior al permitido.")
        elif areabasal_val > areabasal.val_maximo:
            raise ValidationError("El valor es mayor al permitido.")
        else:
            return areabasal_val

    def clean_volmadvivo(self):
        cleaned_data = self.cleaned_data
        volmadvivo_val = cleaned_data.get('volmadvivo')

        volmadvivo = TeIndicador.objects.get(variable_rodal='volmadvivo')

        if volmadvivo_val < volmadvivo.val_minimo:
            raise ValidationError("El valor es inferior al permitido.")
        else:
            return volmadvivo_val

    def clean_numestratos(self):
        cleaned_data = self.cleaned_data
        numestratos_val = cleaned_data.get('numestratos')

        numestratos = TeIndicador.objects.get(variable_rodal='numestratos')

        if numestratos_val < numestratos.val_minimo:
            raise ValidationError("El valor es inferior al permitido.")
        elif numestratos_val > numestratos.val_maximo:
            raise ValidationError("El valor es mayor al permitido.")
        else:
            return numestratos_val

    def clean_numclasdiam(self):
        cleaned_data = self.cleaned_data
        numclasdiam_val = cleaned_data.get('numclasdiam')

        numclasdiam = TeIndicador.objects.get(variable_rodal='numclasdiam')

        if numclasdiam_val < numclasdiam.val_minimo:
            raise ValidationError("El valor es inferior al permitido.")
        elif numclasdiam_val > numclasdiam.val_maximo:
            raise ValidationError("El valor es mayor al permitido.")
        else:
            return numclasdiam_val

    def clean_abundpiesexcep(self):
        cleaned_data = self.cleaned_data
        abundpiesexcep_val = cleaned_data.get('abundpiesexcep')

        abundpiesexcep = TeIndicador.objects.get(variable_rodal='abundpiesexcep')

        if abundpiesexcep_val < abundpiesexcep.val_minimo:
            raise ValidationError("El valor es inferior al permitido.")
        elif abundpiesexcep_val > abundpiesexcep.val_maximo:
            raise ValidationError("El valor es mayor al permitido.")
        else:
            return abundpiesexcep_val

    def clean_volmmpie(self):
        cleaned_data = self.cleaned_data
        volmmpie_val = cleaned_data.get('volmmpie')

        volmmpie = TeIndicador.objects.get(variable_rodal='volmmpie')

        if volmmpie_val < volmmpie.val_minimo:
            raise ValidationError("El valor es inferior al permitido.")
        elif volmmpie_val > volmmpie.val_maximo:
            raise ValidationError("El valor es mayor al permitido.")
        else:
            return volmmpie_val

    def clean_volmmsuelo(self):
        cleaned_data = self.cleaned_data
        volmmsuelo_val = cleaned_data.get('volmmsuelo')

        volmmsuelo = TeIndicador.objects.get(variable_rodal='volmmsuelo')

        if volmmsuelo_val < volmmsuelo.val_minimo:
            raise ValidationError("El valor es inferior al permitido.")
        elif volmmsuelo_val > volmmsuelo.val_maximo:
            raise ValidationError("El valor es mayor al permitido.")
        else:
            return volmmsuelo_val

    def clean_volmmtotal(self):
        cleaned_data = self.cleaned_data
        volmmtotal_val = cleaned_data.get('volmmtotal')

        volmmtotal = TeIndicador.objects.get(variable_rodal='volmmtotal')

        if volmmtotal_val < volmmtotal.val_minimo:
            raise ValidationError("El valor es inferior al permitido.")
        elif volmmtotal_val > volmmtotal.val_maximo:
            raise ValidationError("El valor es mayor al permitido.")
        else:
            return volmmtotal_val

    def clean_volmmprop(self):
        cleaned_data = self.cleaned_data
        volmmprop_val = cleaned_data.get('volmmprop')

        volmmprop=TeIndicador.objects.get(variable_rodal='volmmprop')

        if volmmprop_val < volmmprop.val_minimo:
            raise ValidationError("El valor es inferior al permitido.")
        elif volmmprop_val > volmmprop.val_maximo:
            raise ValidationError("El valor es mayor al permitido.")
        else:
            return volmmprop_val


    def clean_nummicrohab(self):
        cleaned_data = self.cleaned_data
        nummicrohab_val = cleaned_data.get('nummicrohab')

        nummicrohab = TeIndicador.objects.get(variable_rodal='nummicrohab')

        if nummicrohab_val < nummicrohab.val_minimo:
            raise ValidationError("El valor es inferior al permitido.")
        elif nummicrohab_val > nummicrohab.val_maximo:
            raise ValidationError("El valor es mayor al permitido.")
        else:
            return nummicrohab_val


    def clean_numfasessil(self):
        cleaned_data = self.cleaned_data
        numfasessil_val = cleaned_data.get('numfasessil')

        numfasessil=TeIndicador.objects.get(variable_rodal='numfasessil')

        if numfasessil_val < numfasessil.val_minimo:
            raise ValidationError("El valor es inferior al permitido.")
        elif numfasessil_val > numfasessil.val_maximo:
            raise ValidationError("El valor es mayor al permitido.")
        else:
            return numfasessil_val


    class Meta:
        model = Rodal
        fields = ('numesparb', 'areabasal', 'volmadvivo', 'numestratos', 'numclasdiam', 'abundpiesexcep', 'volmmpie',
                  'volmmsuelo', 'volmmprop', 'nummicrohab', 'numfasessil', 'valagropasant', 'valforestant', 'valpropbosc56',
                  'valforestrec', 'valespinvas', 'valfragment', 'valcaza', 'valherbiv', 'valfrecuent', 'valdurabusos',
                  'rodalref', 'volmmtotal')

        widgets = {
            'valagropasant': forms.HiddenInput(),
            'valforestant': forms.HiddenInput(),
            'valforestrec': forms.HiddenInput(),
            'valespinvas': forms.HiddenInput(),
            'valfragment': forms.HiddenInput(),
            'valcaza': forms.HiddenInput(),
            'valherbiv': forms.HiddenInput(),
            'valdurabusos': forms.HiddenInput(),
            'valfrecuent': forms.HiddenInput(),
            'valpropbosc56': forms.HiddenInput()

        }


class rodalFormFields3(ModelForm):
    otroespflora = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Otras especies de flora acompañantes', 'cols': 67, 'rows': 3}), required=False)
    otrohics = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Otras hábitats de interés comunitario (arbolaos o no)', 'cols': 67, 'rows': 3}), required=False)
    otroinfo = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Otra información relevante', 'cols': 67, 'rows': 3}), required=False)

    class Meta:
        model = Rodal
        fields = ('otroespflora', 'otrohics', 'otroinfo')


class rodalFormFields3Foto(ModelForm):
    class Meta:
        model = FotosRodal
        fields = ('foto', )

    def clean_foto(self):
        foto = self.cleaned_data.get('foto', False)
        if foto:
            if foto.size > MAX_UPLOAD_SIZE:
                raise ValidationError("Imagen demasiado grande ( > 2mb )")
            return foto
        else:
            raise ValidationError("No se pudo leer la imagen cargada")


class rodalFormFields3Fotoprincipal(ModelForm):
    class Meta:
        model = FotosRodal
        fields = ('fotoprincipal', )


class rodalFormFields3Doc(ModelForm):
    class Meta:
        model = DocsRodal
        fields = ('doc', )

    def clean_doc(self):
        doc = self.cleaned_data.get('doc', False)
        maxSize = (MAX_UPLOAD_DOC_SIZE /1024)/1024
        if doc:
            if doc.size > MAX_UPLOAD_DOC_SIZE:
                raise ValidationError("El documento es demasiado grande ( > " + str(maxSize) + " mb )")
                #raise ValidationError("El documento es demasiado grande ( > 2 mb )")
            return doc
        else:
            raise ValidationError("No se pudo leer el documento cargado")


class rodalFormFase1Fields(ModelForm):
    datosrestringidos = forms.BooleanField(widget=forms.CheckboxInput(attrs={'id': 'datosRestringidos'}), required=False)
    metodos = Tesaurus.objects.filter().order_by('cod', 'nombre_es')
    metodo_cod = forms.ModelChoiceField(queryset=metodos, widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Método", required=False)
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del rodal'}), required=True)
    propietario = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Propietario'}), required=True)
    habLPEHT = TeLpeht.objects.filter(seleccion='True').filter(cod__contains='.').order_by('nombre')
    lpeht_cod = forms.ModelChoiceField(queryset=habLPEHT, widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Hábitat CORINE (LPHE)", required=True)
    habitatsHIC = TeHic.objects.order_by('nombre_es')
    hic_cod = forms.ModelChoiceField(queryset=habitatsHIC, widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Hábitat de interés comunitario HIC", required=True)
    regionesBiogeo = TeRegbio.objects.order_by('nombre_es')
    regbio_cod = forms.ModelChoiceField(queryset=regionesBiogeo, widget=forms.Select(attrs={'class': 'form-control'}),empty_label="Región biogeográfica", required=True)
    fecha = forms.DateField(label="Fecha", widget=DatePickerInput(format='%d/%m/%Y', attrs={'placeholder': 'Fecha'}),required=False)
    equipo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Equipo de campo'}), required=True)
    tiempoempl = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tiempo empleado'}), required=False)
    tipobosque = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'Tipo de bosque: Descripción de las características de madurez'}), required=False)
    otroespflora = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}), required=False)
    otrohics = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}), required=False)
    otroinfo = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}), required=False)
    #hhantigua = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}), required=False)
    #hhreciente = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}), required=False)


    class Meta:
        model = RodalProsp
        fields = ('datosrestringidos', 'metodo_cod', 'nombre', 'comautonom_cod', 'provincia_cod', 'municipio',
                  'municipio1', 'propietario', 'lpeht_cod', 'hic_cod', 'regbio_cod', 'fecha', 'equipo', 'tiempoempl',
                  'tipobosque', 'otroespflora', 'otrohics', 'otroinfo', 'valspparb','valmasa', 'valestratos',
                  'valarboexcep', 'valmmpie', 'valmmsuelo', 'valmicrohab', 'valhuecos', 'valregen', 'hhantigua',
                  'volarrodal', 'hhreciente', 'notes')

        widgets = {
            'comautonom_cod': forms.HiddenInput(),
            'provincia_cod': forms.HiddenInput(),
            'municipio1': forms.HiddenInput(),
            'valspparb': forms.HiddenInput(),
            'valmasa' : forms.HiddenInput(),
            'valestratos': forms.HiddenInput(),
            'valarboexcep': forms.HiddenInput(),
            'valmmpie': forms.HiddenInput(),
            'valmmsuelo': forms.HiddenInput(),
            'valmicrohab': forms.HiddenInput(),
            'valhuecos': forms.HiddenInput(),
            'valregen': forms.HiddenInput(),
            'hhantigua': forms.HiddenInput(),
            'hhreciente': forms.HiddenInput(),
            'volarrodal': forms.HiddenInput(),
        }


class rodalFormFieldsFase1Foto(ModelForm):
    class Meta:
        model = FotosRodalProsp
        fields = ('foto', )

    def clean_foto(self):
        foto = self.cleaned_data.get('foto', False)
        if foto:
            if foto.size > MAX_UPLOAD_SIZE:
                raise ValidationError("Imagen demasiado grande ( > 2mb )")
            return foto
        else:
            raise ValidationError("No se pudo leer la imagen cargada")


class rodalFormFieldsFase1Fotoprincipal(ModelForm):
    class Meta:
        model = FotosRodalProsp
        fields = ('fotoprincipal', )


class rodalFormFieldsFase1Doc(ModelForm):
    class Meta:
        model = DocsRodalProsp
        fields = ('doc', )

    def clean_doc(self):
        doc = self.cleaned_data.get('doc', False)
        maxSize = (MAX_UPLOAD_DOC_SIZE /1024)/1024
        if doc:
            if doc.size > MAX_UPLOAD_DOC_SIZE:
                raise ValidationError("El documento es demasiado grande ( > " + str(maxSize) + " mb )")
                #raise ValidationError("El documento es demasiado grande ( > 2 mb )")
            return doc
        else:
            raise ValidationError("No se pudo leer el documento cargado")