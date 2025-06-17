from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('sitios/', views.lista_sitios, name='lista_sitios'),
    path('paradas-cercanas/', views.paradas_cercanas, name='paradas_cercanas'),
    path('mapa/', views.vista_mapa, name='vista_mapa'),
    path("", views.inicio, name="inicio"), 
    path("importar-paradas/", views.importar_paradas, name="importar_paradas"),
    path("registro/", views.registro, name="registro"),
    path('login/', auth_views.LoginView.as_view(template_name='lugares/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]


