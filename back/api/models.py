from django.db import models
from django.contrib.auth.models import AbstractUser
import os, uuid

class Responsaveis(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.responsavel
    
class Locais (models.Model):
    local = models.CharField(max_length=50)

    def __str__(self):
        return self.local
    
class Ambientes (models.Model):
    local = models.ForeignKey(Locais, on_delete=models.CASCADE) 
    descricao = models.TextField()	
    responsavel =  models.ForeignKey(Responsaveis, on_delete=models.CASCADE)

    def __str__(self):
        return self.descricao
    
class Sensores (models.Model):
    sensor = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=50)
    unidade_medida = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.BooleanField(default=True)
    ambiente = models.ForeignKey(Ambientes, on_delete=models.CASCADE)

    def __str__(self):
        return self.sensor

class Historico (models.Model):
    sensor = models.ForeignKey(Sensores, to_field="id", on_delete=models.CASCADE)
    valor = models.FloatField()
    timestamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.valor