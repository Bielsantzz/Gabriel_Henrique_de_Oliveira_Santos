import django_filters as df
from django.db.models import Q
from models import Responsaveis, Locais, Ambientes, Sensores,Historico


class ResponsaveisFilter(df.FilterSet):
   class Meta:
      model = Responsaveis
      fields = ['respnsavel']

class LocaisFilter(df.FilterSet):
   class Meta:
      model = Locais
      fields = ['nome']

class AmbientesFilter(df.FilterSet):
   class Meta:
      model = Ambientes
      fields = ['nome', 'local']


class SensoresFilter(df.FilterSet):
   class Meta:
      model = Sensores
      fields = ['nome', 'ambiente']

class HistoricoFilter(df.FilterSet):
   class Meta:
      model = Historico
      fields = ['sensor', 'timesamp']

