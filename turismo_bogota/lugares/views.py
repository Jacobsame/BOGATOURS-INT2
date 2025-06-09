import requests
from django.http import JsonResponse
from .models import Sitio
from django.shortcuts import render


def lista_sitios(request):
    sitios = Sitio.objects.all()
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

import requests
from django.conf import settings
from django.http import JsonResponse


def paradas_cercanas(request):
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")
    radius = request.GET.get("radius", "1000")

    if not lat or not lon:
        return JsonResponse({"error": "Faltan coordenadas (lat y lon)"}, status=400)

    api_key = settings.TRANSITLAND_API_KEY
    url = (
        f"https://transit.land/api/v2/rest/stops"
        f"?lat={lat}&lon={lon}&radius={radius}&api_key={api_key}"
    )

    print("🔗 URL de la API:", url)

    try:
        response = requests.get(url, timeout=10)
        print("🌐 Código de estado:", response.status_code)

        if response.status_code != 200:
            return JsonResponse({
                "error": f"Error desde Transitland (código {response.status_code})"
            }, status=response.status_code)

        data = response.json()
        print("📦 Respuesta de Transitland:", data)

        paradas = [
        {
            "nombre": parada.get("name") or "Parada sin nombre",
            "id": parada.get("onestop_id"),
            "coordenadas": parada.get("geometry", {}).get("coordinates"),
        }
        for parada in data.get("stops", [])
]

        return JsonResponse({"paradas": paradas})

    except requests.exceptions.RequestException as e:
        print("❌ Error de red:", e)
        return JsonResponse({"error": "No se pudo conectar con Transitland"}, status=503)
    
from django.shortcuts import render



def vista_mapa(request):
    return render(request, 'lugares/mapa.html')


def inicio(request):
    return render(request, "lugares/index.html")


