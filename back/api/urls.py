from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResponsaveisViewSet, LocaisViewSet, AmbientesViewSet, SensoresViewSet, HistoricoViewSet

router = DefaultRouter()
router.register(r'responsaveis', ResponsaveisViewSet, basename='responsaveis')
router.register(r'locais', LocaisViewSet, basename='locais')
router.register(r'ambientes', AmbientesViewSet, basename='ambientes')
router.register(r'sensores', SensoresViewSet, basename='sensores')
router.register(r'historico', HistoricoViewSet, basename='historico')

urlpatterns = [
    path('', include(router.urls)),
]
