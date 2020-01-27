from django.db import models

# Create your models here.
class Genero(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre


class Plataforma(models.Model):
    nombre = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre


class Videojuego(models.Model):
    titulo = models.CharField(max_length=80)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    plataforma = models.ForeignKey(Plataforma, on_delete= models.CASCADE)
    descripcion = models.TextField( null=True,blank=True,max_length=200)
    caratula = models.ImageField(null=True,blank=True)
    precio= models.IntegerField()

    def __str__(self):
        return self.titulo


class Slider(models.Model):
    imagen = models.ImageField()
    texto = models.CharField(null=True, blank=True, max_length= 100)
    
    def __str__(self):
        return self.imagen.url


class Galeria(models.Model):
    imagen = models.ImageField()

    def __str__(self):
        return self.imagen.url


class Tipo_contacto(models.Model):
    tipo_contacto = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Tipo contacto"
        verbose_name_plural = "Tipo contacto"


    def __str__(self):
        return self.tipo_contacto


class Contactenos(models.Model):
    rut = models.CharField(max_length=12)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    asunto = models.CharField(max_length=80)
    tipo_contacto = models.ForeignKey(Tipo_contacto, on_delete= models.CASCADE)
    mensaje = models.TextField(null=True,blank=True,max_length=200)
    
    class Meta:
        verbose_name = "Contactenos"
        verbose_name_plural = "Contactenos"
    def __str__(self):
        return self.nombre


class Empresa(models.Model):
    historia = models.TextField()
    vision = models.TextField()
    mision = models.TextField()

    def __str__(self):
        return self.historia