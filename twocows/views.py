from django.shortcuts import render
from rest_framework import viewsets
from .serializer import vacasSerializer,UserSerializer, RegisterSerializer
from .models import vacas
from rest_framework import generics, permissions
from django.contrib.auth.models import User

# Create your views here.
class vacasView(viewsets.ModelViewSet):
    # Definir el conjunto de consultas y el serializador para la vista
    queryset = vacas.objects.all()
    serializer_class = vacasSerializer

# Listar usuarios
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # Solo autenticados

# Registrar nuevos usuarios
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  # Cualquiera puede registrarse