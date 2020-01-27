from django import forms
from .models import Videojuego, Slider, Galeria, Contactenos
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import sys
from itertools import cycle

class VideojuegosForm(forms.ModelForm):
    titulo = forms.CharField(required = True, min_length= 3, max_length=80)
    #descripcion = forms.CharField(min_length= 3, max_length=200)

    class Meta:
        model = Videojuego
        fields = ['titulo', 'genero', 'plataforma', 'descripcion', 'caratula', 'precio']


class SliderForm(forms.ModelForm):

    class Meta:
        model = Slider
        fields = ['imagen', 'texto']


class CustomerUserCreationForm(UserCreationForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        cantidad_email = User.objects.filter(email=email).count()
        
        if cantidad_email > 0 :
            raise forms.ValidationError("El email ya existe, ingrese uno diferente")

        return email
    

    class Meta: 
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']


class ContactenosForm(forms.ModelForm):

    def clean_rut(self):
        rut= self.cleaned_data['rut']
        rut = rut.upper()
        rut = rut.replace("-","")
        rut = rut.replace(".","")
        aux = rut[:-1]
        dv = rut[-1:]
    
        revertido = map(int, reversed(str(aux)))
        factors = cycle(range(2,8))
        s = sum(d * f for d, f in zip(revertido,factors))
        res = (-s)%11
    
        if str(res) == dv:
            return True
        elif dv=="K" and res==10:
            return True
        else:
            raise forms.ValidationError("El rut es invalido")
        
        return rut
    

    

    nombre = forms.CharField(required=True,min_length=3)
    apellido = forms.CharField(min_length=3)
    asunto = forms.CharField(min_length=8)
    class Meta:
        model = Contactenos
        fields = ['rut', 'nombre', 'apellido', 'asunto', 'tipo_contacto', 'mensaje']