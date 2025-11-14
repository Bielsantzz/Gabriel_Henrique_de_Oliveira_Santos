from django.db import models
import os


class Responsaveis(models.Model):
    responsavel = models.CharField(max_length=100)

    def __str__(self):
        return self.responsavel
    
class Locais(models.Model):
    local = models.CharField(max_length=255)

    def __str__(self):
        return self.local
    
class Ambientes(models.Model):
    local = models.ForeignKey(Locais, on_delete=models.CASCADE)
    descricao = models.TextField(max_length=255)
    responsavel = models.ForeignKey(Responsaveis, on_delete=models.CASCADE)

    def __str__(self):
        return self.descricao

class Sensores(models.Model):
    sensor = models.CharField(max_length=255)
    mac_address = models.CharField(max_length=255, unique=True)
    unidade_med = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    ambiente = models.ForeignKey(Ambientes, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id_sensor} - {self.mac_address}"
    
class Historico(models.Model):
    sensor = models.ForeignKey(Sensores,on_delete=models.CASCADE)
    valor = models.CharField(max_length=150)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.id_sensor} - {self.valor}"
    



    
