from django.urls import path
from django.conf.urls import url, include
from . import views

from django.contrib import admin
from django.contrib.auth import views as auth_views
from redbosques.forms import LoginForm

urlpatterns = [
    path('', views.index, name='index'),
    path('menu', views.menu, name='menu'),
    #path('login', views.login,  kwargs={ "authentication_form": AuthenticationForm}),
    #path('login', views.login, { "authentication_form": AuthenticationForm}, name='login'),
    path('login', views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^login/$', views.login, name='login'),
    path('register', views.register, name='register'),
    path('comparador', views.comparador, name='comparador_noparam'),
    path('comparador/<int:id>/', views.comparador, name='comparador'),
    path('comparador/<int:id>/filter', views.filtrosRodal, name='filtrosRodal'),
    path('valorRef', views.valorRef, name='valorRef'),
    path('setFiltrosRodal', views.setFiltrosRodal, name='setFiltrosRodal'),
    path('herramientas', views.herramientas, name='herramientas'),
    path('habitatData', views.habitatData, name='habitatData'),
    path('subHabitatData', views.subHabitatData, name='subHabitatData'),
    path('rodalData', views.rodalData, name='rodalData'),
    path('dataCleaner', views.dataCleaner, name='dataCleaner'),
    path('datos_mapa', views.datos_mapa, name='datos_mapa'),
    url(r'^register/$', views.register, name='register'),


]
