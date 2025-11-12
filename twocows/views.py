from rest_framework import viewsets
from .models import vacas, Lote, EventoSanitario, EventoDesleche
from .serializer import vacaSerializer, LoteSerializer, EventoSanitarioSerializer, EventoDeslecheSerializer

# Create your views here.
class vacasView(viewsets.ModelViewSet):
    # Definir el conjunto de consultas y el serializador para la vista
    queryset = vacas.objects.all()
    serializer_class = vacaSerializer

class LoteView(viewsets.ModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer

class EventoSanitarioView(viewsets.ModelViewSet):
    queryset = EventoSanitario.objects.all()
    serializer_class = EventoSanitarioSerializer

class EventoDeslecheView(viewsets.ModelViewSet):
    queryset = EventoDesleche.objects.all()
    serializer_class = EventoDeslecheSerializer