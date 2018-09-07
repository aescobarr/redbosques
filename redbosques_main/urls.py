from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('herramientas', views.herramientas, name='herramientas'),
    path('datos_mapa', views.datos_mapa, name='datos_mapa'),
    path('datos_habitat', views.datos_habitat, name='datos_habitat'),
]