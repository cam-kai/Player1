from rest_framework import serializers
from .models import Videojuego, Plataforma, Genero, Contactenos,Tipo_contacto

class GeneroSerializers(serializers.ModelSerializer):

    class Meta:
        model = Genero
        fields = ['id', 'nombre']


class PlataformaSerializers(serializers.ModelSerializer):

    class Meta:
        model = Plataforma
        fields = ['id', 'nombre']


class VideojuegoSerializers(serializers.ModelSerializer):

    class Meta:
        model = Videojuego
        fields = ['id','titulo','genero', 'plataforma', 'descripcion', 'caratula','precio']


class TipoContactoSerializers(serializers.ModelSerializer):

    class Meta:
        model =  Tipo_contacto
        fields = ['id','tipo_contacto']


class ContactenosSerializers(serializers.ModelSerializer):

    class Meta:
        model = Contactenos
        fields = ['id', 'rut','nombre', 'apellido','asunto', 'tipo_contacto','mensaje']