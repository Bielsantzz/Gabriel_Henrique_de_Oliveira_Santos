from rest_framework import viewsets
from .models import Responsaveis, Locais, Ambientes, Sensores, Historico
from .serializers import (ResponsaveisSerializer,LocaisSerializer,AmbientesSerializer,SensoresSerializer,
                          SensoresCreateSerializer,HistoricoSerializer,HistoricoCreateSerializer)
# Create your views here.


class ResponsaveisViewSet(viewsets.ModelViewSet):
    queryset = Responsaveis.objects.all()
    serializer_class = ResponsaveisSerializer


class LocaisViewSet(viewsets.ModelViewSet):
    queryset = Locais.objects.all()
    serializer_class = LocaisSerializer

class AmbientesViewSet(viewsets.ModelViewSet):
    queryset = Ambientes.objects.all()
    serializer_class = AmbientesSerializer

class SensoresViewSet(viewsets.ModelViewSet):
    queryset = Sensores.objects.all()
    serializer_class = SensoresSerializer

class HistoricoViewSet(viewsets.ModelViewSet):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer
    
class AmbienteViewSet(viewsets.ModelViewSet):
    queryset = Ambientes.objects.all()
    serializer_class = AmbientesSerializer

class AmbienteViewSet(viewsets.ModelViewSet):
    queryset = Ambientes.objects.all()
    serializer_class = AmbientesSerializer
