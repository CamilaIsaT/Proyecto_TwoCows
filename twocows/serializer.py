from rest_framework import serializers


# Crear un serializador para el modelo vacas
#serializer es una clase que convierte instancias de modelos Django en formatos coamo JSON o XML y viceversa.
class vacasSerializer(serializers.ModelSerializer):
    class Meta:
        from .models import vacas
        # Especificar el
        model = vacas
        # Incluir todos los campos del modelo vacas
        fields = '__all__'

