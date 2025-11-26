from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsAdminOrReadOnly
from .serializer import (UsuarioSerializer, RecursosSerializer, RazaSerializer,TipoPastoSerializer, LoteSerializer, VacaSerializer,RegistroPesoSerializer, EventoSanitarioSerializer, EventoDeslecheSerializer)
from .models import Usuario, Recursos, Raza, Tipo_pasto, Lote, Vaca, RegistroPeso, EventoSanitario, EventoDesleche

# Create your views here.
# Vista para registrar un nuevo usuario
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        if self.action =='create':
            return [AllowAny()]
        return [IsAdminOrReadOnly()]
# vistas protegidas para que solo usuarios autenticados puedan acceder a la vista
class VacaViewSet(viewsets.ModelViewSet):
    #Los usuarios deben estar autenticados para acceder a esta vista
    permission_classes = [IsAuthenticated]
    # Definir el conjunto de consultas y el serializador para la vista
    queryset = Vaca.objects.all()
    serializer_class = VacaSerializer
#permiter filtrar y buscar vacas por ciertos campos
    filter_fields = {'lote', 'estado'}
    search_fields = ['arete']

class RecursosViewSet(viewsets.ModelViewSet):
    queryset = Recursos.objects.all()
    serializer_class = RecursosSerializer
    permission_classes = [IsAuthenticated]

class RazaViewSet(viewsets.ModelViewSet):
    queryset = Raza.objects.all()
    serializer_class = RazaSerializer
    permission_classes = [IsAuthenticated]

class TipoPastoViewSet(viewsets.ModelViewSet):
    queryset = Tipo_pasto.objects.all()
    serializer_class = TipoPastoSerializer
    permission_classes = [IsAuthenticated]

class LoteViewSet(viewsets.ModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer
    permission_classes = [IsAuthenticated]

class RegistroPesoViewSet(viewsets.ModelViewSet):
    queryset = RegistroPeso.objects.all()
    serializer_class = RegistroPesoSerializer
    permission_classes = [IsAuthenticated]

class EventoSanitarioViewSet(viewsets.ModelViewSet):
    queryset = EventoSanitario.objects.all()
    serializer_class = EventoSanitarioSerializer
    permission_classes = [IsAuthenticated]

class EventoDeslecheViewSet(viewsets.ModelViewSet):
    queryset = EventoDesleche.objects.all()
    serializer_class = EventoDeslecheSerializer
    permission_classes = [IsAuthenticated]