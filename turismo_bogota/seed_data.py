from lugares.models import Sitio, ParadaTransporte, RutaSitio, Reseña

# Sitios turísticos
sitios_data = [
    {"nombre": "Monserrate", "descripcion": "Mirador icónico de Bogotá.", "latitud": 4.605, "longitud": -74.055},
    {"nombre": "Museo del Oro", "descripcion": "Museo con artefactos precolombinos.", "latitud": 4.601, "longitud": -74.072},
    {"nombre": "Plaza de Bolívar", "descripcion": "Centro histórico de Bogotá.", "latitud": 4.598, "longitud": -74.074},
]

sitios_creados = {}
for data in sitios_data:
    sitio, _ = Sitio.objects.get_or_create(nombre=data["nombre"], defaults=data)
    sitios_creados[data["nombre"]] = sitio

# Paradas de transporte (ejemplo desde API o manual)
paradas_data = [
    {"nombre": "Estación Museo del Oro", "onestop_id": "s-bog-museo", "latitud": 4.6005, "longitud": -74.071},
    {"nombre": "Estación Aguas", "onestop_id": "s-bog-aguas", "latitud": 4.598, "longitud": -74.076},
]

paradas_creadas = {}
for data in paradas_data:
    parada, _ = ParadaTransporte.objects.get_or_create(onestop_id=data["onestop_id"], defaults=data)
    paradas_creadas[data["nombre"]] = parada

# Rutas desde paradas a sitios turísticos
rutas_data = [
    {
        "parada": "Estación Museo del Oro",
        "sitio": "Museo del Oro",
        "duracion_min": 4,
        "distancia_metros": 300,
    },
    {
        "parada": "Estación Aguas",
        "sitio": "Plaza de Bolívar",
        "duracion_min": 6,
        "distancia_metros": 500,
    },
]

for ruta in rutas_data:
    RutaSitio.objects.get_or_create(
        sitio=sitios_creados[ruta["sitio"]],
        parada_origen=paradas_creadas[ruta["parada"]],
        defaults={
            "duracion_min": ruta["duracion_min"],
            "distancia_metros": ruta["distancia_metros"],
        }
    )

# Reseñas
resenas_data = [
    {"sitio": "Monserrate", "nombre_usuario": "Camila", "comentario": "La vista es espectacular.", "calificacion": 5},
    {"sitio": "Museo del Oro", "nombre_usuario": "Carlos", "comentario": "Muy interesante para conocer la historia.", "calificacion": 4},
    {"sitio": "Plaza de Bolívar", "nombre_usuario": "Laura", "comentario": "Ideal para tomar fotos.", "calificacion": 4},
]

for data in resenas_data:
    Reseña.objects.get_or_create(
        sitio=sitios_creados[data["sitio"]],
        nombre_usuario=data["nombre_usuario"],
        comentario=data["comentario"],
        calificacion=data["calificacion"],
    )

print("✅ Datos insertados con éxito en Sitio, ParadaTransporte, RutaSitio y Reseña.")
