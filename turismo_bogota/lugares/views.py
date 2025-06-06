import requests
from django.http import JsonResponse
from .models import SitioTuristico



def lista_sitios(request):
    sitios = SitioTuristico.objects.all()
    data = [
        {
            "id": sitio.id,
            "nombre": sitio.nombre,
            "descripcion": sitio.descripcion,
            "latitud": sitio.latitud,
            "longitud": sitio.longitud,
        }
        for sitio in sitios
    ]
    return JsonResponse({"sitios": data})



from django.conf import settings  # Importar settings

from django.conf import settings
import requests
from django.http import JsonResponse


def paradas_cercanas(request):
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")
    radius = request.GET.get("radius", "1000")

    if not lat or not lon:
        return JsonResponse({"error": "Faltan coordenadas"}, status=400)

    api_key = settings.TRANSITLAND_API_KEY

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    url = f"https://transit.land/api/v2/rest/stops?lat={lat}&lon={lon}&r={radius}"
    print("🔗 URL de la API:", url)
    print("🔐 Encabezados:", headers)

    response = requests.get(url, headers=headers)
    data = response.json()

    print("📦 Respuesta de Transitland:", data)  # <-- MUY IMPORTANTE

    paradas = [
        {
            "nombre": parada.get("name"),
            "id": parada.get("onestop_id"),
            "coordenadas": parada.get("geometry", {}).get("coordinates"),
        }
        for parada in data.get("stops", [])
    ]
    return JsonResponse({"paradas": paradas})
