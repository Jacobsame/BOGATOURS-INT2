from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Sitio turístico
class Sitio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self):
        return self.nombre

class ParadaTransporte(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    onestop_id = models.CharField(max_length=100, unique=True)
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self):
        return self.nombre or self.onestop_id

class RutaSitio(models.Model):
    sitio = models.ForeignKey(Sitio, on_delete=models.CASCADE)
    parada_origen = models.ForeignKey(ParadaTransporte, on_delete=models.CASCADE)
    duracion_min = models.IntegerField()
    distancia_metros = models.IntegerField()

    def __str__(self):
        return f"{self.parada_origen} → {self.sitio}"

class LugarTuristico(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=255)
    ubicacion = models.CharField(max_length=255)
    horarios = models.CharField(max_length=255)
    costo = models.CharField(max_length=100)
    imagen = models.URLField()

    def __str__(self):
        return self.nombre

# Reseñas genéricas (pueden ser para Sitio o LugarTuristico)
class Reseña(models.Model):
    nombre_usuario = models.CharField(max_length=50)
    comentario = models.TextField()
    calificacion = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    fecha = models.DateTimeField(auto_now_add=True)

    # Relación genérica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    contenido_objeto = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"{self.nombre_usuario} - {self.content_type} ({self.object_id})"
