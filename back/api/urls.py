from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()  # gera barra final nas rotas

urlpatterns = [
    path('responsaveis/', ResponsaveisView.as_view(), name='responsaveis-list'),
    path('responsaveis/<int:pk>', ResponsaveisDetailView.as_view(), name='responsaveis-detail'),

    path('locais', LocaisView.as_view(), name='locais-list'),
    path('locais/<int:pk>', LocaisDetailView.as_view(), name='locais-detail'),

    path('ambientes', AmbientesView.as_view(), name='ambientes-list'),
    path('ambientes/<int:pk>', AmbientesDetailView.as_view(), name='ambientes-detail'),
    
    path('sensores', SensoresView.as_view(), name='sensores-list'),
    path('sensores/<int:pk>', SensoresDetailView.as_view(), name='sensores-detail'),
    
    path('historico', HistoricoView.as_view(), name='historico-list'),
    path('historico/<int:pk>', HistoricoDetailView.as_view(), name='historico-detail'),


    path('token/',   TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(),    name='token_refresh'),
    path('register/', RegisterView.as_view(),       name='register'),
]

urlpatterns += router.urls