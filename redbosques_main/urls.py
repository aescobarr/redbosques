from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu', views.menu, name='menu'),
    path('login', views.login, name='login'),
    path('comparador', views.comparador, name='comparador_noparam'),
    path('comparador/<int:id>/', views.comparador, name='comparador'),
    path('comparador/<int:id>/filter', views.filtrosRodal, name='filtrosRodal'),
    path('valorRef', views.valorRef, name='valorRef'),
    path('setFiltrosRodal', views.setFiltrosRodal, name='setFiltrosRodal'),
    path('herramientas', views.herramientas, name='herramientas'),
    path('datos_mapa', views.datos_mapa, name='datos_mapa'),
    path('datos_habitat', views.datos_habitat, name='datos_habitat'),
]