from rest_framework import serializers
from .models import Responsaveis, Locais, Ambientes, Sensores, Historico
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator


class ResponsaveisSerializers(serializers.ModelSerializer):
    class Meta:
        model = Responsaveis
        fields = '__all__'

class LocaisSerializers(serializers.ModelSerializer):
    class Meta:
        model = Locais
        fields = '__all__'

class AmbientesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ambientes
        fields = '__all__'

class SensoresSerializers(serializers.ModelSerializer):
    class Meta:
        model = Sensores
        fields = '__all__'

class HistoricoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Historico
        fields = '__all__'


User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all(),message="Este Usuário já existe")]
    )
    password =serializers.CharField(
        write_only = True, required = True, validators = [validate_password],
        style ={'input_type': 'password'}
    )


    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def create(self,validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )