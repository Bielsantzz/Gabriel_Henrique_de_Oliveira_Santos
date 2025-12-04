from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, BooleanFilter
from .models import Responsaveis, Locais, Ambientes, Sensores, Historico
from .serializers import (
    ResponsaveisSerializers,
    LocaisSerializers,
    SensoresSerializers,
    HistoricoSerializers,
    AmbientesSerializers
)

# Filtros
class ResponsaveisFilter(FilterSet):
    class Meta:
        model = Responsaveis
        fields = ['responsavel']

class LocaisFilter(FilterSet):
    class Meta:
        model = Locais
        fields = ['local']

class AmbientesFilter(FilterSet):
    class Meta:
        model = Ambientes
        fields = ['descricao']

class HistoricoFilter(FilterSet):
    class Meta:
        model = Historico
        fields = ['sensor', 'timestamp']  # ajuste conforme campos do seu model

class SensoresFilter(FilterSet):
    status = BooleanFilter(field_name='status')

    class Meta:
        model = Sensores
        fields = ['status', 'sensor', 'mac_address', 'ambiente']

# ViewSets
class ResponsaveisViewSet(viewsets.ModelViewSet):
    queryset = Responsaveis.objects.all()
    serializer_class = ResponsaveisSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ResponsaveisFilter
    search_fields = ['responsavel']
    permission_classes = [IsAuthenticated]

class LocaisViewSet(viewsets.ModelViewSet):
    queryset = Locais.objects.all()
    serializer_class = LocaisSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = LocaisFilter
    search_fields = ['local']
    permission_classes = [IsAuthenticated]

class AmbientesViewSet(viewsets.ModelViewSet):
    queryset = Ambientes.objects.all()
    serializer_class = AmbientesSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = AmbientesFilter
    search_fields = ['descricao']
    permission_classes = [IsAuthenticated]

class SensoresViewSet(viewsets.ModelViewSet):
    queryset = Sensores.objects.all()
    serializer_class = SensoresSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = SensoresFilter
    search_fields = ['sensor', 'mac_address']
    permission_classes = [IsAuthenticated]

class HistoricoViewSet(viewsets.ModelViewSet):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = HistoricoFilter
    search_fields = []
    permission_classes = [IsAuthenticated]
