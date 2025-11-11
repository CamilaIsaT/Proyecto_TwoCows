from django.shortcuts import render
from rest_framework import viewsets
from .serializer import vacasSerializer
from .models import vacas

# Create your views here.
class vacasView(viewsets.ModelViewSet):
    # Definir el conjunto de consultas y el serializador para la vista
    queryset = vacas.objects.all()
    serializer_class = vacasSerializer
