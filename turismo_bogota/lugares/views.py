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

import requests
from django.conf import settings
from django.http import JsonResponse
from .models import ParadaTransporte

def importar_paradas(request):
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")
    radius = request.GET.get("radius", 1500)

    if not lat or not lon:
        return JsonResponse({"error": "Faltan coordenadas"}, status=400)

    headers = {
        "Authorization": f"Bearer {settings.TRANSITLAND_API_KEY}"
    }

    url = f"https://transit.land/api/v2/rest/stops?lat={lat}&lon={lon}&r={radius}"
    response = requests.get(url, headers=headers)
    data = response.json()

    nuevas = 0
    for parada in data.get("stops", []):
        nombre = parada.get("name") or ""
        onestop_id = parada.get("onestop_id")
        coords = parada.get("geometry", {}).get("coordinates")

        if onestop_id and coords:
            _, created = ParadaTransporte.objects.get_or_create(
                onestop_id=onestop_id,
                defaults={
                    "nombre": nombre,
                    "latitud": coords[1],
                    "longitud": coords[0],
                }
            )
            if created:
                nuevas += 1

    return JsonResponse({"mensaje": f"✅ {nuevas} paradas nuevas guardadas."})


def vista_mapa(request):
    return render(request, 'lugares/mapa.html')


def inicio(request):
    return render(request, "lugares/index.html")

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not all([username, email, password]):
            messages.error(request, 'Por favor completa todos los campos.')
            return render(request, 'lugares/registro.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Este nombre de usuario ya existe.')
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect('login')  # Redirige al login si tienes uno

    return render(request, 'lugares/registro.html')






