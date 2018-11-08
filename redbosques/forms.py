from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


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

