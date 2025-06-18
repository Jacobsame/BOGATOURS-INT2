from django.contrib import admin
from .models import Sitio, ParadaTransporte, RutaSitio, LugarTuristico, Reseña

@admin.register(Sitio)
class SitioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'latitud', 'longitud')

@admin.register(ParadaTransporte)
class ParadaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'latitud', 'longitud')

@admin.register(RutaSitio)
class RutaAdmin(admin.ModelAdmin):
    list_display = ('sitio', 'parada_origen', 'duracion_min', 'distancia_metros')

@admin.register(LugarTuristico)
class LugarTuristicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'costo')

@admin.register(Reseña)
class ReseñaAdmin(admin.ModelAdmin):
    list_display = ('nombre_usuario', 'get_objetivo', 'calificacion', 'fecha')

    def get_objetivo(self, obj):
        return f"{obj.content_type.name} #{obj.object_id}"
    get_objetivo.short_description = "Relacionado a"
