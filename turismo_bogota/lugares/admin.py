from django.contrib import admin
    
from .models import Sitio, ParadaTransporte, RutaSitio, Reseña

@admin.register(Sitio)
class SitioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'latitud', 'longitud')

@admin.register(ParadaTransporte)
class ParadaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'latitud', 'longitud')

@admin.register(RutaSitio)
class RutaAdmin(admin.ModelAdmin):
    list_display = ('parada_origen', 'sitio', 'duracion_min', 'distancia_metros')

@admin.register(Reseña)
class ReseñaAdmin(admin.ModelAdmin):
    list_display = ('sitio', 'nombre_usuario', 'calificacion', 'fecha')