from django.shortcuts import render , redirect
from .models import *
from .forms import *
from django.contrib.auth import login, authenticate
from django.db.models import Avg, Min, Max, Sum
from django.contrib.auth.decorators import login_required, permission_required
from .serializers import *
from rest_framework import viewsets

from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
import json
from fcm_django.models import FCMDevice

# Create your views here.

@csrf_exempt
def save_token(request):
    body = request.body.decode('utf-8')
    #transformamos el json en un diccionario
    dicttoken = json.loads(body)
    token = dicttoken['token']

    #preguntaremos si el token ya existe
    cantidad = FCMDevice.objects.filter(registration_id=token, active=True).count()

    if cantidad > 0:
        return JsonResponse({'mensaje':'el token ya existe'}, status=400)

    dispositivo = FCMDevice()
    dispositivo.registration_id = token

    if request.user.is_authenticated:
        dispositivo.user = request.user

    dispositivo.save()
    return JsonResponse({'mensaje':'guardado'}, status=200)


class GeneroViewSet(viewsets.ModelViewSet):
    queryset = Genero.objects.all()
    serializer_class = GeneroSerializers

    def get_queryset(self):
        genero = Genero.objects.all()

        nombre = self.request.GET.get('nombre') or ''

        if nombre:
            genero = genero.filter(nombre__contains=nombre)

        return genero


class PlataformaViewSet(viewsets.ModelViewSet):
    queryset = Plataforma.objects.all() 
    serializer_class = PlataformaSerializers

    def get_queryset(self):
        plataforma = Plataforma.objects.all()

        nombre = self.request.GET.get('nombre') or ''
        
        if nombre:
            plataforma = plataforma.filter(nombre__contains=nombre)

        return plataforma


class VideojuegoViewSet(viewsets.ModelViewSet):
    queryset = Videojuego.objects.all()
    serializer_class = VideojuegoSerializers

    def get_queryset(self):
        videojuegos = Videojuego.objects.all()
        titulo = self.request.GET.get('titulo') or ''
        nombre_genero = self.request.GET.get('nombregenero') or ''
        nombre_plataforma = self.request.GET.get('nombreplataforma') or ''

        if titulo:
            videojuegos = videojuegos.filter(titulo__contains = titulo)

        if nombre_genero:
            videojuegos = videojuegos.filter(genero__nombre__contains = nombre_genero )

        if nombre_plataforma:
            videojuegos = videojuegos.filter(plataforma__nombre__contains= nombre_plataforma)

        return videojuegos


class ContactenosViewSet(viewsets.ModelViewSet):
    queryset = Contactenos.objects.all()
    serializer_class = ContactenosSerializers

    def get_queryset(self):
        contactenos = Contactenos.objects.all()

        tipo_contacto = self.request.GET.get('tipocontacto') or ''

        if tipo_contacto:
            contactenos = contactenos.filter(tipo_contacto__tipo_contacto__contains= tipo_contacto)

        return contactenos    


def home(request):
    slider = Slider.objects.all()
    videojuegos = Videojuego.objects.all()
    data={
        'videojuegos': videojuegos,
        'slider': slider,
    }
    
    return render(request,'core/home.html',data )

def contactenos(request):
    data={
        'form': ContactenosForm()
    }

    if request.method=='POST':
        formulario = ContactenosForm(data= request.POST)
        if formulario.is_valid():
            formulario.save()
            data['mensaje']= 'Guardado correctamente'
        else:
            data['form']= formulario

    return render(request, 'core/contactenos.html', data)


def economia(request):
    return render(request, 'core/economia.html')

def empresa(request):
    empresa= Empresa.objects.all()
    data = {
        'empresa': empresa,
    }
    return render(request, 'core/empresa.html', data)

def galeria(request):
    galeria = Galeria.objects.all()
    data = {
        'galeria': galeria
    }
    return render(request,'core/galeria.html',data)

@permission_required('core.view_videojuego')
def listado_videojuegos(request):

    videojuegos = Videojuego.objects.all()

    busqueda= request.GET.get('busqueda') or ''

    if busqueda:
        videojuegos = videojuegos.filter(titulo__contains='busqueda')


    cantidad_videojuegos= videojuegos.count()
    menor_precio= videojuegos.aggregate(Min('precio'))
    mayor_precio= videojuegos.aggregate(Max('precio'))
    precio_promedio = videojuegos.aggregate(Avg('precio')) 
    sumatoria_precio = videojuegos.aggregate(Sum('precio'))

    data={
        'busqueda': busqueda,
        'videojuegos': videojuegos,
        'cantidad_videojuegos': cantidad_videojuegos,
        'menor_precio': menor_precio,
        'mayor_precio': mayor_precio,
        'precio_promedio': precio_promedio,
        'sumatoria_precio': sumatoria_precio,

    }
    return render(request, 'core/listado_videojuegos.html', data)

@permission_required('core.add_videojuego')
def agregar_videojuego(request):
    data={
        'form': VideojuegosForm()
    }

    if request.method=='POST':
        formulario = VideojuegosForm(data= request.POST, files= request.FILES)
        if formulario.is_valid():
            formulario.save()
            dispositivos = FCMDevice.objects.all()
            dispositivos.send_message(
                title= "Se ha agregado un nuevo videojuego ",
                body = f"Se agregó: {formulario.cleaned_data['titulo']}",
                icon = "/static/core/img/pac-man.png",
            )

            data['mensaje']= 'Guardado correctamente'
        else:
            data['form']= formulario

    return render(request, 'core/agregar_videojuegos.html', data)

@permission_required('core.change_videojuego')
def modificar_videojuego(request, id):
    videojuegos= Videojuego.objects.get(id=id)
    data={
        'form':VideojuegosForm(instance=videojuegos)
    }
    if request.method=='POST':
        formulario = VideojuegosForm(data= request.POST , instance= videojuegos, files= request.FILES)
        if formulario.is_valid():
            formulario.save()
            data['mensaje']= 'Se ha modificado correctamente'
        data['form']= formulario
    return render(request, 'core/modificar_videojuegos.html', data)

@permission_required('core.delete_videojuego')
def eliminar_videojuego(request, id):
    videojuegos = Videojuego.objects.get(id= id)
    dispositivos = FCMDevice.objects.filter(user__is_superuser=True)
    dispositivos.send_message(
        title = "Se ha eliminado un videojuego",
        body = f"Se eliminó: {videojuegos.titulo}",
        icon = "/static/core/img/pac-man.png"

    )
    videojuegos.delete()

    return redirect(to= 'listado_videojuegos')

    




def registro(request):

     
    data={
        'form': CustomerUserCreationForm()
    }

    if request.method =='POST':
        formulario = CustomerUserCreationForm(data= request.POST)
        if formulario.is_valid():
            formulario.save()
            username = formulario.cleaned_data['username']
            password = formulario.cleaned_data['password1']
            user = authenticate(username=username , password= password)
            login(request, user)
            dispositivos = FCMDevice.objects.filter(user__is_superuser=True)
            dispositivos.send_message(
                title = "Se ha registrado un nuevo usuario",
                body = f"Se registro: {formulario.cleaned_data['first_name']}",
                icon = "/static/core/img/pac-man.png"
            )

            return redirect (to= home)

        data['form']= formulario

    return render( request, 'registration/registro.html', data)