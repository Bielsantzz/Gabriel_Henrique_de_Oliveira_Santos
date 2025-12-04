import django_filters as df
from .models import Responsaveis, Locais, Ambientes, Sensores,Historico


class ResponsaveisFilter(df.FilterSet):
   class Meta:
      model = Responsaveis
      fields = ['responsavel']

class LocaisFilter(df.FilterSet):
   class Meta:
      model = Locais
      fields = ['local']

class AmbientesFilter(df.FilterSet):
   class Meta:
      model = Ambientes
      fields = ['descricao', 'local']


class SensoresFilter(df.FilterSet):
   class Meta:
      model = Sensores
      fields = ['sensor', 'ambiente']

class HistoricoFilter(df.FilterSet):
   class Meta:
      model = Historico
      fields = ['sensor', 'timestamp']

