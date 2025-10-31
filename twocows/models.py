from django.db import models
from datetime import date


# Create your models here.
# Definir el modelo vacas con sus campos y métodos
class vacas(models.Model):    
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

