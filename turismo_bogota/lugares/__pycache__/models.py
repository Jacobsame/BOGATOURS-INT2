from django.db import models

# Create your models here.
from django.db import models

class SitioTuristico(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self):
        return self.nombre
