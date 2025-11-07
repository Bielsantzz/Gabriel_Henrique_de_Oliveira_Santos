import django_filters
from models import Responsaveis, Locais, Ambientes, Sensores,Historico


class ResponsaveisFilter(django_filters.FilterSet):
   class Meta:
      Model = Responsaveis
      fields = ['nome']

class LocaisFilter(django_filters.FilterSet):
   class Meta:
      Model = Locais
      fields = ['nome']

class AmbientesFilter(django_filters.FilterSet):
   class Meta:
      Model = Ambientes
      fields = ['nome', 'local']


class SensoresFilter(django_filters.FilterSet):
   class Meta:
      Model = Sensores
      fields = ['nome', 'ambiente']

class HistoricoFilter(django_filters.FilterSet):
   class Meta:
      Model = Historico
      fields = ['sensor', 'timesamp']

