from django.contrib import admin
from .models import *
from fcm_django.models import FCMDevice


# Register your models here.

class VideojuegoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'genero', 'plataforma', 'precio']
    search_fields = ['titulo']
    list_filter = ['genero','plataforma']    
    list_per_page = 10

    def save_model(self,request, obj,form,change):
        if not change:
            dispositivos = FCMDevice.objects.all()
            dispositivos.send_message(
                title = "Se ha agregado un nuevo videojuego",
                body = f"Se agrego: {obj.titulo}",
                icon = "/static/core/img/pac-man.png"
            )
        super().save_model(request,obj,form,change)

    
    


class GeneroAdmin(admin.ModelAdmin):
    search_fields =['genero']  
    list_per_page = 10


class PlataformaAdmin(admin.ModelAdmin):
    search_fields =['plataforma']  
    list_per_page = 10

class SliderAdmin(admin.ModelAdmin):
    search_fields =['imagen']  
    list_per_page = 10

class GaleriaAdmin(admin.ModelAdmin):
    search_fields =['imagen']  
    list_per_page = 10


admin.site.register(Genero, GeneroAdmin)
admin.site.register(Plataforma, PlataformaAdmin)
admin.site.register(Videojuego, VideojuegoAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(Galeria, GaleriaAdmin)
admin.site.register(Tipo_contacto)
admin.site.register(Contactenos)
admin.site.register(Empresa)