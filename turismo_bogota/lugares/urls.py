from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('sitios/', views.lista_sitios, name='lista_sitios'),
    path('paradas-cercanas/', views.paradas_cercanas, name='paradas_cercanas'),
]
