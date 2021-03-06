from django.contrib import admin
from .models import *
from fcm_django.models import FCMDevice


# Register your models here.

class VideojuegoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'genero', 'plataforma', 'precio']
    search_fields = ['titulo']
    list_filter = ['genero','plataforma']    
    list_per_page = 10

    def save_model(self,request,obj,form,change):
        if not change:
            dispositivos = FCMDevice.objects.all()
            dispositivos.send_message(
                title = "Se ha agregado un nuevo videojuego",
                body = f"Se agregó: {obj.titulo}",
                icon = "/static/core/img/pac-man.png"
            )
        super().save_model(request,obj,form,change)


    def delete_model(self,request,obj):
        dispositivos = FCMDevice.objects.filter(user__is_superuser=True)
        dispositivos.send_message(
            title = "Se ha eliminado un videojuego",
            body = f"Se eliminó: {obj.titulo}",
            icon = "/static/core/img/pac-man.png",
        )
        super().delete_model(request,obj)
    
    
    def delete_queryset(self,request,queryset):
        cantidad = queryset.count()
        dispositivos = FCMDevice.objects.filter(user__is_superuser=True)
        dispositivos.send_message(
            title = "Se ha realizado una eliminación masiva",
            body = f"Se han eliminado un total de {cantidad} de videojuegos",
            icon = "/static/core/img/pac-man.png",
        )
        super().delete_queryset(request,queryset)


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

class Tipo_contactoAdmin(admin.ModelAdmin):
    search_fields = ['tipo_contacto']
    list_per_page = 10

class ContactenosAdmin(admin.ModelAdmin):
    search_fields = ['nombre']
    list_per_page = 10


admin.site.register(Genero, GeneroAdmin)
admin.site.register(Plataforma, PlataformaAdmin)
admin.site.register(Videojuego, VideojuegoAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(Galeria, GaleriaAdmin)
admin.site.register(Tipo_contacto,Tipo_contactoAdmin)
admin.site.register(Contactenos, ContactenosAdmin)
admin.site.register(Empresa)