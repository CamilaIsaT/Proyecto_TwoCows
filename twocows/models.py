from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from datetime import date
from django.forms import ValidationError


#Create your models here.

class Usuario(AbstractUser): #AbstracUser extiende el modelo de usuario predeterminado de Django
     roles = [
        ('ADMIN', 'Jefe de Campo'),
        ('CUIDADOR', 'Cuidador de Vacas'),
        ('ORDENADOR', 'Ordeñador'),
        ('POTRERO', 'Encargado de Potrero'),
    ]
     rol = models.CharField(
          max_length=20, 
          choices=roles, 
          default='CUIDADOR', # Valor por defecto
          verbose_name="Rol del Usuario")
     class Meta:
          verbose_name = "Usuario"
          verbose_name_plural = "Usuarios"
        
class Recursos(models.Model):
        # Modelo para gestionar recursos como alimentos, medicinas, vacunas, etc.
     tipo_recurso=[
        ('ALIMENTO', 'Alimento'),
        ('MEDICINA', 'Medicina'),
        ('VACUNA', 'Vacuna'),
     ]
     nombre = models.CharField(max_length=100, unique=True)
     tipo = models.CharField(max_length=50, choices=tipo_recurso)
     cantidad_disponible = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad Disponible")
     unidad = models.CharField(max_length=20, verbose_name="Unidad de Medida (kg, litros, dosis, etc.)")
     fecha_venc = models.DateField(null=True, blank=True)

     def __str__(self):
          return f"{self.nombre} ({self.cantidad_disponible} {self.unidad}"
          
       
class Raza(models.Model):
        # Modelo para definir las razas de las vacas
     nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Raza")
    
     class Meta:
         #define nombres legibles para el modelo en singular y plural
         verbose_name = "Raza"
         verbose_name_plural = "Razas"

     def __str__(self):
         return self.nombre
     
class Tipo_pasto(models.Model):
        # Modelo para definir tipos de pasto
        nombre = models.CharField(max_length=100, unique=True, verbose_name="Tipo de Pasto")
        descripcion = models.TextField(blank=True, verbose_name="Descripción del Pasto")
    
        def __str__(self):
            return self.nombre

class Lote(models.Model):
     # Modelo para agrupar vacas en lotes
     nombre = models.CharField(max_length=100, unique=True, verbose_name="Lote") #verbose_name para etiquetas más amigables en formularios y admin
     pasto = models.ForeignKey(
          Tipo_pasto, on_delete=models.SET_NULL, 
          null=True, 
          verbose_name="Tipo de Pasto"
          )
     area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Área hectareas", default=0)
     descripcion = models.TextField(blank=True, verbose_name="Descripción")
     capacidad = models.IntegerField(verbose_name="Capacidad Máxima")
     estado = models.BooleanField(default=True, verbose_name="Lote Activo")

     def __str__(self):
         return self.nombre #devuelve el nombre del lote como representación del objeto

class Vaca(models.Model):
     
     validar = RegexValidator( r'^\d+$', 'El número de arete solo debe contener números.')
     arete = models.CharField(
          max_length=12,
          unique=True,
          verbose_name="Número de Arete",
          validators=[validar]
          )  #validador para asegurar que solo contenga números
     raza = models.ForeignKey(
          Raza, 
          on_delete=models.SET_NULL,
          null=True, 
          verbose_name="Raza"
          )
     lote = models.ForeignKey(
          Lote, 
          on_delete=models.SET_NULL, 
          null=True, 
          related_name='vacas_en_lote',
          verbose_name="Lote Actual"
          )
     fecha_nacimiento = models.DateField()
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
     sexo_choices = [
         ('Macho', 'Macho'),
         ('Hembra', 'Hembra'),
     ]
     #selección de sexo con opciones
     sexo = models.CharField(max_length=6, choices=sexo_choices)
     peso_inicial = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="Peso inicial (kg)")
     peso_actual = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="Peso Actual (kg)")
     estado_vaca= [
        ('ACTIVO', 'Activo en hato'),
        ('VENDIDO', 'Vendido'),
        ('MUERTO', 'Fallecido'),
        ('PERDIDO', 'Perdido/Robado'),
    ]
     estado = models.CharField(max_length=20, choices=estado_vaca, default='ACTIVO')
     @property 
     def edad_meses(self):
        hoy = date.today()
        #Se asegura de que la fecha de nacimiento esté disponible
        if self.fecha_nacimiento:
            return (hoy.year - self.fecha_nacimiento.year) * 12 + hoy.month - self.fecha_nacimiento.month
        return 0

     @property # Indica que este método se puede acceder como un atributo
     def etapa_vida(self):
        meses = self.edad_meses
        if meses < 6: return 'Ternero/a'
        elif meses < 18: return 'Novillo/Novilla'
        elif meses < 96: return 'Adulta'
        else: return 'Vieja'

     class Meta:
        verbose_name = "Vaca/Animal"
        verbose_name_plural = "Inventario de Animales"

     def __str__(self):
        return f"Arete {self.arete} ({self.sexo})"
     
class RegistroPeso(models.Model):
    vaca = models.ForeignKey(
         Vaca, 
         on_delete=models.CASCADE, 
         related_name='registros_peso',
         verbose_name="Vaca"
         )
    fecha_registro = models.DateField(verbose_name="Fecha de Registro")
    peso = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Peso (kg)")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    
    def save(self, *args, **kwargs):# el metodo sobreescribe el peso de la vaca cada vez que se guarda un nuevo registro de peso
        super().save(*args, **kwargs)
        self.vaca.peso_actual = self.peso
        self.vaca.save()


    def __str__(self):
        return f"Peso de Vaca {self.vaca.arete} el {self.fecha_registro}: {self.peso} kg"

class EventoSanitario(models.Model):
    tipo_evento = [
     ('VACUNA', 'Vacunación'),
     ('TRATAMIENTO', 'Tratamiento'),
     ('DESPARASITACION', 'Desparasitación'),
     ('ENFERMEDAD', 'Enfermedad'),
     ]
    tipo = models.CharField(max_length=50, choices=tipo_evento, verbose_name="Tipo de Evento")
    fecha = models.DateField(verbose_name="Fecha del Evento")
    producto_usado = models.ForeignKey(
         Recursos,
         on_delete=models.PROTECT,
         null=True,
         verbose_name="Medicina Usada"
         )
    dosis = models.IntegerField(
        max_length=8, 
        decimal_places=2,
        help_text="Cantidad de dosis aplicada",#help_text para guiar al usuario de qué ingresar
        blank=True, 
        null=True,
        verbose_name="Dosis Aplicada"
        )
    peso_animal= models.DecimalField(max_digits=6,decimal_places=2,blank=True, null=True, verbose_name="Peso del Animal (kg)")
    observaciones = models.TextField(blank=True)
    vaca_afectada = models.ForeignKey(
         Vaca, 
         on_delete=models.CASCADE, 
         null=True,
         blank=True,
         related_name='eventos_sanitarios',
         verbose_name="Animal Afectado"
         )    
    lote_afectado = models.ForeignKey(
         Lote, 
         on_delete=models.CASCADE, 
         related_name='eventos_sanitarios',
         verbose_name="Lote Afectado",
         null=True,           
         blank=True           
         )
    #asegura que se selecione una relacion paraque el evento pueda ser guardado
    def clean(self):
        if not self.vaca_afectada and not self.lote_afectado:
            raise ValidationError('Debes seleccionar una Vaca o un Lote afectado.')
        if self.vaca_afectada and self.lote_afectado:
            raise ValidationError('No puedes asignar el evento a una Vaca y un Lote al mismo tiempo.')
#save hace la validación antes de guardar
    def save(self, *args, **kwargs):
        self.full_clean() # Fuerza la validación antes de guardar
        super().save(*args, **kwargs)

        if self.peso_animal and self.vaca_afectada:
            RegistroPeso.objects.create(
                vaca=self.vaca_afectada,
                fecha_registro=self.fecha,
                peso=self.peso_animal,
                observaciones=f"Registro durante evento sanitario: {self.get_tipo_display()}")
    def __str__(self):
        destino = f"Vaca {self.vaca_afectada.arete}" if self.vaca_afectada else f"Lote {self.lote_afectado.nombre}"
        return f"{self.get_tipo_display()} - {destino} - {self.fecha}"

class EventoDesleche(models.Model):
    lote_origen = models.ForeignKey(
         Lote,
         on_delete=models.SET_NULL,
         null=True,
         blank=True,
         verbose_name="Lote de Origen"
         )
    lote_destino = models.ForeignKey(
        Lote,
         on_delete=models.SET_NULL,
         null=True,
         blank=True,
         verbose_name="Lote de Destino"
         )
    fecha_desleche=models.DateField(verbose_name="Fecha de Desleche (Destete)")
    numero_animales=models.IntegerField(verbose_name="Número de Animales Deslechados")
    peso_promedio=models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Peso Promedio (kg)"
        )
    observaciones=models.TextField(blank=True)
    def __str__(self):
        return f"Desleche del Lote {self.lote_origen.nombre if self.lote_origen else 'N/A'} el {self.fecha_desleche}"
