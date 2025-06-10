from django.db import models

# Sitio turístico
class Sitio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self):
        return self.nombre

# Parada de transporte (opcional si guardas paradas localmente)
class ParadaTransporte(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    onestop_id = models.CharField(max_length=100, unique=True)
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self):
        return self.nombre or self.onestop_id

# Ruta sugerida desde una parada hasta un sitio
class RutaSitio(models.Model):
    sitio = models.ForeignKey(Sitio, on_delete=models.CASCADE)
    parada_origen = models.ForeignKey(ParadaTransporte, on_delete=models.CASCADE)
    duracion_min = models.IntegerField()
    distancia_metros = models.IntegerField()

    def __str__(self):
        return f"{self.parada_origen} → {self.sitio}"

# Reseñas de los sitios
class Reseña(models.Model):
    sitio = models.ForeignKey(Sitio, on_delete=models.CASCADE, related_name='resenas')
    nombre_usuario = models.CharField(max_length=50)
    comentario = models.TextField()
    calificacion = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_usuario} - {self.sitio.nombre}"
