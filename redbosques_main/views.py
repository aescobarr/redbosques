from django.shortcuts import render, redirect, get_object_or_404
from redbosques_main.models import WebMapa, Habitat, Rodal, RodalValorres2, TeRegbio, TeProvincia, RodalValoresAmbito, WebMapaValAmb, WebCompData, WebCompDataValAmb, TeHic, TeLpeht, Tesaurus, User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
import decimal
import json
from django.db.models import Avg, StdDev
from redbosques.settings_local import URL_BASE
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from redbosques.forms import RegistrationForm, LoginForm, rodalFormFields, rodalFormFields2, rodalFormFields3
from django.contrib import messages
from django.contrib import auth
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from django.contrib.auth import authenticate

import pyproj
from shapely.geometry import shape
from shapely.ops import transform
from functools import partial
import shapely.wkt

from django.db import connection
from collections import namedtuple
from django.http import HttpResponseRedirect



def namedtuplefetchall(cursor):
    #Return all rows from a cursor as a namedtuple
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]





# Create your views here.
def index(request):
    context = {'titol': 'Titol', 'URL_BASE': URL_BASE}
    return render(request, 'redbosques_main/index.html', context)

@login_required(login_url="login/")
def menu(request):
    rodalesSelector = []
    rodals_list = WebMapa.objects.filter(eje_cod='nm').order_by('nombre')

    for r in rodals_list:
        rodalesSelector.append({'id_rodal': r.id_rodal, 'nombre': r.nombre})

    context = {'herramientas': 'Herramienta de evaluación de rodales maduros', 'rodalesSelector':rodalesSelector}
    return render(request, 'redbosques_main/menu.html', context)



def initialData():
    # Carga de datos para el selector de Habitat
    habitatData=[]
    habData = Habitat.objects.filter(seleccion=True).exclude(cod='4').exclude(cod__contains='.').order_by('nombre')
    for h in habData:
        habitatData.append({'cod': h.cod, 'nombre': h.nombre})

    subHabExist = []
    subHabitatData = []
    allSub = WebMapaValAmb.objects.all()
    allSub2 = allSub.filter(eje_cod='nm').values_list('habitat_cod', flat=True)

    subHabExist = Habitat.objects.filter(cod__in=allSub2.values_list('habitat_cod', flat=True)).order_by('nombre')

    for habitat in subHabExist:
        subHabitatData.append({'cod': habitat.cod, 'nombre': habitat.nombre})

    # Carga de datos para el selector de Rodales
    rodalesData = []
    rodales = WebMapaValAmb.objects.filter(eje_cod='nm').order_by('nombre')
    for r in rodales:
        rodalesData.append({'id_rodal': r.id_rodal, 'nombre': r.nombre})

    # context = {'herramientas': 'Herramienta de evaluación de rodales maduros', 'habitatData': habitatData, 'llista_rodals':llista_rodals, 'URL_BASE': URL_BASE}
    context = {'herramientas': 'Herramienta de evaluación de rodales maduros',
               'habitatData': habitatData,
               'subHabitatData': subHabitatData,
               'rodalesData': rodalesData}

    return context

@login_required(login_url="login/")
def herramientas(request, id=None):

    if id is None:
        #context = initialData()
        data = initialData()
        context = {'initial_data': data, 'coordenadas_rodal': 'null'}
    else:
        coordenadas_rodal = cordRodal(id)
        data = initialData()
        context = {'initial_data': data, 'coordenadas_rodal': coordenadas_rodal}

    return render(request, 'redbosques_main/herramientas.html', context)


def cordRodal(id):

    rodal = WebMapaValAmb.objects.filter(id_rodal=id).filter(eje_cod='nm')

    coordenadas_rodal = []
    for punt in rodal:
        coordenadas_rodal.append({
            'id_rodal': punt.id_rodal,
            'x': punt.geom.x,
            'y': punt.geom.y,
            'nombre': punt.nombre
        })

    return coordenadas_rodal





@api_view(['GET'])
def dataCleaner(request):
    resultado = initialData()
    return Response(resultado)



@api_view(['GET'])
def habitatData(request):
    #habitatData2 = Habitat.objects.filter(seleccion=True).exclude(cod='4').exclude(cod__contains='.').order_by('nombre')

    codiHabitat = request.query_params.get('ch', None)
    codiAmbito = request.query_params.get('ca', None)

    newSubHabitatData = []
    newRodalesData = []


    subHabExist = []
    allSub = WebMapaValAmb.objects.all()
    allSub2 = allSub.filter(eje_cod='nm').values_list('habitat_cod', flat=True)

    subHabExist = Habitat.objects.filter(cod__in=allSub2.values_list('habitat_cod', flat=True))

    if codiHabitat == 'null':
        subHabExistFilter = subHabExist.filter(cod__contains='.').order_by('nombre')
        rodales = WebMapaValAmb.objects.filter(eje_cod=codiAmbito).order_by('nombre')
    else:
        subHabExistFilter = subHabExist.filter(cod__startswith=codiHabitat).filter(cod__contains='.').order_by('nombre')
        rodales = WebMapaValAmb.objects.filter(eje_cod=codiAmbito).filter(habitat_cod__startswith=codiHabitat).order_by('nombre')

    for habitat in subHabExistFilter:
        newSubHabitatData.append({'cod': habitat.cod, 'nombre': habitat.nombre})

    for r in rodales:
        newRodalesData.append({
            'id_rodal':r.id_rodal,
            'x':r.geom.x,
            'y':r.geom.y,
            'nombre': r.nombre,
            'Comunidad_autonoma': r.ccaa_nombre,
            'habitat_nom': r.habitat_nom,
            'tipobosque_nombre': r.tipobosque_nombre,
            'valor': r.valor,
            'imagen': r.fotoglobo,
            'valor_hh': r.hh,
            'valor_ie': r.ie,
            'valor_nm': r.nm,
            'regionBiogeo': r.nombre_es
        })

    context = {'newSubHabitatData': newSubHabitatData, 'newRodalesData': newRodalesData}
    return Response(context)



@api_view(['GET'])
def subHabitatData(request):
    codiSubhabitat = request.query_params.get('csh', None)
    codiAmbito = request.query_params.get('ca', None)

    newRodalesData2 = []

    if codiSubhabitat == 'null':
        rodales = WebMapaValAmb.objects.filter(eje_cod=codiAmbito).order_by('nombre')
    else:
        rodales = WebMapaValAmb.objects.filter(eje_cod=codiAmbito).filter(habitat_cod__startswith=codiSubhabitat).order_by('nombre')


    for r in rodales:
        newRodalesData2.append({
            'id_rodal':r.id_rodal,
            'x':r.geom.x,
            'y':r.geom.y,
            'nombre': r.nombre,
            'Comunidad_autonoma': r.ccaa_nombre,
            'habitat_nom': r.habitat_nom,
            'tipobosque_nombre': r.tipobosque_nombre,
            'valor': r.valor,
            'imagen': r.fotoglobo,
            'valor_hh': r.hh,
            'valor_ie': r.ie,
            'valor_nm': r.nm,
            'regionBiogeo': r.nombre_es
        })

    context = {'newRodalesData2': newRodalesData2}
    return Response(context)


@api_view(['GET'])
def rodalData(request):
    codiRodal = request.query_params.get('cr', None)
    codiAmbito = request.query_params.get('ca', None)
    rodalData = []

    if codiRodal == 'null':
        rod = WebMapaValAmb.objects.filter(eje_cod=codiAmbito).order_by('nombre')
    else:
        rod = WebMapaValAmb.objects.filter(id_rodal=codiRodal).filter(eje_cod=codiAmbito).order_by('nombre')

    for r in rod:
        rodalData.append({
            'id_rodal':r.id_rodal,
            'x':r.geom.x,
            'y':r.geom.y,
            'nombre': r.nombre,
            'Comunidad_autonoma': r.ccaa_nombre,
            'habitat_nom': r.habitat_nom,
            'tipobosque_nombre': r.tipobosque_nombre,
            'valor': r.valor,
            'imagen': r.fotoglobo,
            'valor_hh': r.hh,
            'valor_ie': r.ie,
            'valor_nm': r.nm,
            'regionBiogeo': r.nombre_es
        })

    context = {'rodalData': rodalData}
    return Response(context)



@api_view(['GET'])
def ambitoData(request):

    codiAmbito = request.query_params.get('ca', None)
    #print(codiAmbito)

    rodalData = []
    rod = WebMapa.objects.filter(eje_cod=codiAmbito).order_by('nombre')

    for r in rod:
        rodalData.append({'id_rodal': r.id_rodal, 'nombre': r.nombre})

    context = {'rodalData': rodalData}
    return Response(context)




# Retorna totes les dades de la vista web_mapa per poder generar els punts en el mapa
@api_view(['GET'])
def datos_mapa(request):
    codi_hab = request.query_params.get('h', None)
    codi_tipus_habitat = request.query_params.get('csh', None)
    eje_selected = request.query_params.get('e', None)
    codi_rodal = request.query_params.get('cr', None)

    #Filtraje por tipo de eje
    #dades_punts = WebMapa.objects.filter(eje_cod=eje_selected)
    dades_punts = WebMapaValAmb.objects.filter(eje_cod=eje_selected)

    # rebem com a parametre el codir del rodal
    if codi_rodal is not None:
        dades_punts = dades_punts.filter(id_rodal=codi_rodal)


    codi_hab = request.query_params.get('h', None)
    llista_habitats = []

    if not codi_hab is None:
        dades_habitat = Habitat.objects.filter(seleccion=True).filter(cod__startswith=codi_hab).filter(cod__contains='.').order_by('nombre')
        for habitat in dades_habitat:
            llista_habitats.append({'cod': habitat.cod, 'nombre': habitat.nombre})

        dades_punts = dades_punts.filter(habitat_cod__startswith=codi_hab)


    if codi_tipus_habitat is not None:
        #dades_punts = dades_punts.filter(habitat_cod=codi_tipus_habitat)
        dades_punts = dades_punts.filter(habitat_cod__startswith=codi_tipus_habitat)


    #valoracio = request.query_params.getlist('val_valor') or None

    llista_punts = []
    for punt in dades_punts:
        llista_punts.append({
            'id_rodal':punt.id_rodal,
            'x':punt.geom.x,
            'y':punt.geom.y,
            'nombre': punt.nombre,
            'Comunidad_autonoma': punt.ccaa_nombre,
            'habitat_nom': punt.habitat_nom,
            'tipobosque_nombre': punt.tipobosque_nombre,
            'valor': punt.valor,
            'imagen': punt.fotoglobo,
            'valor_hh': punt.hh,
            'valor_ie': punt.ie,
            'valor_nm': punt.nm,
            'regionBiogeo': punt.nombre_es
        })

    context = {'llista_punts': llista_punts, 'llista_habitats': llista_habitats}
    return Response(context)


def comparador(request, id=None):
    # rebem com a parametre el codir del rodal
    #codi_rodal = request.query_params.get('cr', None)

    all = WebCompDataValAmb.objects.all()
    allHab = all.filter(eje_cod='nm').values_list('habitat_cod', flat=True)

    habitatData = []
    #habData = Habitat.objects.filter(seleccion=True).exclude(cod='4').filter(cod__contains='.').order_by('nombre')
    habData = Habitat.objects.filter(cod__in=allHab.values_list('habitat_cod', flat=True)).filter(seleccion=True).exclude(cod='4').filter(cod__contains='.').order_by('nombre')

    for h in habData:
        habitatData.append({'cod': h.cod, 'nombre': h.nombre})

    tipoBosqueData = []
    #tb = Habitat.objects.filter(seleccion=True).exclude(cod='4').exclude(cod__contains='.').order_by('nombre')
    tb = Habitat.objects.filter(cod__in=allHab.values_list('tipobosque_cod', flat=True)).filter(seleccion=True).exclude(cod='4').exclude(cod__contains='.').order_by('nombre')

    for t in tb:
        tipoBosqueData.append({'tipobosque_cod': t.cod, 'tipobosque_nombre': t.nombre})

    rodals_list = WebCompData.objects.all()

    ####### Selector Regió biogeográfica ########

    RegBio_list = WebCompDataValAmb.objects.filter(eje_cod='nm').distinct().values('regbio_cod', 'nombre_es')
    #RegBio_list = TeRegbio.objects.all()

    listaRegBio = []
    for regBio in RegBio_list:
        listaRegBio.append({
            'cod': regBio['regbio_cod'],
            'nombre': regBio['nombre_es']
        })

    #############################################


    ####### Selector Comunidad autonoma ########

    ComAuto_list = WebCompDataValAmb.objects.filter(eje_cod='nm').distinct().values('ccaa_nom', 'ccaa_nombre')
    #ComAuto_list = TeProvincia.objects.filter(nivel='Com. autònoma')

    listaComAuto = []
    for comAut in ComAuto_list:
        listaComAuto.append({
            'codigo': comAut['ccaa_nom'],
            'nombre': comAut['ccaa_nombre']
        })

    #############################################


    if id is not None:

        hab_cod = rodals_list.filter(id_rodal=id).values_list('habitat_cod', flat=True).first()
        #selector_rodals = rodals_list.filter(habitat_cod=hab_cod).filter(eje_cod='nm').exclude(id_rodal=id)
        selector_rodals = rodals_list.filter(eje_cod='nm').order_by('nombre')
        selector_rodals_comp = rodals_list.filter(rodalref=False).filter(eje_cod='nm').order_by('nombre')

        listaRodales = []
        for rodal in selector_rodals:
            listaRodales.append({
                'id_rodal': rodal.id_rodal,
                'nombre': rodal.nombre,
                'rodalref': rodal.rodalref

        })

        listaRodalesComp = []
        for rodalComp in selector_rodals_comp:
            listaRodalesComp.append({
                'id_rodal': rodalComp.id_rodal,
                'nombre': rodalComp.nombre,
                'rodalref': rodal.rodalref

            })



        dades_rodal = RodalValorres2.objects.filter(id_rodal=id)
        info_rodal = rodals_list.filter(id_rodal=id)

        rodalArbol = crearArbol(dades_rodal)

        ######## Valores info rodal ##############

        infoRodal = {}
        for punt in info_rodal:
            infoRodal = {
                'id_rodal': punt.id_rodal,
                'nombre': punt.nombre,
                'Comunidad_autonoma': punt.ccaa_nombre,
                'habitat_nom': punt.habitat_nom,
                'habitat_cod': punt.habitat_cod,
                'tipobosque_nombre': punt.tipobosque_nombre,
                'tipobosque_cod': punt.tipobosque_cod
            }

        #########################################



        valores_rodal_json = json.dumps(rodalArbol)

        context = {'herramientas': 'Herramienta de evaluación de rodales maduros',
                   'habitats': habitatData,
                   'valores_rodal': rodalArbol,
                   'infoRodal': infoRodal,
                   'listaRodales': listaRodales,
                   'listaRodalesComp': listaRodalesComp,
                   'valores_rodal_json': valores_rodal_json,
                   'listaRegBio': listaRegBio,
                   'listaComAuto': listaComAuto,
                   'tiposDeBosque': tipoBosqueData}

    else:

        #hab_cod = rodals_list.filter(id_rodal=id).values_list('habitat_cod', flat=True).first()
        #selector_rodals = rodals_list.filter(habitat_cod=hab_cod).filter(eje_cod='nm').exclude(id_rodal=id)
        selector_rodals = rodals_list.filter(eje_cod='nm').order_by('nombre')
        selector_rodals_comp = rodals_list.filter(eje_cod='nm').filter(rodalref=False).filter(eje_cod='nm').order_by('nombre')

        listaRodales = []
        for rodal in selector_rodals:
            listaRodales.append({
                'id_rodal': rodal.id_rodal,
                'nombre': rodal.nombre,
                'rodalref': rodal.rodalref

            })

        listaRodalesComp = []
        for rodal in selector_rodals_comp:
            listaRodalesComp.append({
                'id_rodal': rodal.id_rodal,
                'nombre': rodal.nombre,
                'rodalref': rodal.rodalref

            })

        context = {'herramientas': 'Herramienta de evaluación de rodales maduros',
                   'habitats': habitatData,
                   'valores_rodal': '',
                   'infoRodal': 'null',
                   'listaRodales': listaRodales,
                   'listaRodalesComp': listaRodalesComp,
                   'valores_rodal_json': 'null',
                   'listaRegBio': listaRegBio,
                   'listaComAuto': listaComAuto,
                   'tiposDeBosque': tipoBosqueData}



    return render(request, 'redbosques_main/comparador.html', context)




@api_view(['GET'])
def filtrosRodal(request, id=None):
    rodals_list = WebCompData.objects.all()

    info_rodal = rodals_list.filter(id_rodal=id)

    infoRodal = {}
    for punt in info_rodal:
        infoRodal = {
            'id_rodal': punt.id_rodal,
            'nombre': punt.nombre,
            'Comunidad_autonoma': punt.ccaa_nombre,
            'habitat_nom': punt.habitat_nom,
        }

    return render(request, 'redbosques_main/comparador.html', infoRodal)

@api_view(['GET'])
def valorRef(request):

    cordRod = request.query_params.get('vr', None)
    idHab = request.query_params.get('idHab', None)
    idComAut = request.query_params.get('comAut', None)
    idRegBiogeo = request.query_params.get('regBiogeo', None)
    rodRef = request.query_params.get('rodRef', None)

    if cordRod == None:
        context = {}


    #if test is not None:
    if cordRod != None:
        if cordRod != 'medRod':
            dades_rodal2 = RodalValorres2.objects.filter(id_rodal=cordRod)
            rodal_referencia = crearArbol(dades_rodal2)

            context = {'rodal_referencia': rodal_referencia}

        elif cordRod == 'medRod':

            if idHab == None and idComAut == None and idRegBiogeo == None:
                dades_rodal2 = RodalValorres2.objects.filter(rodalref=rodRef).values('indicador_cod').annotate(mitjana=Avg('valor'), stddev=StdDev('valor'))

            elif idHab == None and idComAut == None:
                dades_rodal2 = RodalValorres2.objects.filter(rodalref=rodRef).filter(regbio_cod=idRegBiogeo).values('indicador_cod').annotate(mitjana=Avg('valor'), stddev=StdDev('valor'))

            elif idHab == None and idRegBiogeo == None:
                dades_rodal2 = RodalValorres2.objects.filter(rodalref=rodRef).filter(comautonom_cod=idComAut).values('indicador_cod').annotate(mitjana=Avg('valor'), stddev=StdDev('valor'))

            elif idComAut == None and idRegBiogeo == None:

                dades_rodal2 = RodalValorres2.objects.filter(rodalref=rodRef).filter(lpeht_cod__startswith=idHab).filter(lpeht_cod__contains='.').values('indicador_cod').annotate(mitjana=Avg('valor'), stddev=StdDev('valor'))

            elif idHab == None:
                dades_rodal2 = RodalValorres2.objects.filter(rodalref=rodRef).filter(comautonom_cod=idComAut).filter(regbio_cod=idRegBiogeo).values('indicador_cod').annotate(mitjana=Avg('valor'), stddev=StdDev('valor'))

            elif idComAut == None:
                dades_rodal2 = RodalValorres2.objects.filter(rodalref=rodRef).filter(lpeht_cod__startswith=idHab).filter(lpeht_cod__contains='.').filter(regbio_cod=idRegBiogeo).values('indicador_cod').annotate(mitjana=Avg('valor'), stddev=StdDev('valor'))

            elif idRegBiogeo == None:
                dades_rodal2 = RodalValorres2.objects.filter(rodalref=rodRef).filter(lpeht_cod__startswith=idHab).filter(lpeht_cod__contains='.').filter(comautonom_cod=idComAut).values('indicador_cod').annotate(mitjana=Avg('valor'), stddev=StdDev('valor'))
            else:
                dades_rodal2 = RodalValorres2.objects.filter(rodalref=rodRef).filter(lpeht_cod__startswith=idHab).filter(lpeht_cod__contains='.').filter(comautonom_cod=idComAut).filter(regbio_cod=idRegBiogeo).values('indicador_cod').annotate(mitjana=Avg('valor'), stddev=StdDev('valor'))


            if not dades_rodal2:
                print(dades_rodal2)
                context = {'rodal_referencia': "No hay resultados"}
            else:
                rodal_referencia = crearArbolMedia(dades_rodal2)
                #rodal_referencia = crearArbol(dades_rodal2)
                context = {'rodal_referencia': rodal_referencia}


    return Response(context)


@api_view(['GET'])
def valorRodal(request):

    cordRod = request.query_params.get('vr', None)
    habSel = request.query_params.get('habSel', None)

    if cordRod == None:
        context = {}


    #if test is not None:
    if cordRod != None:
        if cordRod != 'medRod':
            dades_rodal2 = RodalValorres2.objects.filter(id_rodal=cordRod)
            rodal_referencia = crearArbol(dades_rodal2)
        if cordRod == 'medRod':
            #dades_rodal2 = RodalValorres2.objects.all()
            #rodals_list = RodalValorres2.objects.all()
            #hab_cod = rodals_list.filter(id_rodal=selRod).values_list('lpeht_cod', flat=True).first()

            dades_rodal2 = RodalValorres2.objects.filter(lpeht_cod=habSel).values('indicador_cod').annotate(mitjana=Avg('valor'),stddev=StdDev('valor'))
            rodal_referencia = crearArbolMedia(dades_rodal2)

        #rodal_referencia = crearArbol(dades_rodal2)
        context = {'rodal': rodal_referencia}

    return Response(context)


@api_view(['GET'])
def setFiltrosRodal(request):
    idRod = request.query_params.get('idR', None)
    regBio = request.query_params.get('rb', None)
    comAut = request.query_params.get('ca', None)

    select_rodals = []

    rodals_list = RodalValorres2.objects.all()
    hab_cod = rodals_list.filter(id_rodal=idRod).values_list('lpeht_cod', flat=True).first()

    if regBio is not None and comAut is not None:
        select_rodals = rodals_list.filter(lpeht_cod=hab_cod).filter(indicador_cod='nm').filter(regbio_cod=regBio).filter(comautonom_cod=comAut).exclude(id_rodal=idRod)

    elif regBio is not None:
        select_rodals = rodals_list.filter(lpeht_cod=hab_cod).filter(indicador_cod='nm').filter(regbio_cod=regBio).exclude(id_rodal=idRod)

    elif comAut is not None:
        select_rodals = rodals_list.filter(lpeht_cod=hab_cod).filter(indicador_cod='nm').filter(comautonom_cod=comAut).exclude(id_rodal=idRod)
    else:
        select_rodals = rodals_list.filter(lpeht_cod=hab_cod).filter(indicador_cod='nm').exclude(id_rodal=idRod)



    #listaRodales = {}
    rodAux = []

    for rodal in select_rodals:
        rodAux.append(rodal.id_rodal)
        #rodAux = WebMapa.objects.filter(id_rodal=rodal.id_rodal).filter(eje_cod='nm')

    rodales = {}
    listaRodales = []
    i=0

    for idList in rodAux:
        #rodales[i] = WebMapa.objects.filter(id_rodal=idList).filter(eje_cod='nm')
        rodales[i] = WebCompData.objects.get(id_rodal=idList,eje_cod='nm')
        #filter(id_rodal=idList).filter(eje_cod='nm')
        i = i+1


    for rodal in rodales:
        listaRodales.append({
            #'id_rodal': rodal.id_rodal,
            #'nombre': rodal.nombre
            'id_rodal': rodales[rodal].id_rodal,
            'nombre': rodales[rodal].nombre,
        })


    context = {'listaRodales': listaRodales}
    #return render(request, 'redbosques_main/comparador.html', context)
    return Response(context)



def crearArbol(dades):

    #######Asignación de los valores a las variables##########
        for valor2 in dades:
            if valor2.indicador_cod == 'nm':
                if valor2.valor == None:
                    nm_valor = "---"
                else:
                    nm_valor = round(valor2.valor, 2)

            if valor2.indicador_cod == 'cp':
                if valor2.valor == None:
                    cp_valor = "---"
                else:
                    cp_valor = round(valor2.valor, 2)

            if valor2.indicador_cod == 'ea':
                if valor2.valor == None:
                    ea_valor = "---"
                else:
                    ea_valor = round(valor2.valor)

            if valor2.indicador_cod == 'ce':
                if valor2.valor == None:
                    ce_valor = "---"
                else:
                    ce_valor = round(valor2.valor, 2)

            if valor2.indicador_cod == 'ab':
                if valor2.valor == None:
                    ab_valor = "---"
                else:
                    ab_valor = round(valor2.valor)

            if valor2.indicador_cod == 'ev':
                if valor2.valor == None:
                    ev_valor = "---"
                else:
                    ev_valor = round(valor2.valor)

            if valor2.indicador_cod == 'de':
                if valor2.valor == None:
                    de_valor = "---"
                else:
                    de_valor = round(valor2.valor)

            if valor2.indicador_cod == 'sn':
                if valor2.valor == None:
                    sn_valor = "---"
                else:
                    sn_valor = round(valor2.valor, 2)

            if valor2.indicador_cod == 'ae':
                if valor2.valor == None:
                    ae_valor = "---"
                else:
                    ae_valor = round(valor2.valor)

            if valor2.indicador_cod == 'mm':
                if valor2.valor == None:
                    mm_valor = "---"
                else:
                    mm_valor = round(valor2.valor)

            if valor2.indicador_cod == 'pm':
                if valor2.valor == None:
                    pm_valor = "---"
                else:
                    pm_valor = round(valor2.valor)

            if valor2.indicador_cod == 'hm':
                if valor2.valor == None:
                    hm_valor = "---"
                else:
                    hm_valor = round(valor2.valor, 2)

            if valor2.indicador_cod == 'mh':
                if valor2.valor == None:
                    mh_valor = "---"
                else:
                    mh_valor = round(valor2.valor)

            if valor2.indicador_cod == 'dn':
                if valor2.valor == None:
                    dn_valor = "---"
                else:
                    dn_valor = round(valor2.valor, 2)

            if valor2.indicador_cod == 'cs':
                if valor2.valor == None:
                    cs_valor = "---"
                else:
                    cs_valor = round(valor2.valor)

            if valor2.indicador_cod == 'hh':
                if valor2.valor == None:
                    hh_valor = "---"
                else:
                    hh_valor = round(valor2.valor, 2)

            if valor2.indicador_cod == 'ha':
                if valor2.valor == None:
                    ha_valor = "---"
                else:
                    ha_valor = round(valor2.valor, 2)

            if valor2.indicador_cod == 'tb':
                if valor2.valor == None:
                    tb_valor = "---"
                else:
                    tb_valor = round(valor2.valor)

            if valor2.indicador_cod == 'ua':
                if valor2.valor == None:
                    ua_valor = "---"
                else:
                    ua_valor = round(valor2.valor)

            if valor2.indicador_cod == 'fa':
                if valor2.valor == None:
                    fa_valor = "---"
                else:
                    fa_valor = round(valor2.valor)

            if valor2.indicador_cod == 'hr':
                if valor2.valor == None:
                    hr_valor = "---"
                else:
                    hr_valor = round(valor2.valor, 2)

            if valor2.indicador_cod == 'fr':
                if valor2.valor == None:
                    fr_valor = "---"
                else:
                    fr_valor = round(valor2.valor)

            if valor2.indicador_cod == 'ei':
                if valor2.valor == None:
                    ei_valor = "---"
                else:
                    ei_valor = round(valor2.valor)

            if valor2.indicador_cod == 'fg':
                if valor2.valor == None:
                    fg_valor = "---"
                else:
                    fg_valor = round(valor2.valor)

            if valor2.indicador_cod == 'cz':
                if valor2.valor == None:
                    cz_valor = "---"
                else:
                    cz_valor = round(valor2.valor)

            if valor2.indicador_cod == 'hb':
                if valor2.valor == None:
                    hb_valor = "---"
                else:
                    hb_valor = round(valor2.valor)

            if valor2.indicador_cod == 'fc':
                if valor2.valor == None:
                    fc_valor = "---"
                else:
                    fc_valor = round(valor2.valor)

            if valor2.indicador_cod == 'du':
                if valor2.valor == None:
                    du_valor = "---"
                else:
                    du_valor = round(valor2.valor)

            if valor2.indicador_cod == 'ie':
                if valor2.valor == None:
                    ie_valor = "---"
                else:
                    ie_valor = round(valor2.valor, 2)

            if valor2.indicador_cod == 'ar':
                if valor2.valor == None:
                    ar_valor = "---"
                else:
                    ar_valor = round(valor2.valor, 2)

            if valor2.indicador_cod == 'cf':
                if valor2.valor == None:
                    cf_valor = "---"
                else:
                    cf_valor = round(valor2.valor, 2)

            if valor2.indicador_cod == 'eb':
                if valor2.valor == None:
                    eb_valor = "---"
                else:
                    eb_valor = round(valor2.valor, 2)

            if valor2.indicador_cod == 'cn':
                if valor2.valor == None:
                    cn_valor = "---"
                else:
                    cn_valor = round(valor2.valor, 2)

    ######   Valores del rodal    #########
        rodal_referencia = {
            'naturalidad': {
                'valor': nm_valor,
                'composicion': {
                    'valor': cp_valor,
                    'especies_arboreas': {'valor': ea_valor}
                },
                'complejidad': {
                    'valor': ce_valor,
                    'area_basimetrica': {'valor': ab_valor},
                    'estratificacion_vertical': {'valor': ev_valor},
                    'diversidad_estructural': {'valor': de_valor}
                },
                'senectud': {
                    'valor': sn_valor,
                    'arb_tam_excep': {'valor': ae_valor},
                    'abund_mad_muerta': {'valor': mm_valor},
                    'prop_madera_muerta': {'valor': pm_valor}
                },
                'micro_habitats': {
                    'valor': hm_valor,
                    'mh_pies_vivos': {'valor': mh_valor}
                },
                'dinamica': {
                    'valor': dn_valor,
                    'ciclo_silvogen': {'valor': cs_valor}
                }
            },
            'huellaHumana': {
                'valor': hh_valor,
                'antigua': {
                    'valor': ha_valor,
                    'cont_temp': {'valor': tb_valor},
                    'usos_agropast': {'valor': ua_valor},
                    'usos_forestales': {'valor': fa_valor}
                },
                'reciente': {
                    'valor': hr_valor,
                    'usos_forestales': {'valor': fr_valor},
                    'especies_inv': {'valor': ei_valor},
                    'causa_fragment': {'valor': fg_valor},
                    'actv_cineget': {'valor': cz_valor},
                    'herv_rom': {'valor': hb_valor},
                    'frecuent': {'valor': fc_valor},
                    'durab_usos': {'valor': du_valor}
                },
            },
            'integridadEspacial': {
                'valor': ie_valor,
                'tamano': {'valor': ar_valor},
                'cont_forest': {'valor': cf_valor},
                'efect_borde': {'valor': eb_valor},
                'conect': {'valor': cn_valor}
            }
        }
        print(rodal_referencia)
        return rodal_referencia

def crearArbolMedia(dades):
    #print(dades)
    for indicador_cod in dades:
        #json1 = json.dumps(indicador_cod, ensure_ascii=False)
        #print(indicador_cod.keys(),'->', indicador_cod.values())
        #print(indicador_cod['indicador_cod'])
        #print(indicador_cod['mitjana'])
        #print(indicador_cod['stddev'])
        if indicador_cod['indicador_cod'] == 'nm':
            if indicador_cod['mitjana'] == None:
                nm_valor = "---"
            else:
                nm_valor = round(indicador_cod['mitjana'], 2)

            if indicador_cod['stddev'] == None:
                nm_valor_desv = "---"
            else:
                nm_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'cp':
            if indicador_cod['mitjana'] == None:
                cp_valor = "---"
            else:
                cp_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                cp_valor_desv = "---"
            else:
                cp_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'ea':
            if indicador_cod['mitjana'] == None:
                ea_valor = "---"
            else:
                ea_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                ea_valor_desv = "---"
            else:
                ea_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'ce':
            if indicador_cod['mitjana'] == None:
                ce_valor = "---"
            else:
                ce_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                ce_valor_desv = "---"
            else:
                ce_valor_desv = indicador_cod['stddev']



        if indicador_cod['indicador_cod'] == 'ab':
            if indicador_cod['mitjana'] == None:
                ab_valor = "---"
            else:
                ab_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                ab_valor_desv = "---"
            else:
                ab_valor_desv = indicador_cod['stddev']



        if indicador_cod['indicador_cod'] == 'ev':
            if indicador_cod['mitjana'] == None:
                ev_valor = "---"
            else:
                ev_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                ev_valor = "---"
            else:
                ev_valor_desv = indicador_cod['stddev']


        if indicador_cod['indicador_cod'] == 'de':
            if indicador_cod['mitjana'] == None:
                de_valor = "---"
            else:
                de_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                de_valor_desv = "---"
            else:
                de_valor_desv = indicador_cod['stddev']



        if indicador_cod['indicador_cod'] == 'sn':
            if indicador_cod['mitjana'] == None:
                sn_valor = "---"
            else:
                sn_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                sn_valor_desv = "---"
            else:
                sn_valor_desv = indicador_cod['stddev']



        if indicador_cod['indicador_cod'] == 'ae':
            if indicador_cod['mitjana'] == None:
                ae_valor = "---"
            else:
                ae_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                ae_valor_desv = "---"
            else:
                ae_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'mm':
            if indicador_cod['mitjana'] == None:
                mm_valor = "---"
            else:
                mm_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                mm_valor_desv = "---"
            else:
                mm_valor_desv = indicador_cod['stddev']


        if indicador_cod['indicador_cod'] == 'pm':
            if indicador_cod['mitjana'] == None:
                pm_valor = "---"
            else:
                pm_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                pm_valor_desv = "---"
            else:
                pm_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'hm':
            if indicador_cod['mitjana'] == None:
                hm_valor = "---"
            else:
                hm_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                hm_valor_desv = "---"
            else:
                hm_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'mh':
            if indicador_cod['mitjana'] == None:
                mh_valor = "---"
            else:
                mh_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                mh_valor_desv = "---"
            else:
                mh_valor_desv = indicador_cod['stddev']


        if indicador_cod['indicador_cod'] == 'dn':
            if indicador_cod['mitjana'] == None:
                dn_valor = "---"
            else:
                dn_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                dn_valor_desv = "---"
            else:
                dn_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'cs':
            if indicador_cod['mitjana'] == None:
                cs_valor = "---"
            else:
                cs_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                cs_valor_desv = "---"
            else:
                cs_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'hh':
            if indicador_cod['mitjana'] == None:
                hh_valor = "---"
            else:
                hh_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                hh_valor_desv = "---"
            else:
                hh_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'ha':
            if indicador_cod['mitjana'] == None:
                ha_valor = "---"
            else:
                ha_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                ha_valor_desv = "---"
            else:
                ha_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'tb':
            if indicador_cod['mitjana'] == None:
                tb_valor = "---"
            else:
                tb_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                tb_valor_desv = "---"
            else:
                tb_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'ua':
            if indicador_cod['mitjana'] == None:
                ua_valor = "---"
            else:
                ua_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                ua_valor_desv = "---"
            else:
                ua_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'fa':
            if indicador_cod['mitjana'] == None:
                fa_valor = "---"
            else:
                fa_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                fa_valor_desv = "---"
            else:
                fa_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'hr':
            if indicador_cod['mitjana'] == None:
                hr_valor = "---"
            else:
                hr_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                hr_valor_desv = "---"
            else:
                hr_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'fr':
            if indicador_cod['mitjana'] == None:
                fr_valor = "---"
            else:
                fr_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                fr_valor_desv = "---"
            else:
                fr_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'ei':
            if indicador_cod['mitjana'] == None:
                ei_valor = "---"
            else:
                ei_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                ei_valor_desv = "---"
            else:
                ei_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'fg':
            if indicador_cod['mitjana'] == None:
                fg_valor = "---"
            else:
                fg_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                fg_valor_desv = "---"
            else:
                fg_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'cz':
            if indicador_cod['mitjana'] == None:
                cz_valor = "---"
            else:
                cz_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                cz_valor_desv = "---"
            else:
                cz_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'hb':
            if indicador_cod['mitjana'] == None:
                hb_valor = "---"
            else:
                hb_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                hb_valor_desv = "---"
            else:
                hb_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'fc':
            if indicador_cod['mitjana'] == None:
                fc_valor = "---"
            else:
                fc_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                fc_valor_desv = "---"
            else:
                fc_valor_desv = indicador_cod['stddev']



        if indicador_cod['indicador_cod'] == 'du':
            if indicador_cod['mitjana'] == None:
                du_valor = "---"
            else:
                du_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                du_valor_desv = "---"
            else:
                du_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'ie':
            if indicador_cod['mitjana'] == None:
                ie_valor = "---"
            else:
                ie_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                ie_valor_desv = "---"
            else:
                ie_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'ar':
            if indicador_cod['mitjana'] == None:
                ar_valor = "---"
            else:
                ar_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                ar_valor_desv = "---"
            else:
                ar_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'cf':
            if indicador_cod['mitjana'] == None:
                cf_valor = "---"
            else:
                cf_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                cf_valor_desv = "---"
            else:
                cf_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'eb':
            if indicador_cod['mitjana'] == None:
                eb_valor = "---"
            else:
                eb_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                eb_valor_desv = "---"
            else:
                eb_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'cn':
            if indicador_cod['mitjana'] == None:
                cn_valor = "---"
            else:
                cn_valor = round(indicador_cod['mitjana'])

            if indicador_cod['stddev'] == None:
                cn_valor_desv = "---"
            else:
                cn_valor_desv = indicador_cod['stddev']

    ######   Valores del rodal    #########
    rodal_referencia = {
        'naturalidad': {
            'valor': nm_valor,
            'valor_desv': nm_valor_desv,
            'composicion': {
                'valor': cp_valor,
            'valor_desv': cp_valor_desv,
                'especies_arboreas': {'valor': ea_valor,
                                      'valor_desv': ea_valor_desv}
            },
            'complejidad': {
                'valor': ce_valor,
                'valor_desv': ce_valor_desv,
                'area_basimetrica': {'valor': ab_valor,
                                    'valor_desv': ab_valor_desv},
                'estratificacion_vertical': {'valor': ev_valor,
                                            'valor_desv': ev_valor_desv},
                'diversidad_estructural': {'valor': de_valor,
                                            'valor_desv': de_valor_desv}
            },
            'senectud': {
                'valor': sn_valor,
                'valor_desv': sn_valor_desv,
                'arb_tam_excep': {'valor': ae_valor,
                                'valor_desv': ae_valor_desv},
                'abund_mad_muerta': {'valor': mm_valor,
                                     'valor_desv': mm_valor_desv},
                'prop_madera_muerta': {'valor': pm_valor,
                                    'valor_desv': pm_valor_desv}
            },
            'micro_habitats': {
                'valor': hm_valor,
                'valor_desv': hm_valor_desv,
                'mh_pies_vivos': {'valor': mh_valor,
                                'valor_desv': mh_valor_desv}
            },
            'dinamica': {
                'valor': dn_valor,
                'valor_desv': dn_valor_desv,
                'ciclo_silvogen': {'valor': cs_valor,
                                'valor_desv': cs_valor_desv}
            }
        },
        'huellaHumana': {
            'valor': hh_valor,
            'valor_desv': hh_valor_desv,
            'antigua': {
                'valor': ha_valor,
                'valor_desv': ha_valor_desv,
                'cont_temp': {'valor': tb_valor,
                            'valor_desv': tb_valor_desv},
                'usos_agropast': {'valor': ua_valor,
                                'valor_desv': ua_valor_desv},
                'usos_forestales': {'valor': fa_valor,
                                    'valor_desv': fa_valor_desv}
            },
            'reciente': {
                'valor': hr_valor,
                'valor_desv': hr_valor_desv,
                'usos_forestales': {'valor': fr_valor,
                                    'valor_desv': fr_valor_desv},
                'especies_inv': {'valor': ei_valor,
                                'valor_desv': ei_valor_desv},
                'causa_fragment': {'valor': fg_valor,
                                    'valor_desv': fg_valor_desv},
                'actv_cineget': {'valor': cz_valor,
                                'valor_desv': cz_valor_desv},
                'herv_rom': {'valor': hb_valor,
                            'valor_desv': hb_valor_desv},
                'frecuent': {'valor': fc_valor,
                            'valor_desv': fc_valor_desv},
                'durab_usos': {'valor': du_valor,
                            'valor_desv': du_valor_desv}
            },
        },
        'integridadEspacial': {
            'valor': ie_valor,
            'valor_desv': ie_valor_desv,
            'tamano': {'valor': ar_valor,
                        'valor_desv': ar_valor_desv},
            'cont_forest': {'valor': cf_valor,
                            'valor_desv': cf_valor_desv},
            'efect_borde': {'valor': eb_valor,
                            'valor_desv': eb_valor_desv},
            'conect': {'valor': cn_valor,
                        'valor_desv': cn_valor_desv}
        }
    }

    return rodal_referencia


def login(request):

    login_form = LoginForm()

    if request.user.is_authenticated:
        return redirect('menu')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # correct username and password login the user
            auth.login(request, user)
            return redirect('menu')

        else:
            messages.error(request, 'Error wrong username/password')

    context = {'herramientas': 'Herramienta de evaluación de rodales maduros', 'login_form': login_form}
    return render(request, 'registration/login.html', context)


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST or None)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            # username = user_form.cleaned_data.get('email')
            user.set_password(user.password)
            user.save()
            return redirect('/redbosques')
    else:
        user_form = RegistrationForm()

    context = {'user_form': user_form}
    return render(request, 'registration/registration.html', context)


def rodalForm(request):
    if request.method == 'POST':
        form = rodalFormFields(request.POST or None)

        current_user = request.user
        user = User.objects.get(usuario=current_user)
        print(user)

        if form.is_valid():
            dades = form.save(commit=False)
            dades.usuario = user

            json_geometry = json.loads(request.POST["geometria_string"])
            multipoligon = []
            for feature in json_geometry['features']:
                feature_geometry = GEOSGeometry(json.dumps(feature['geometry']))
                feature_geometry.transform(25830)
                multipoligon.append(feature_geometry)

            mp = MultiPolygon(multipoligon)
            dades.geom = mp
            dades.save()

        #return HttpResponseRedirect('/redbosques/rodalForm2/' + str(dades.id) + '/')
        return redirect('rodalForm2', id=dades.id)


    else:
        form = rodalFormFields()
        context = {'form': form}

    return render(request, 'redbosques_main/rodalesForm.html', context)


def rodalForm2(request, id=None):

    if request.method == 'POST':
        #form = rodalFormFields2(request.POST or None)

        datos = get_object_or_404(Rodal, id=id)
        #current_user = request.user
        #user = User.objects.get(usuario=current_user)

        form = rodalFormFields2(request.POST, instance=datos)

        if form.is_valid():
            dades = form.save(commit=False)
            dades.save()

        return redirect('rodalForm3', id=dades.id)

    else:
        form = rodalFormFields2()

        datos = get_object_or_404(Rodal, pk=id)
        geom = datos.geom
        area = geom.area

        cursor = connection.cursor()

        ######## Continuidad mancha forestal #########

        contManchForestSQL = cursor.execute('select (stats).mean from '
                                            '( select st_summarystats(st_clip( rast, ST_GeomFromText(%s, 25830),true)) '
                                            'as stats from carto.bosque_cf '
                                            'WHERE ST_Intersects(rast, ST_GeomFromText(%s, 25830)) ) as foo',
                                            [geom.wkt, geom.wkt])

        contManchForest = cursor.fetchall()

        ##############################################

        ######## Densidad de bosque #########

        densBosqueSQL = cursor.execute('select (stats).mean from '
                                       '( select st_summarystats(st_clip( rast, ST_GeomFromText(%s, 25830),true)) '
                                       'as stats from carto.bosque_sf '
                                       'WHERE ST_Intersects(rast, ST_GeomFromText(%s, 25830)) ) as foo',
                                       [geom.wkt, geom.wkt])

        densBosque = cursor.fetchall()

        ##############################################

        ######## Distancia a la core área #########

        distCoreAreaSql = cursor.execute('select (stats).mean from '
                                         '( select st_summarystats(st_clip( rast, ST_GeomFromText(%s, 25830),true)) '
                                         'as stats from carto.bosque_ps '
                                         'WHERE ST_Intersects(rast, ST_GeomFromText(%s, 25830)) ) as foo',
                                         [geom.wkt, geom.wkt])

        distCoreArea = cursor.fetchall()
        ##############################################

        areaHectareas = round(area/10000, 2)
        contManchForestKM2 = round(contManchForest[1][0]/1000, 2)
        densBosquexcent = round(densBosque[0][0]/100, 2)
        distCoreAreaKM = round(distCoreArea[0][0]/1000, 2)

        print("Área: " + str(areaHectareas) + " ha")
        print("Continuidad mancha forestal: " + str(contManchForestKM2) + " km2")
        print("Densidad de bosque: " + str(densBosquexcent) + " %")
        print("Distancia a la core área: " + str(distCoreAreaKM) + " Km")

        context = {'herramientas': 'Herramienta de evaluación de rodales maduros',
                   'areaHectareas': areaHectareas,
                    'contManchForestKM2': contManchForestKM2,
                    'densBosquexcent': densBosquexcent,
                    'distCoreAreaKM': distCoreAreaKM,
                   'form': form,
                   'id': id}

        return render(request, 'redbosques_main/rodalesForm2.html', context)


def rodalForm3(request, id):

    if request.method == 'POST':
        #form = rodalFormFields3(request.POST or None)

        datos = get_object_or_404(Rodal, id=id)

        form = rodalFormFields3(request.POST, instance=datos)

        if form.is_valid():
            dades = form.save(commit=False)
            dades.save()

        return redirect('menu')

    else:
        form = rodalFormFields3()

        datos = get_object_or_404(Rodal, pk=id)

        context = {'herramientas': 'Herramienta de evaluación de rodales maduros', 'form': form, 'id': id}
        return render(request, 'redbosques_main/rodalesForm3.html', context)



######################## Filtres data table rodales ##################################

@api_view(['GET'])
def filtraxtipobosque(request):
    codiTipoBosque = request.query_params.get('idTipoBosque', None)
    rodalReferencia = request.query_params.get('rodRef', None)
    rodalesTable = WebCompDataValAmb.objects.all()


    if(codiTipoBosque == 'null'):
        codHab = rodalesTable.filter(eje_cod='nm').filter(rodalref=rodalReferencia or None).distinct().values('habitat_cod', 'tipobosque_nombre')
        comunAut = rodalesTable.filter(eje_cod='nm').filter(rodalref=rodalReferencia or None).distinct().values('ccaa_nom', 'ccaa_nombre')
        rbgeo = rodalesTable.filter(eje_cod='nm').filter(rodalref=rodalReferencia or None).distinct().values('regbio_cod', 'nombre_es')
        rod = rodalesTable.filter(eje_cod='nm').distinct().values('id_rodal', 'nombre', 'rodalref')
        rodComp = rodalesTable.filter(eje_cod='nm').filter(rodalref=rodalReferencia or None).distinct().values('id_rodal', 'nombre', 'rodalref')
    else:
        codHab = rodalesTable.filter(tipobosque_cod__startswith=codiTipoBosque).exclude(tipobosque_cod__contains='.').filter(eje_cod='nm').filter(rodalref=rodalReferencia or None).distinct().values('habitat_cod', 'tipobosque_nombre')
        comunAut = rodalesTable.filter(tipobosque_cod__startswith=codiTipoBosque).filter(habitat_cod__contains='.').filter(eje_cod='nm').filter(rodalref=rodalReferencia or None).distinct().values('ccaa_nom', 'ccaa_nombre')
        rbgeo = rodalesTable.filter(tipobosque_cod__startswith=codiTipoBosque).filter(habitat_cod__contains='.').filter(eje_cod='nm').filter(rodalref=rodalReferencia or None).distinct().values('regbio_cod', 'nombre_es')
        rod = rodalesTable.filter(tipobosque_cod__startswith=codiTipoBosque).filter(habitat_cod__contains='.').filter(eje_cod='nm').distinct().values('id_rodal', 'nombre', 'rodalref')
        rodComp = rodalesTable.filter(tipobosque_cod__startswith=codiTipoBosque).filter(habitat_cod__contains='.').filter(eje_cod='nm').filter(rodalref=rodalReferencia or None).distinct().values('id_rodal', 'nombre', 'rodalref')


    codigoHab = []
    for ch in codHab:
        codigoHab.append({
            'habitat_cod': ch['habitat_cod'],
            'tipobosque_nombre': ch['tipobosque_nombre'] #Noms canviats
        })

    comAut = []
    for c in comunAut:
        comAut.append({
            'ccaa_nom': c['ccaa_nom'],
            'ccaa_nombre': c['ccaa_nombre']
        })

    regBiogeo = []
    for r in rbgeo:
        regBiogeo.append({
            'regbio_cod': r['regbio_cod'],
            'nombre_es': r['nombre_es']
        })


    rodales = []
    for x in rod:
        rodales.append({
            'id_rodal': x['id_rodal'],
            'nombre': x['nombre'],
            'rodalref': x['rodalref']
        })

    rodalesComp = []
    for x in rodComp:
        rodalesComp.append({
            'id_rodal': x['id_rodal'],
            'nombre': x['nombre'],
            'rodalref': x['rodalref']
        })

    context = {'codigoHab': codigoHab,
                   'comAuto': comAut,
                   'regBiogeo': regBiogeo,
                   'rodales': rodales,
                   'rodalesComp': rodalesComp}

    return Response(context)

@api_view(['GET'])
def filtraxhabitat(request):
    codiHabitat = request.query_params.get('idHab', None)
    rodalReferencia = request.query_params.get('rodRef', None)
    rodalesTable = WebCompDataValAmb.objects.all()

    #print(rodalReferencia)

    if(codiHabitat == 'null'):
        comunAut = rodalesTable.filter(eje_cod='nm').filter(rodalref=rodalReferencia or None).distinct().values('ccaa_nom', 'ccaa_nombre')
        rbgeo = rodalesTable.filter(eje_cod='nm').filter(rodalref=rodalReferencia or None).distinct().values('regbio_cod', 'nombre_es')
        rod = rodalesTable.filter(eje_cod='nm').distinct().values('id_rodal', 'nombre', 'rodalref')
        rodComp = rodalesTable.filter(eje_cod='nm').filter(rodalref=rodalReferencia or None).distinct().values('id_rodal', 'nombre', 'rodalref')
    else:
        comunAut = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(eje_cod='nm').filter(rodalref=rodalReferencia or None).distinct().values('ccaa_nom', 'ccaa_nombre')

        rbgeo = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(eje_cod='nm').filter(rodalref=rodalReferencia or None).distinct().values('regbio_cod', 'nombre_es')

        rod = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(eje_cod='nm').distinct().values('id_rodal', 'nombre', 'rodalref')

        rodComp = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(eje_cod='nm').filter(rodalref=rodalReferencia or None).distinct().values('id_rodal', 'nombre', 'rodalref')

    comAut = []
    for c in comunAut:
        comAut.append({
            'ccaa_nom': c['ccaa_nom'],
            'ccaa_nombre': c['ccaa_nombre']
        })

    regBiogeo = []
    for r in rbgeo:
        regBiogeo.append({
            'regbio_cod': r['regbio_cod'],
            'nombre_es': r['nombre_es']
        })


    rodales = []
    for x in rod:
        rodales.append({
            'id_rodal': x['id_rodal'],
            'nombre': x['nombre'],
            'rodalref': x['rodalref']
        })

    rodalesComp = []
    for x in rodComp:
        rodalesComp.append({
            'id_rodal': x['id_rodal'],
            'nombre': x['nombre'],
            'rodalref': x['rodalref']
        })

    context = {'comAuto': comAut, 'regBiogeo': regBiogeo, 'rodales': rodales, 'rodalesComp': rodalesComp}
    return Response(context)


@api_view(['GET'])
def filtrarxComAut(request):
    codiHabitat = request.query_params.get('idHab', None)
    codiComaut = request.query_params.get('comAut', None)
    rodalReferencia = request.query_params.get('rodRef', None)

    #print(rodalReferencia)
    rodalesTable = WebCompDataValAmb.objects.all()

    if rodalReferencia == None:
        if codiHabitat == None:
            if codiComaut == 'null' or codiComaut == 'all':
                rbgeo = rodalesTable.filter(eje_cod='nm').distinct().values('regbio_cod','nombre_es')
                rod = rodalesTable.filter(eje_cod='nm').distinct().values('id_rodal','nombre', 'rodalref')
            else:
                rbgeo = rodalesTable.filter(ccaa_nom=codiComaut).filter(eje_cod='nm').distinct().values('regbio_cod', 'nombre_es')
                rod = rodalesTable.filter(ccaa_nom=codiComaut).filter(eje_cod='nm').distinct().values('id_rodal','nombre', 'rodalref')
        else:
            if codiComaut == 'null' or codiComaut == 'all':
                # comunAut = rodalesTable.filter(eje_cod='nm').distinct().values('ccaa_nom', 'ccaa_nombre')
                rbgeo = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(eje_cod='nm').distinct().values('regbio_cod','nombre_es')
                rod = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(eje_cod='nm').distinct().values('id_rodal','nombre', 'rodalref')
            else:
                rbgeo = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(ccaa_nom=codiComaut).filter(eje_cod='nm').distinct().values('regbio_cod', 'nombre_es')
                rod = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(ccaa_nom=codiComaut).filter(eje_cod='nm').distinct().values('id_rodal','nombre', 'rodalref')
    else:
        if codiHabitat == None:
            if codiComaut == 'null' or codiComaut == 'all':
                rbgeo = rodalesTable.filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('regbio_cod','nombre_es')
                rod = rodalesTable.filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
            else:
                rbgeo = rodalesTable.filter(ccaa_nom=codiComaut).filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('regbio_cod', 'nombre_es')
                rod = rodalesTable.filter(ccaa_nom=codiComaut).filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
        else:
            if codiComaut == 'null' or codiComaut == 'all':
                # comunAut = rodalesTable.filter(eje_cod='nm').distinct().values('ccaa_nom', 'ccaa_nombre')
                rbgeo = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('regbio_cod','nombre_es')
                rod = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
            else:
                rbgeo = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(ccaa_nom=codiComaut).filter(eje_cod='nm').filter(rodalref=rodalReferencia or None).distinct().values('regbio_cod', 'nombre_es')
                rod = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(ccaa_nom=codiComaut).filter(eje_cod='nm').filter(rodalref=rodalReferencia or None).distinct().values('id_rodal','nombre', 'rodalref')


    regBiogeo = []
    for r in rbgeo:
        regBiogeo.append({
            'regbio_cod': r['regbio_cod'],
            'nombre_es': r['nombre_es']
        })

    rodales = []
    for x in rod:
        rodales.append({
            'id_rodal': x['id_rodal'],
            'nombre': x['nombre'],
            'rodalref': x['rodalref']
        })

    context = {'regBiogeo': regBiogeo, 'rodales': rodales}

    return Response(context)



@api_view(['GET'])
def filtrarxRegBiogeo(request):
    codiHabitat = request.query_params.get('idHab', None)
    codiComaut = request.query_params.get('comAut', None)
    codiregBiogeo = request.query_params.get('regBiogeo', None)
    rodalReferencia = request.query_params.get('rodRef', None)

    rodalesTable = WebCompDataValAmb.objects.all()

    if rodalReferencia == None:
        if codiregBiogeo == 'null' or codiregBiogeo == 'all':
            if codiHabitat == None and codiComaut == None :
                rod = rodalesTable.filter(eje_cod='nm').distinct().values('id_rodal','nombre', 'rodalref')
            elif codiHabitat == None :
                rod = rodalesTable.filter(ccaa_nom=codiComaut).filter(eje_cod='nm').distinct().values('id_rodal','nombre', 'rodalref')
            elif codiComaut == None :
                rod = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(eje_cod='nm').distinct().values('id_rodal','nombre', 'rodalref')
            else:
                rod = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(ccaa_nom=codiComaut).filter(eje_cod='nm').distinct().values('id_rodal','nombre', 'rodalref')
        else:
            if codiHabitat == None and codiComaut == None :
                rod = rodalesTable.filter(regbio_cod=codiregBiogeo).filter(eje_cod='nm').distinct().values('id_rodal','nombre', 'rodalref')
            elif codiHabitat == None :
                rod = rodalesTable.filter(regbio_cod=codiregBiogeo).filter(ccaa_nom=codiComaut).filter(eje_cod='nm').distinct().values('id_rodal','nombre', 'rodalref')
            elif codiComaut == None :
                rod = rodalesTable.filter(regbio_cod=codiregBiogeo).filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(eje_cod='nm').distinct().values('id_rodal','nombre', 'rodalref')
            else:
                rod = rodalesTable.filter(regbio_cod=codiregBiogeo).filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(ccaa_nom=codiComaut).filter(eje_cod='nm').distinct().values('id_rodal','nombre', 'rodalref')

    else:
        if codiregBiogeo == 'null' or codiregBiogeo == 'all':
            if codiComaut == 'null' or codiComaut == 'all':
                if codiHabitat == None and codiComaut == None :
                    rod = rodalesTable.filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
                elif codiHabitat == None :
                    rod = rodalesTable.filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
                elif codiComaut == None :
                    rod = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
                else:
                    rod = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
            else:
                if codiHabitat == None and codiComaut == None :
                    rod = rodalesTable.filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
                elif codiHabitat == None :
                    rod = rodalesTable.filter(ccaa_nom=codiComaut).filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
                elif codiComaut == None :
                    rod = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
                else:
                    rod = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(ccaa_nom=codiComaut).filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
        else:
            if codiComaut == 'null' or codiComaut == 'all':
                if codiHabitat == None and codiComaut == None:
                    rod = rodalesTable.filter(regbio_cod=codiregBiogeo).filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
                elif codiHabitat == None:
                    rod = rodalesTable.filter(regbio_cod=codiregBiogeo).filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
                elif codiComaut == None:
                    rod = rodalesTable.filter(regbio_cod=codiregBiogeo).filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
                else:
                    rod = rodalesTable.filter(regbio_cod=codiregBiogeo).filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
            else:
                if codiHabitat == None and codiComaut == None:
                    rod = rodalesTable.filter(regbio_cod=codiregBiogeo).filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
                elif codiHabitat == None:
                    rod = rodalesTable.filter(regbio_cod=codiregBiogeo).filter(ccaa_nom=codiComaut).filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
                elif codiComaut == None:
                    rod = rodalesTable.filter(regbio_cod=codiregBiogeo).filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
                else:
                    rod = rodalesTable.filter(regbio_cod=codiregBiogeo).filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(ccaa_nom=codiComaut).filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')

    '''if codiregBiogeo == 'null':
        #comunAut = rodalesTable.filter(eje_cod='nm').distinct().values('ccaa_nom', 'ccaa_nombre')
        #rbgeo = rodalesTable.filter(eje_cod='nm').distinct().values('regbio_cod', 'nombre_es')
        rod = rodalesTable.filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal', 'nombre')'''

    rodales = []
    for x in rod:
        rodales.append({
            'id_rodal': x['id_rodal'],
            'nombre': x['nombre'],
            'rodalref': x['rodalref']

        })


    #context = {'regBiogeo': regBiogeo, 'rodales': rodales}
    context = {'rodales': rodales}
    return Response(context)

@api_view(['GET'])
def filtrarxRodRef(request):
    codiHabitat = request.query_params.get('idHab', None)
    codiComaut = request.query_params.get('comAut', None)
    codiregBiogeo = request.query_params.get('regBiogeo', None)
    rodalReferencia = request.query_params.get('rodRef', None)

    print(codiHabitat)
    print(codiComaut)
    print(codiregBiogeo)
    print(rodalReferencia)


    rodalesTable = WebCompDataValAmb.objects.all()

    if codiHabitat == None and codiComaut == None and codiregBiogeo == None :
        rod = rodalesTable.filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')

    elif codiHabitat == None and codiComaut == None :
        if codiregBiogeo == 'null' or codiregBiogeo == 'all':
            rod = rodalesTable.filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
        else:
            rod = rodalesTable.filter(regbio_cod=codiregBiogeo).filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')

    elif codiHabitat == None and codiregBiogeo == None :
        if codiComaut == 'null' or codiComaut == 'all':
            rod = rodalesTable.filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
        else:
            rod = rodalesTable.filter(ccaa_nom=codiComaut).filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')

    elif codiComaut == None and codiregBiogeo == None:

        rod = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')

    elif codiHabitat == None:
        '''if codiComaut == 'null' or codiComaut == 'all' or codiregBiogeo == 'null' or codiregBiogeo == 'all':
            rod = rodalesTable.filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal', 'nombre')
        el'''
        if codiregBiogeo == 'null' or codiregBiogeo == 'all':
            rod = rodalesTable.filter(eje_cod='nm').filter(ccaa_nom=codiComaut).filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
        elif codiComaut == 'null' or codiComaut == 'all':
            rod = rodalesTable.filter(eje_cod='nm').filter(regbio_cod=codiregBiogeo).filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
        else:
            rod = rodalesTable.filter(eje_cod='nm').filter(ccaa_nom=codiComaut).filter(regbio_cod=codiregBiogeo).filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')

    elif codiComaut == None:

        if codiregBiogeo == 'null' or codiregBiogeo == 'all':
            rod = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
        else:
            rod = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(eje_cod='nm').filter(regbio_cod=codiregBiogeo).filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')

    elif codiregBiogeo == None:
        if codiComaut == 'null' or codiComaut == 'all':
            rod = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
        else:
            rod = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(eje_cod='nm').filter(ccaa_nom=codiComaut).filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
    else:
        if codiComaut == 'null' or codiComaut == 'all' or codiregBiogeo == 'null' or codiregBiogeo == 'all':
            rod = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(eje_cod='nm').filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')
        else:
            rod = rodalesTable.filter(habitat_cod__startswith=codiHabitat).filter(habitat_cod__contains='.').filter(eje_cod='nm').filter(ccaa_nom=codiComaut).filter(regbio_cod=codiregBiogeo).filter(rodalref=rodalReferencia).distinct().values('id_rodal','nombre', 'rodalref')

    rodales = []
    for r in rod:
        rodales.append({
            'id_rodal': r['id_rodal'],
            'nombre': r['nombre'],
            'rodalref': r['rodalref']
        })


    #context = {'regBiogeo': regBiogeo, 'rodales': rodales}
    context = {'rodales': rodales}
    return Response(context)


'''@api_view(['POST'])
def rodalFormData(request):

    current_user = request.user
    user = User.objects.get(usuario=current_user)


    if request.method == 'POST':
        print('POST')
    else:
        print('No post')

    form = rodalFormFields(request.POST)

    if form.is_valid():
        dades = form.save(commit=False)
        dades.usuario = user

        json_geometry = json.loads(request.POST["geometria_string"])
        multipoligon = []
        for feature in json_geometry['features']:
            feature_geometry = GEOSGeometry(json.dumps(feature['geometry']))
            feature_geometry.transform(25830)
            multipoligon.append(feature_geometry)

        mp = MultiPolygon(multipoligon)
        dades.geom = mp
        dades.save()


            testJson = json.loads(request.POST["geometria_string"])

            print(testJson)
            testJson2 = testJson['features'][0]['geometry']


            fig = shape(testJson2)


            proj = partial(pyproj.transform, pyproj.Proj(init='epsg:4326'), pyproj.Proj(init='epsg:3857'))

            # Encontrado aquí https://gist.github.com/robinkraft/c6de2f988c9d3f01af3c
            # https://gist.github.com/drmalex07/5a54fc4f1db06a66679e
            fig_new = transform(proj, fig)
            area = fig_new.area

            cursor = connection.cursor()

            ######## Continuidad mancha forestal #########

            contManchForestSQL = cursor.execute('select (stats).mean from '
                '( select st_summarystats(st_clip( rast, ST_Transform(ST_GeomFromText(%s, 4326), 25830),true)) '
                'as stats from carto.bosque_cf '
                'WHERE ST_Intersects(rast, ST_Transform(ST_GeomFromText(%s, 4326), 25830)) ) as foo', [fig.wkt, fig.wkt])

            contManchForest = cursor.fetchall()

            print(contManchForest)
            #contManchForest = namedtuplefetchall(cursor)

            ##############################################


            ######## Densidad de bosque #########

            densBosqueSQL = cursor.execute('select (stats).mean from '
                '( select st_summarystats(st_clip( rast, ST_Transform(ST_GeomFromText(%s, 4326), 25830),true)) '
                'as stats from carto.bosque_sf '
                'WHERE ST_Intersects(rast, ST_Transform(ST_GeomFromText(%s, 4326), 25830)) ) as foo', [fig.wkt, fig.wkt])

            densBosque = cursor.fetchall()

            ##############################################


            ######## Distancia a la core área #########

            distCoreAreaSql = cursor.execute('select (stats).mean from '
                '( select st_summarystats(st_clip( rast, ST_Transform(ST_GeomFromText(%s, 4326), 25830),true)) '
                'as stats from carto.bosque_ps '
                'WHERE ST_Intersects(rast, ST_Transform(ST_GeomFromText(%s, 4326), 25830)) ) as foo', [fig.wkt, fig.wkt])

            distCoreArea = cursor.fetchall()
            ##############################################

            areaHectareas = round(area/10000, 2)
            contManchForestKM2 = round(contManchForest[1][0]/1000, 2)
            densBosquexcent = round(densBosque[0][0]/100, 2)
            distCoreAreaKM = round(distCoreArea[0][0]/1000, 2)

            print("Área: " + str(areaHectareas) + " ha")
            print("Continuidad mancha forestal: " + str(contManchForestKM2) + " km2")
            print("Densidad de bosque: " + str(densBosquexcent) + " %")
            print("Distancia a la core área: " + str(distCoreAreaKM) + " Km")

            context = {'areaHectareas': areaHectareas,
                     'contManchForestKM2': contManchForestKM2,
                     'densBosquexcent': densBosquexcent,
                     'distCoreAreaKM': distCoreAreaKM,
                     'idRodoal': id}


    return HttpResponseRedirect('/redbosques/rodalForm2/'+ str(dades.id) +'/')

'''

'''@api_view(['POST'])
def rodalFormData2(request, id):
    if request.method == 'POST':
        datos = get_object_or_404(Rodal, id=id)



        current_user = request.user
        user = User.objects.get(usuario=current_user)

        form = rodalFormFields2(request.POST, instance=datos)

        if form.is_valid():
            dades = form.save(commit=False)
            dades.save()
        print('POST')
    else:
        print('No post')

    data = 1

    return data
'''
