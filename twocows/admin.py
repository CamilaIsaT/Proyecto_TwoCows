from django.contrib import admin
from .models import vacas, EventoDesleche, EventoSanitario, Lote, Raza


# Register your models here.
# Registrar el modelo vacas en el sitio de administración de Django
admin.site.register(vacas)
admin.site.register(EventoDesleche)
admin.site.register(EventoSanitario)
admin.site.register(Lote)
admin.site.register(Raza)

