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


from django.http import JsonResponse
from .models import LugarTuristico
from django.views.decorators.csrf import csrf_exempt


def api_inicio(request):
    return JsonResponse({"mensaje": "Bienvenido a la API de búsqueda de lugares turísticos de Bogotá. Usa /buscar para buscar lugares."})

def buscar_lugares(request):
    query = request.GET.get("q", "").lower()
    tipo = request.GET.get("tipo", "").lower()
    lugares = LugarTuristico.objects.all()

    resultados = []
    for lugar in lugares:
        tipos = [t.strip().lower() for t in lugar.tipo.split(",")]
        if (not query or query in lugar.nombre.lower() or query in lugar.descripcion.lower()) and (not tipo or tipo in tipos):
            resultados.append({
                "id": lugar.id,
                "nombre": lugar.nombre,
                "descripcion": lugar.descripcion,
                "tipo": tipos,
                "ubicacion": lugar.ubicacion,
                "horarios": lugar.horarios,
                "costo": lugar.costo,
                "imagen": lugar.imagen
            })

    return JsonResponse(resultados, safe=False)

def obtener_lugar_por_id(request, lugar_id):
    try:
        lugar = LugarTuristico.objects.get(pk=lugar_id)
        return JsonResponse({
            "id": lugar.id,
            "nombre": lugar.nombre,
            "descripcion": lugar.descripcion,
            "tipo": lugar.tipo,
            "ubicacion": lugar.ubicacion,
            "horarios": lugar.horarios,
            "costo": lugar.costo,
            "imagen": lugar.imagen
        })
    except LugarTuristico.DoesNotExist:
        return JsonResponse({"error": "Lugar no encontrado"}, status=404)

from django.shortcuts import render
from .models import LugarTuristico

def lugares_turisticos(request):
    lugares = LugarTuristico.objects.all()
    return render(request, 'lugares/lugares_turisticos.html', {'lugares': lugares})

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Sitio, Reseña

def index(request):
    sitios = Sitio.objects.all()
    return render(request, 'lugares/index.html', {"sitios": sitios})

def detalles_sitio(request, sitio_id):
    sitio = get_object_or_404(Sitio, id=sitio_id)
    reseñas = sitio.resenas.order_by('-fecha').values("nombre_usuario", "comentario", "calificacion", "fecha")
    data = {
        "nombre": sitio.nombre,
        "descripcion": sitio.descripcion,
        "latitud": sitio.latitud,
        "longitud": sitio.longitud,
        "reseñas": list(reseñas)
    }
    return JsonResponse(data)

def buscar_lugar(request):
    query = request.GET.get("q", "").strip().lower()
    sitio = Sitio.objects.filter(nombre__icontains=query).first()

    if not sitio:
        return JsonResponse({"error": "Lugar no encontrado"}, status=404)

    return JsonResponse({"id": sitio.id})

from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
def enviar_resena(request):
    data = json.loads(request.body)
    sitio = get_object_or_404(Sitio, id=data["sitio_id"])
    Reseña.objects.create(
        sitio=sitio,
        nombre_usuario=data["nombre_usuario"],
        comentario=data["comentario"],
        calificacion=data["calificacion"]
    )
    return JsonResponse({"ok": True})




