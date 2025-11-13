from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Responsaveis, Locais, Ambientes, Sensores, Historico
from .serializers import (ResponsaveisSerializers,LocaisSerializers,
                          SensoresSerializers,HistoricoSerializers,AmbientesSerializers,)



class ResponsaveisViewSet(viewsets.ModelViewSet):
    queryset = Responsaveis.objects.all()
    serializer_class = ResponsaveisSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['respnsavel']
    permission_classes =[IsAuthenticated]
    

class LocaisViewSet(viewsets.ModelViewSet):
    queryset = Locais.objects.all()
    serializer_class = LocaisSerializers
    filter_backends = [DjangoFilterBackend,SearchFilter]
    search_fields = ['local']
    permission_classes = [IsAuthenticated]

class SensoresViewSet(viewsets.ModelViewSet):
    queryset = Sensores.objects.all()
    serializer_class = SensoresSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['sensor', 'mac_address']
    permission_classes = [IsAuthenticated]

class HistoricoViewSet(viewsets.ModelViewSet):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = []
    
class AmbientesViewSet(viewsets.ModelViewSet):
    queryset = Ambientes.objects.all()
    serializer_class = AmbientesSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['descricao']



