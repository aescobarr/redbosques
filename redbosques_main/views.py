from django.shortcuts import render
from redbosques_main.models import WebMapa, Habitat
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
def index(request):
    context = {'titol': 'Titol'}
    return render(request, 'redbosques_main/index.html', context)

def herramientas(request):
    dades_habitat_contenidors = Habitat.objects.filter(seleccion = True).exclude(cod='4').exclude(cod__contains='.').order_by('nombre')
    context = {'herramientas': 'Herramienta de evaluación de rodales maduros', 'dades_habitat_contenidors' : dades_habitat_contenidors}
    return render(request, 'redbosques_main/herramientas.html', context)


@api_view(['GET'])
def datos_habitat(request):
    codi_hab = request.query_params.get('h', None)
    llista_habitats = []
    if not codi_hab is None:
        dades_habitat = Habitat.objects.filter(seleccion = True).filter(cod__startswith=codi_hab).filter(cod__contains='.').order_by('nombre')
        for habitat in dades_habitat:
            llista_habitats.append({'cod':habitat.cod,'nombre':habitat.nombre})
    return Response(llista_habitats)

# Retorna totes les dades de la vista web_mapa per poder generar els punts en el mapa
@api_view(['GET'])
def datos_mapa(request):
    dades_punts = WebMapa.objects.filter(eje_cod='hh')
    llista_punts = []
    for punt in dades_punts:
        llista_punts.append({
            'id_rodal':punt.id_rodal,
            'x':punt.geom.x,
            'y':punt.geom.y,
            'nombre': punt.nombre,
            'Comunidad_autonoma': punt.ccaa_nombre,
            'habitat_nom': punt.habitat_nom
        })
    return Response(llista_punts)