from django.shortcuts import render
from redbosques_main.models import WebMapa, Habitat, Rodal, RodalValorres
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
def index(request):
    context = {'titol': 'Titol'}
    return render(request, 'redbosques_main/index.html', context)

def herramientas(request):
    dades_habitat_contenidors = Habitat.objects.filter(seleccion = True).exclude(cod='4').exclude(cod__contains='.').order_by('nombre')

    # Retorna el llistat dels rodals
    ids_habitat_web = WebMapa.objects.filter(eje_cod='nm').values('id_rodal')
    llista_rodals = Rodal.objects.filter(id__in=ids_habitat_web).order_by('nombre')

    context = {'herramientas': 'Herramienta de evaluación de rodales maduros', 'dades_habitat_contenidors' : dades_habitat_contenidors, 'llista_rodals':llista_rodals}
    return render(request, 'redbosques_main/herramientas.html', context)


@api_view(['GET'])
def datos_habitat(request):
    codi_hab = request.query_params.get('h', None)
    llista_habitats = []

    if not codi_hab is None:
        dades_habitat = Habitat.objects.filter(seleccion = True).filter(cod__startswith=codi_hab).filter(cod__contains='.').order_by('nombre')
        for habitat in dades_habitat:
            llista_habitats.append({'cod': habitat.cod, 'nombre': habitat.nombre})

    return Response(llista_habitats)



# Retorna totes les dades de la vista web_mapa per poder generar els punts en el mapa
@api_view(['GET'])
def datos_mapa(request):

    #Filtraje por tipo de eje
    eje_selected = request.query_params.get('e', None)
    dades_punts = WebMapa.objects.filter(eje_cod=eje_selected)


    # rebem com a parametre el codir del rodal
    codi_rodal = request.query_params.get('cr', None)


    if codi_rodal is not None:
        dades_punts = dades_punts.filter(id_rodal=codi_rodal)



    codi_hab = request.query_params.get('h', None)
    llista_habitats = []

    if not codi_hab is None:
        dades_habitat = Habitat.objects.filter(seleccion=True).filter(cod__startswith=codi_hab).filter(
            cod__contains='.').order_by('nombre')
        for habitat in dades_habitat:
            llista_habitats.append({'cod': habitat.cod, 'nombre': habitat.nombre})

        dades_punts = dades_punts.filter(habitat_cod__startswith=codi_hab)

    codi_tipus_habitat = request.query_params.get('ch', None)


    if codi_tipus_habitat is not None:
        #dades_punts = dades_punts.filter(habitat_cod=codi_tipus_habitat)
        dades_punts = dades_punts.filter(habitat_cod__startswith=codi_tipus_habitat)


    valoracio = request.query_params.getlist('val_valor') or None


    if codi_tipus_habitat is not None:
        dades_punts = dades_punts.filter(habitat_cod__startswith=codi_tipus_habitat)

    if valoracio is not None:
        dades_punts = dades_punts.filter(valor__in=valoracio)


    llista_punts = []
    for punt in dades_punts:
        llista_punts.append({
            'id_rodal':punt.id_rodal,
            'x':punt.geom.x,
            'y':punt.geom.y,
            'nombre': punt.nombre,
            'Comunidad_autonoma': punt.ccaa_nombre,
            'habitat_nom': punt.habitat_nom,
            'valor': punt.valor
        })


    context = {'llista_punts': llista_punts, 'llista_habitats': llista_habitats}
    return Response(context)
    '''return Response(llista_punts)'''


def menu(request):
    context = {'herramientas': 'Herramienta de evaluación de rodales maduros'}
    return render(request, 'redbosques_main/menu.html', context)


'''@api_view(['GET'])'''
def comparador(request, id=None):
    # rebem com a parametre el codir del rodal
    #codi_rodal = request.query_params.get('cr', None)
    if id is not None:
        dades_rodal = RodalValorres.objects.filter(_id=id)

    context = {'herramientas': 'Herramienta de evaluación de rodales maduros', 'dades_rodal': dades_rodal}
    return render(request, 'redbosques_main/comparador.html', context)