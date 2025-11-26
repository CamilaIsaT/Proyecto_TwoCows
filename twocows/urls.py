from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views

router = routers.DefaultRouter()
router.register(r'vacas', views.VacaViewSet, basename='vacas')
router.register(r'usuarios', views.UsuarioViewSet, basename='usuarios')
router.register(r'recursos', views.RecursosViewSet)
router.register(r'razas', views.RazaViewSet)
router.register(r'tipos-pasto', views.TipoPastoViewSet)
router.register(r'lotes', views.LoteViewSet)
router.register(r'registros-peso', views.RegistroPesoViewSet)
router.register(r'eventos-sanitarios', views.EventoSanitarioViewSet)
router.register(r'desleches', views.EventoDeslecheViewSet)


urlpatterns = [
    # para hacer Login (Obtener Token)
    path('login/', obtain_auth_token, name='login'),
# Incluir las rutas del router
    path('', include(router.urls)),
]