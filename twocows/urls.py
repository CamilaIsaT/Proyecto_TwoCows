from django.urls import path, include
from rest_framework import routers
from twocows import views
from .views import RegisterView, UserListView

# Configurar el enrutador para las vistas de la API
router = routers.DefaultRouter()
# Registrar la vista vacasView con el enrutador
router.register(r'vacas', views.vacasView, 'vacas')
# Definir las rutas de la API
urlpatterns=[
    path('api/v1/', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
]

