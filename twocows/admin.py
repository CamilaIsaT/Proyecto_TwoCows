from django.contrib import admin
from .models import (
    Recursos, Vaca, Lote, EventoSanitario, EventoDesleche, 
    Usuario, Raza, Tipo_pasto, RegistroPeso, 
    ProduccionLeche, DetalleEventoSanitario
)
# Register your models here.
# Registrar el modelo vacas en el sitio de administración de Django
admin.site.register(Usuario)
admin.site.register(Recursos)
admin.site.register(Raza)
admin.site.register(Tipo_pasto)
admin.site.register(Lote)
admin.site.register(Vaca)
admin.site.register(RegistroPeso)
admin.site.register(EventoSanitario)
admin.site.register(EventoDesleche)
admin.site.register(ProduccionLeche)
admin.site.register(DetalleEventoSanitario)

