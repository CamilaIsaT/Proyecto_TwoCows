from rest_framework import serializers
from django.contrib.auth.models import User


# Crear un serializador para el modelo vacas
#serializer es una clase que convierte instancias de modelos Django en formatos coamo JSON o XML y viceversa.
class vacasSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import vacas
        # Especificar el
        model = vacas
        # Incluir todos los campos del modelo vacas
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','email']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user