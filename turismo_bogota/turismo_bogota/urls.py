from django.contrib import admin
from django.urls import path, include
from lugares import views  # Importamos las vistas desde la app correcta

urlpatterns = [
    
    path('api/', include('lugares.urls')),  # Incluye todas las rutas de la app
    path('paradas-cercanas/', views.paradas_cercanas, name='paradas_cercanas'),  # Esta ruta extra si la necesitas aparte
    path("admin/", admin.site.urls),
    path("", include("lugares.urls")),
]


