from rest_framework import serializers
from .models import Responsaveis, Locais, Ambientes, Sensores, Historico



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

