from rest_framework import serializers
from .models import vacas, Lote, EventoSanitario, EventoDesleche
from datetime import date


# Crear un serializador para el modelo vacas
#serializer es una clase que convierte instancias de modelos Django en formatos coamo JSON o XML y viceversa.
class vacaSerializer(serializers.ModelSerializer):
    # Agregar campos calculados
    edad_meses = serializers.SerializerMethodField()
    etapa_vida = serializers.ReadOnlyField()
# Meta indica qué modelo se está serializando y qué campos incluir
    class Meta:
        model = vacas
        fields = '__all__'
# Agregar método para calcular edad en meses
    def get_edad_meses(self, obj):
        """Devuelve la edad de la vaca en meses."""
        return obj.edad_meses()
    


#Cewrar un serializador para el modelo lote
class LoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lote
        fields = '__all__'

# Crear un serializador para el modelo Evento
class EventoSanitarioSerializer(serializers.ModelSerializer):
    # Muestra los nombres del lote y la vaca en texto
    vaca_afectada_nombre = serializers.CharField(
        source='vaca_afectada.arete', read_only=True
    )
    lote_afectado_nombre = serializers.CharField(
        source='lote_afectado.nombre', read_only=True
    )
    class Meta:
        model = EventoSanitario
        fields = '__all__'

# Crear un serializador para el modelo EventoDesleche
class EventoDeslecheSerializer(serializers.ModelSerializer):
    # Nombres legibles de los lotes
    lote_origen_nombre = serializers.CharField(
        source='lote_origen.nombre', read_only=True
    )
    lote_destino_nombre = serializers.CharField(
        source='lote_destino.nombre', read_only=True
    )

    class Meta:
        model = EventoDesleche
        fields = '__all__'

class VacaDetalleSerializer(serializers.ModelSerializer):
    eventos_individuales = EventoSanitarioSerializer(many=True, read_only=True)

    class Meta:
        model = vacas
        fields = '__all__'