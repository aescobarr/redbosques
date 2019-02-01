from django.urls import path
from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.auth import views as auth_views
from redbosques.forms import LoginForm

urlpatterns = [
    path('', views.index, name='index'),
    path('menu', views.menu, name='menu'),
    path('login', views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^login/$', views.login, name='login'),
    path('register', views.register, name='register'),
    path('comparador', views.comparador, name='comparador_noparam'),
    path('comparador/<int:id>/', views.comparador, name='comparador'),
    path('comparador_new/', views.comparador_new, name='comparador_new'),
    path('comparador_new/<int:id>/', views.comparador_new, name='comparador_new'),
    path('comparador/<int:id>/filter', views.filtrosRodal, name='filtrosRodal'),
    path('valorRef', views.valorRef, name='valorRef'),
    path('valorRodal', views.valorRodal, name='valorRodal'),
    path('setFiltrosRodal', views.setFiltrosRodal, name='setFiltrosRodal'),
    path('herramientas', views.herramientas, name='herramientas'),
    path('herramientas/<int:id>/', views.herramientas, name='herramientas'),
    path('habitatData', views.habitatData, name='habitatData'),
    path('subHabitatData', views.subHabitatData, name='subHabitatData'),
    path('rodalData', views.rodalData, name='rodalData'),
    path('ambitoData', views.ambitoData, name='ambitoData'),
    path('dataCleaner', views.dataCleaner, name='dataCleaner'),
    path('datos_mapa', views.datos_mapa, name='datos_mapa'),
    url(r'^register/$', views.register, name='register'),
    path('rodalForm', views.rodalForm, name='rodalForm'),
    path('rodalForm2/<int:id>/', views.rodalForm2, name='rodalForm2'),
    path('rodalForm3/<int:id>/', views.rodalForm3, name='rodalForm3'),
    path('uploadImage/<int:id>/', views.uploadImage, name='uploadImage'),
    path('eliminarImagen/<int:id>/', views.deleteImage, name='eliminarImagen'),

    path('uploadDocs/<int:id>/', views.uploadDocs, name='uploadDocs'),
    path('eliminarDoc/<int:id>/', views.deleteDoc, name='eliminarDoc'),

    path('filtraxhabitat', views.filtraxhabitat, name='filtraxhabitat'),
    path('filtrarxComAut', views.filtrarxComAut, name='filtrarxComAut'),
    path('filtrarxRegBiogeo', views.filtrarxRegBiogeo, name='filtrarxRegBiogeo'),
    path('filtrarxRodRef', views.filtrarxRodRef, name='filtrarxRodRef'),
    path('filtraxtipobosque', views.filtraxtipobosque, name='filtraxtipobosque'),
    path('habitats_ajax',views.habitats_ajax,name="habitats_ajax"),
    path('ccaa_ajax',views.ccaa_ajax,name="ccaa_ajax"),
    path('regbiogeo_ajax',views.regbiogeo_ajax,name="regbiogeo_ajax"),
    path('rodals_ajax',views.rodals_ajax,name="rodals_ajax"),
    path('valorref_ajax',views.valorref_ajax,name="valorref_ajax"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





