from rest_framework import serializers
from redbosques_main.models import DatosUsuario, Institucion
from django.contrib.auth.models import User

class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'is_active')


class DatosUsuarioSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    institucion = InstitucionSerializer()
    class Meta:
        model = DatosUsuario
        fields = '__all__'