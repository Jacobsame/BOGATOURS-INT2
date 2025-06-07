from django.contrib import admin
from .models import Sitio

@admin.register(Sitio)
class SitioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'latitud', 'longitud')
