from django.db import models
from datetime import date
from django.forms import ValidationError


# Create your models here.
# Definir el modelo vacas con sus campos y métodos

"""    class vacas(models.Model):    
    arete = models.CharField(max_length=50)
    raza = models.CharField(max_length=100)
    etapas_vida_choices=[
        ('ternero', 'ternero'),
        ('novillo', 'novillo'),
        ('joven', 'joven'),
        ('adulta', 'adulta'),
        ('vieja', 'vieja'),
    ]
    etapa = models.CharField(max_length=50, choices=etapas_vida_choices)
    lote = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()    
    sexo_choices=[
        ('Macho', 'Macho'),
        ('Hembra', 'Hembra'),
    ]
    sexo = models.CharField(max_length=6, choices=sexo_choices)
    madre = models.CharField(max_length=100)
    padre = models.CharField(max_length=100)


    def edad_meses(self):
        # Calcula la edad en meses a partir de la fecha de nacimiento
        hoy = date.today()
        return (hoy.year - self.fecha_nacimiento.year) * 12 + hoy.month - self.fecha_nacimiento.month


    @property
    def etapa_vida(self):
        # Determina la etapa de vida basada en la edad en meses
        meses = self.edad_meses()
        if meses < 6:
            return 'ternero'
        elif meses < 18:
            return 'novillo'
        elif meses < 36:
            return 'joven'
        elif meses < 96:
            return 'adulta'
        else:
            return 'vieja'


    def __str__(self):
        return self.arete

"""
# ===============================================
# MODELO: Lote de Vacas
# ===============================================
class Lote(models.Model):
    """Representa un grupo de vacas."""
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Lote")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    capacidad = models.IntegerField(verbose_name="Capacidad Máxima")
    activo = models.BooleanField(default=True, verbose_name="Lote Activo")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Lote de Vacas"
        verbose_name_plural = "Lotes de Vacas"


# ===============================================
# MODELO: Evento Sanitario (Vacunas, Tratamientos)
# ===================================
class EventoSanitario(models.Model):
    """Registra una actividad de salud, aplicable a una vaca o un lote."""
    
    TIPO_EVENTO = [
        ('VACUNA', 'Vacunación'),
        ('TRATAMIENTO', 'Tratamiento'),
        ('DESPARASITACION', 'Desparasitación'),
    ]

    tipo = models.CharField(max_length=50, choices=TIPO_EVENTO, verbose_name="Tipo de Evento(Vacuna, tratamiento, Desparasitación)")
    fecha = models.DateField(verbose_name="Fecha del Evento")
    producto_usado = models.CharField(max_length=150, verbose_name="Producto/Medicina Usada")
    dosis = models.CharField(max_length=50, blank=True, verbose_name="Dosis Aplicada")
    observaciones = models.TextField(blank=True)
    
    # 1. Relación para eventos individuales (Opcional)
    vaca_afectada = models.ForeignKey(
        'Vaca', 
        on_delete=models.CASCADE, 
        related_name='eventos_individuales',
        verbose_name="Animal Afectado",
        null=True,           # Permite valor NULL en la base de datos
        blank=True           # Permite dejar el campo vacío en formularios
    )
    
    # 2. Relación para eventos grupales (Opcional)
    lote_afectado = models.ForeignKey(
        'Lote', 
        on_delete=models.CASCADE, 
        related_name='eventos_grupales',
        verbose_name="Lote Afectado",
        null=True,           # Permite valor NULL en la base de datos
        blank=True           # Permite dejar el campo vacío en formularios
    )

    def clean(self):
        """Valida que al menos una de las dos relaciones (Vaca o Lote) esté seleccionada."""
        if not self.vaca_afectada and not self.lote_afectado:
            raise ValidationError('Debe seleccionar un Animal Afectado o un Lote Afectado. No puede dejar ambos campos vacíos.')
        
        # Opcional: Evitar que se seleccionen AMBOS
        if self.vaca_afectada and self.lote_afectado:
             raise ValidationError('Un evento no puede estar asignado a un animal individual Y a un lote simultáneamente. Elija solo uno.')


    def save(self, *args, **kwargs):
        """Llama a clean() antes de guardar para asegurar la validación."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.vaca_afectada:
            return f"{self.get_tipo_display()} a Vaca {self.vaca_afectada.arete} el {self.fecha}"
        elif self.lote_afectado:
            return f"{self.get_tipo_display()} al Lote {self.lote_afectado.nombre} el {self.fecha}"
        return f"{self.get_tipo_display()} sin asignación"


    class Meta:
        verbose_name = "Evento Sanitario"
        verbose_name_plural = "Eventos Sanitarios"
# ===============================================
# MODELO: Evento de Desleche (Destete)
# ===============================================

class EventoDesleche(models.Model):
    """Registra el proceso de desleche (destete) de los animales."""
    
    # Relación de Muchos a Uno (Un lote es el origen del desleche)
    lote_origen = models.ForeignKey(
        Lote, 
        on_delete=models.SET_NULL, # Si el lote se borra, el evento permanece (NULL)
        null=True, 
        related_name='desleches_realizados',
        verbose_name="Lote de Origen"
    )
    
    fecha_desleche = models.DateField(verbose_name="Fecha de Desleche (Destete)")
    numero_animales = models.IntegerField(verbose_name="Número de Animales Deslechados")
    peso_promedio = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        blank=True, 
        null=True,
        verbose_name="Peso Promedio (kg)"
    )
    
    # Campo para registrar a qué nuevo lote pasaron los animales deslechados
    lote_destino = models.ForeignKey(
        Lote, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='desleches_recibidos',
        verbose_name="Lote de Destino"
    )
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Desleche del Lote {self.lote_origen.nombre if self.lote_origen else 'N/A'} el {self.fecha_desleche}"

    class Meta:
        verbose_name = "Evento de Desleche"
        verbose_name_plural = "Eventos de Desleche"

# ===============================================
# MODELO: Vaca
# ===============================================

class Vaca(models.Model):
    """Modelo principal para registrar una vaca individual."""

    # 1. Información de Identificación
    arete = models.CharField(max_length=50, unique=True, verbose_name="Número de Arete")
    raza = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    
    # 2. Relación con Lote (¡INTEGRACIÓN CLAVE!)
    lote = models.ForeignKey(
        Lote, 
        on_delete=models.SET_NULL, # Mantiene la vaca aunque se borre el lote
        null=True, 
        blank=True,
        related_name='animales_en_lote',
        verbose_name="Lote Actual"
    )
    
    # 3. Sexo
    sexo_choices = [
        ('Macho', 'Macho'),
        ('Hembra', 'Hembra'),
    ]
    sexo = models.CharField(max_length=6, choices=sexo_choices)
    
    # 4. Genealogía (Relaciones consigo misma - Recursivas)
    madre = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='hijos',
        verbose_name="Arete de la Madre"
    )
    padre = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='crias',
        verbose_name="Arete del Padre"
    )


    # --- LÓGICA DE EDAD Y ETAPA DE VIDA ---
    
    def edad_meses(self):
        """Calcula la edad exacta de la vaca en meses."""
        hoy = date.today()
        # Se asegura de que la fecha de nacimiento esté disponible
        if self.fecha_nacimiento:
            return (hoy.year - self.fecha_nacimiento.year) * 12 + hoy.month - self.fecha_nacimiento.month
        return 0

    @property
    def etapa_vida(self):
        """Determina la etapa de vida basada en la edad en meses."""
        meses = self.edad_meses()
        if meses < 6:
            return 'Ternero/a'
        elif meses < 18:
            return 'Novillo/Novilla'
        elif meses < 36:
            # En la edad joven una vaca ya podría ser una 'Vaca Joven'
            return 'Joven'
        elif meses < 96:
            return 'Adulta'
        else:
            return 'Vieja'


    def __str__(self):
        return self.arete

    class Meta:
        verbose_name = "Vaca/Animal"
        verbose_name_plural = "Vacas/Animales"