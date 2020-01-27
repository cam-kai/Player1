from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('genero', GeneroViewSet)
router.register('plataforma', PlataformaViewSet)
router.register('videojuegos', VideojuegoViewSet)
router.register('contactenos', ContactenosViewSet)

urlpatterns = [
    path('', home, name= "home"),
    path('contactenos/', contactenos, name="contactenos"),
    path('economia/', economia, name= "economia"),
    path('empresa/', empresa , name= "empresa"),
    path('galeria/', galeria, name= "galeria"),
    path('listado-videojuegos/', listado_videojuegos, name= "listado_videojuegos"),
    path('agregar-videojuegos/', agregar_videojuego, name= "agregar_videojuegos"),
    path('modificar-videojuegos/<id>/', modificar_videojuego, name= "modificar_videojuegos"),
    path('eliminar-videojuego/<id>/', eliminar_videojuego, name= "eliminar_videojuego"),
    path('registro/', registro, name="registro"),
    path('api/', include(router.urls)),
    path('save-token/', save_token, name="save_token"),
]