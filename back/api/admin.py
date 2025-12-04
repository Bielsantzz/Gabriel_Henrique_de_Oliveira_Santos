from django.contrib import admin
from .models import Responsaveis, Locais, Ambientes, Sensores, Historico

admin.site.register(Responsaveis)
admin.site.register(Locais)
admin.site.register(Ambientes)
admin.site.register(Sensores)
admin.site.register(Historico)
