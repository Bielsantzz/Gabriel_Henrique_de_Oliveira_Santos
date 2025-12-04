from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from .models import Responsaveis, Locais, Sensores, Ambientes, Historico

########## para cadastro #############


class ResponsaveisSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Responsaveis
        fields = '__all__'

class LocaisSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Locais
        fields = '__all__'

class SensoresSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Sensores
        fields = '__all__'

class AmbientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ambientes
        fields = '__all__' 
        
class HistoricoSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Sensores
        fields = '__all__'

class HistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Historico
        fields = '__all__' 
        
# === ADICIONE: serializer de registro de usuário ===
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Usuário já existe.")]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password],
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )