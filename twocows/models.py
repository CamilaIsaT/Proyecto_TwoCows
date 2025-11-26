from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from datetime import date
from django.forms import ValidationError
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils.text import slugify
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
     tempo_password = models.BooleanField(default=True, verbose_name="Debe de cambiarse la contraseña")
     
     def save(self, *args, **kwargs):
          if not self.username and self.first_name and self.last_name:
            rol_clean = slugify(self.rol).replace('-', '')
            nombre_clean =slugify(self.first_name)
            apellido_clean = slugify(self.last_name)

            base_user = f"{rol_clean}_{nombre_clean}{apellido_clean}"
            self.username = base_user
            contador = 1
            while Usuario.objects.filter(username=self.username).exists():
                self.username = f"{base_user}{contador}"
                contador += 1
          super().save(*args, **kwargs)
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

     def clean(self):
            if self.madre and self.madre.sexo != 'Hembra':
                raise ValidationError('La madre debe ser una vaca hembra.')
            if self.padre and self.padre.sexo != 'Macho':
                raise ValidationError('El padre debe ser un toro macho.')
            if self.madre == self or self.padre == self:
                raise ValidationError('Una vaca no puede ser su propia madre o padre.') 
            if self.fecha_nacimiento > date.today():
                raise ValidationError('La fecha de nacimiento no puede ser en el futuro.')  
            
     def save(self, *args, **kwargs):
            self.full_clean() # Fuerza la validación antes de guardar
            super().save(*args, **kwargs)
     def __str__(self):
            return f"Arete {self.arete} ({self.sexo})"
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


class DetalleEventoSanitario(models.Model):
    evento = models.ForeignKey(
         EventoSanitario,
         on_delete=models.CASCADE,
         related_name='insumos_usados',
         verbose_name="Evento Sanitario"
         )
    recurso = models.ForeignKey(
         Recursos,
         on_delete=models.PROTECT,
         null=True,
         verbose_name="Recurso Usado"
         )
    cantidad_usada = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cantidad/Dosis Usada")

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk is None:
                if self.recurso.cantidad_disponible < self.cantidad_usada:
                    raise ValidationError(f"No hay suficiente {self.recurso.nombre} disponible.")
                self.recurso.cantidad_disponible -= self.cantidad_usada
                self.recurso.save()
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.recurso.nombre}-{self.cantidad}"
class EventoDesleche(models.Model):
    lote_origen = models.ForeignKey(
         Lote,
         on_delete=models.SET_NULL,
         related_name='eventos_desleche_origen',
         null=True,
         blank=True,
         verbose_name="Lote de Origen"
         )
    lote_destino = models.ForeignKey(
        Lote,
         on_delete=models.SET_NULL,
         related_name='eventos_desleche_destino',
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

class ProduccionLeche(models.Model):
    vaca = models.ForeignKey(
         Vaca,
         on_delete=models.CASCADE,
         related_name='produccion_leche',
         verbose_name="Vaca Ordeñada", 
         )
    fecha = models.DateField(default=date.today, verbose_name="Fecha de Ordeño")
    cantidad_leche = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Cantidad de Leche (litros)")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    jornada_choices = [
        ('MAÑANA', 'Mañana'),
        ('TARDE', 'Tarde')
    ]
    jornada = models.CharField(max_length=10, choices=jornada_choices, verbose_name="Jornada de Ordeño")
    
    ordeñador = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        limit_choices_to={'rol': 'ORDENADOR'} # Solo puede el Ordeñador
    )
    class Meta:
        verbose_name = "Registro de Leche"
        verbose_name_plural = "Producción de Leche"
        ordering = ['-fecha', 'vaca']#ordena por fecha descendente y luego por vaca

    def clean(self):
        if self.vaca.sexo == 'Macho':
            raise ValidationError('No se puede registrar producción de leche para vacas macho.')
        if self.vaca.edad_meses < 18:
            raise ValidationError('Esta vaca es muy joven para producir leche.')
    def save(self, *args, **kwargs):
        self.full_clean() # Fuerza la validación antes de guardar
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.vaca.arete} - {self.fecha} ({self.jornada}): {self.litros}L"
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)