from rest_framework import serializers
from django.utils.crypto import get_random_string
from .models import (
    Recursos, Vaca, Lote, EventoSanitario, EventoDesleche, 
    Usuario, Raza, Tipo_pasto, RegistroPeso, 
    ProduccionLeche, DetalleEventoSanitario
)
#Serializer es una clase que convierte instancias de modelos Django en formatos coamo JSON o XML y viceversa.
class UsuarioSerializer(serializers.ModelSerializer):
    pass_temp=serializers.CharField(read_only=True)
    
    class Meta:
        model = Usuario
        fields = ['id','username', 'pass_temp', 'email', 'first_name', 'last_name', 'rol']
        read_only_fields = ['username']
        
    def create(self, validated_data):
        generate_pass= get_random_string(length=8)

        # Crear el usuario con la contraseña hasheada
        user = Usuario(
            email=validated_data.get('email',''),
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            rol=validated_data.get('rol', 'CUIDADOR'),
            tempo_password=True            
        )
        user.set_password(generate_pass)
         # Guardar el usuario en la base de datos        
        user.save()
        user.pass_temp=generate_pass
        return user
    
class RecursosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recursos
        fields = '__all__'

class RazaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raza
        fields = '__all__'
    
class TipoPastoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo_pasto
        fields = '__all__'
    
class LoteSerializer(serializers.ModelSerializer):
    tipo_pasto_detalle = serializers.CharField(source='tipo_pasto.nombre', read_only=True)
    
    class Meta:
        model = Lote
        fields = '__all__'

class VacaSerializer(serializers.ModelSerializer):
    edad_meses = serializers.SerializerMethodField()
    etapa_vida = serializers.ReadOnlyField()

    class Meta:
        model = Vaca
        # Indicar los campos a incluir en el serializador
        fields = [
            'arete', 'fecha_nacimiento', 'peso_actual', 
            'raza', 'lote', 'edad_meses', 'etapa_vida',
            'estado'
            ]
# Agregar método para calcular edad en meses
    read_only_fields = ['peso_actual']

    def get_edad_meses(self, obj):
        return obj.edad_meses()
class RegistroPesoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistroPeso
        fields = '__all__'

class ProduccionLecheSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProduccionLeche
        fields = '__all__'

class DetalleEventoSanitarioSerializer(serializers.ModelSerializer):
    nombre_recursos = serializers.CharField(source='insumo.nombre', read_only=True)
    class Meta:
        model = DetalleEventoSanitario
        fields = ['id', 'insumo', 'nombre_insumo', 'cantidad_usada']
class EventoSanitarioSerializer(serializers.ModelSerializer):
    insumos_usados = DetalleEventoSanitarioSerializer(many=True,)
    class Meta:
        model = EventoSanitario
        fields = [
            'id', 'tipo', 'fecha', 'vaca_afectada', 'lote_afectado', 
            'peso_animal', 'observaciones', 'insumos_usados'
        ]

    def validar(self, data):
        if not data.get('vaca_afectada') and not data.get('lote_afectado'):
            raise serializers.ValidationError("Debes seleccionar una vaca o un lote afectado.")
        if data.get('vaca_afectada') and data.get('lote_afectado'):
            raise serializers.ValidationError("No puedes seleccionar una vaca y un lote al mismo tiempo.") 
        return data
    
    def create(self, validated_data):
        insumos_data = validated_data.pop('insumos_usados')
        evento = EventoSanitario.objects.create(**validated_data)
        for insumo in insumos_data:
            DetalleEventoSanitario.objects.create(evento=evento, **insumo)
            
        return evento

class EventoDeslecheSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventoDesleche
        fields = '__all__'