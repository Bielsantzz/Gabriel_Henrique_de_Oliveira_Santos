from django.shortcuts import render
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView
)
from django.contrib.auth import get_user_model
from .models import Responsaveis, Locais, Sensores, Ambientes, Historico
from .serializers import (ResponsaveisSerializer,
    LocaisSerializer,
    SensoresSerializer,
    AmbientesSerializer,
    HistoricoSerializer,
    RegisterSerializer
)

# ----------------------------
# CRUD Responsáveis
# ----------------------------
class ResponsaveisView(ListCreateAPIView):
    queryset = Responsaveis.objects.all()
    serializer_class = ResponsaveisSerializer


class ResponsaveisDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Responsaveis.objects.all()
    serializer_class = ResponsaveisSerializer


# ----------------------------
# CRUD Locais
# ----------------------------
class LocaisView(ListCreateAPIView):
    queryset = Locais.objects.all()
    serializer_class = LocaisSerializer


class LocaisDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Locais.objects.all()
    serializer_class = LocaisSerializer


# ----------------------------
# CRUD Ambientes
# ----------------------------
class AmbientesView(ListCreateAPIView):
    queryset = Ambientes.objects.all()
    serializer_class = AmbientesSerializer


class AmbientesDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Ambientes.objects.all()
    serializer_class = AmbientesSerializer


# ----------------------------
# CRUD Sensores
# ----------------------------
class SensoresView(ListCreateAPIView):
    queryset = Sensores.objects.all()
    serializer_class = SensoresSerializer


class SensoresDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Sensores.objects.all()
    serializer_class = SensoresSerializer
    

class HistoricoView(ListCreateAPIView):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer

class HistoricoDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Historico.objects.all()
    serializer_class = HistoricoSerializer

# ----------------------------
# Register User
# ----------------------------
User = get_user_model()

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        user = ser.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': {'id': user.id, 'username': user.username},
            'tokens': {'refresh': str(refresh), 'access': str(refresh.access_token)}
        }, status=status.HTTP_201_CREATED)