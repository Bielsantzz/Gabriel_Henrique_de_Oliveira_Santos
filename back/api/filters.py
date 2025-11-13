import django_filters as df
from django.db.models import Q
from models import Responsaveis, Locais, Ambientes, Sensores,Historico


class ResponsaveisFilter(df.FilterSet):
   class Meta:
      Model = Responsaveis
      fields = ['nome']

class LocaisFilter(df.FilterSet):
   class Meta:
      Model = Locais
      fields = ['nome']

class AmbientesFilter(df.FilterSet):
   class Meta:
      Model = Ambientes
      fields = ['nome', 'local']


class SensoresFilter(df.FilterSet):
   class Meta:
      Model = Sensores
      fields = ['nome', 'ambiente']

class HistoricoFilter(df.FilterSet):
   class Meta:
      Model = Historico
      fields = ['sensor', 'timesamp']

