from django.shortcuts import render, redirect, get_object_or_404
from redbosques_main.models import WebMapa, Habitat, Rodal, RodalValorres2, TeRegbio, TeProvincia, RodalValoresAmbito, WebMapaValAmb, WebCompData, WebCompDataValAmb, TeHic, TeLpeht, Tesaurus, User, TeCategoria, FotosRodal, DocsRodal, Institucion, DatosUsuario
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.urls import reverse
from django.http import JsonResponse
from django.http import HttpResponse
import decimal
import json
from django.db.models import Avg, StdDev
from redbosques.settings_local import URL_BASE
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from redbosques.forms import RegistrationForm, LoginForm, rodalFormFields, rodalFormFields2, rodalFormFields3, rodalFormFields3Foto, rodalFormFields3Doc
from django.contrib import messages
from django.contrib import auth
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from osgeo import ogr


from django.contrib.auth import authenticate

import pyproj
from shapely.geometry import shape
from shapely.ops import transform
from functools import partial
import shapely.wkt
from django.db import DatabaseError, transaction
from django.db import connection
from collections import namedtuple
from django.http import HttpResponseRedirect
from django.http import Http404

import ntpath
import glob, os
import magic
import shapefile
import zipfile
from ajaxuploader.views import AjaxFileUploader
from redbosques.settings import *
from querystring_parser import parser
import functools
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import operator
from django.db.models import Q
from redbosques_main.serializers import DatosUsuarioSerializer
from django.contrib.auth.models import User as dUser
import copy
from django.template.loader import get_template
from django.core.mail import EmailMessage
from redbosques import settings


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
    current_user = request.user
    du = None
    try:
        du = DatosUsuario.objects.get(user=current_user)
    except DatosUsuario.DoesNotExist:
        pass

    #user = User.objects.get(usuario=current_user)


    rodalesSelector = []
    #rodals_list = WebMapa.objects.filter(eje_cod='nm').order_by('nombre')
    #rodals_list = Rodal.objects.filter(usuario=user).order_by('nombre')
    rodals_list = Rodal.objects.all().order_by('nombre')

    for r in rodals_list:
        #rodalesSelector.append({'id_rodal': r.id_rodal, 'nombre': r.nombre})
        rodalesSelector.append({'id_rodal': r.id, 'nombre': r.nombre})

    context = {'herramientas': 'Herramienta de evaluación de rodales maduros', 'rodalesSelector':rodalesSelector, 'du':du }
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


def comparador_new(request, id = None):
    init_params = {}
    if id is not None:
        valors_ini = WebMapaValAmb.objects.filter(id_rodal=id).distinct().values('habitat_cod','ccaa_nom','regbio_cod').first()

        if valors_ini is None:
            raise Http404("No hay datos de comparacion para el rodal seleccionado")

        # recuperar hàbitat inicial, ccaa inicial, regio inicial
        habitat_ini = valors_ini['habitat_cod']
        ccaa_ini = valors_ini['ccaa_nom']
        regbio_ini = valors_ini['regbio_cod']

        dades_ini = list(WebMapaValAmb.objects.filter(habitat_cod=habitat_ini).values())

        if len(dades_ini) > 0:
            cc_aa_ini_list = []
            reg_ini_list = []
            rodals_ini_list = []
            # carregar comunitats per hàbitat inicial

            already_in_there = set()
            for d in dades_ini:
                if not d['ccaa_nombre'] in already_in_there:
                    already_in_there.add(d['ccaa_nombre'])
                    cc_aa_ini_list.append({'codigo': d['ccaa_nom'], 'nombre_es': d['ccaa_nombre']})
            cc_aa_ini_list.sort(key=lambda x: x['nombre_es'])

            # carregar regio per comunitat autonoma
            already_in_there = set()
            for d in dades_ini:
                if not d['regbio_cod'] in already_in_there:
                    already_in_there.add(d['regbio_cod'])
                    reg_ini_list.append({'cod': d['regbio_cod'], 'nombre_es': d['nombre_es']})
            reg_ini_list.sort(key=lambda x: x['nombre_es'])

            # carregar rodals per regió i cc_aa
            already_in_there = set()
            for d in dades_ini:
                if not d['id_rodal'] in already_in_there and d['regbio_cod'] == regbio_ini and d['ccaa_nom'] == ccaa_ini:
                    already_in_there.add(d['id_rodal'])
                    if d['rodalref'] == True:
                        rodals_ini_list.append({ 'id_rodal': d['id_rodal'],'nombre': d['nombre'],'rodalref': 1 })
                    else:
                        rodals_ini_list.append({'id_rodal': d['id_rodal'], 'nombre': d['nombre'],'rodalref': 0 })
            rodals_ini_list.sort(key=lambda x: x['nombre'])

            init_params['rodal_ini'] = id
            init_params['habitat_ini']=habitat_ini
            init_params['ccaa_ini']=ccaa_ini
            init_params['regbio_ini'] = regbio_ini
            init_params['cc_aa_ini_list'] = cc_aa_ini_list
            init_params['reg_ini_list'] = reg_ini_list
            init_params['rodals_ini_list'] = rodals_ini_list

        else:
            raise Http404("No hay datos de comparacion para el rodal seleccionado")

    tb_in_data = WebMapaValAmb.objects.all().distinct().values('tipobosque_cod')
    hab_in_data = WebMapaValAmb.objects.all().distinct().values('habitat_cod')

    tb = Habitat.objects.filter(cod__in=tb_in_data).order_by('nombre')
    hb = Habitat.objects.filter(cod__in=hab_in_data).order_by('nombre')
    tipoBosqueData = []
    habitatData = []
    for t in tb:
        tipoBosqueData.append({'tipobosque_cod': t.cod, 'tipobosque_nombre': t.nombre})
    for h in hb:
        habitatData.append({'habitat_cod': h.cod, 'habitat_nombre': h.nombre})

    if not bool(init_params):
        context = {'tiposDeBosque': tipoBosqueData, 'habitats': habitatData }
    else:
        context = {'tiposDeBosque': tipoBosqueData, 'habitats': habitatData, 'init_params': init_params }

    return render(request, 'redbosques_main/comparador_new.html', context)


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
def valorref_ajax(request):

    cordRod = request.query_params.get('vr', None)
    idHab = request.query_params.get('idHab', None)
    idComAut = request.query_params.get('comAut', None)
    idRegBiogeo = request.query_params.get('regBiogeo', None)
    rodRef = request.query_params.get('rodRef', None)


    if cordRod is not None and cordRod != 'medRod':
        dades_rodal2 = RodalValorres2.objects.filter(id_rodal=cordRod)
        rodal_referencia = crearArbol(dades_rodal2)
        context = {'rodal_referencia': rodal_referencia}
    elif cordRod == 'medRod':
        dades_rodal2 = RodalValorres2.objects.all()
        if idRegBiogeo is not None and idRegBiogeo != 'all':
            dades_rodal2 = dades_rodal2.filter(regbio_cod=idRegBiogeo)
        if idComAut is not None and idComAut != 'all':
            dades_rodal2 = dades_rodal2.filter(comautonom_cod=idComAut)
        if idHab is not None:
            dades_rodal2 = dades_rodal2.filter(lpeht_cod__startswith=idHab)
        if rodRef is not None and rodRef == '1':
            dades_rodal2 = dades_rodal2.filter(rodalref=True)

        dades_rodal2 = dades_rodal2.values('indicador_cod').annotate(mitjana=Avg('valor'), stddev=StdDev('valor'))
        rodal_referencia = crearArbolMedia(dades_rodal2)
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
        #print(rodal_referencia)
        return rodal_referencia

def crearArbolMedia(dades):
    #print(dades)
    for indicador_cod in dades:
        #json1 = json.dumps(indicador_cod, ensure_ascii=False)
        #print(indicador_cod.keys(),'->', indicador_cod.values())
        #print(indicador_cod['indicador_cod'])
        #print(indicador_cod['mitjana'])
        #print(indicador_cod['stddev'])

        ev_valor_desv = None

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
            try:
                user = dUser.objects.get(username=username)
                if not user.is_active:
                    messages.error(request, 'Tu usuario está desactivado. Por favor, contacta con el responsable de tu institución')
                else:
                    messages.error(request, 'Nombre de usuario o password incorrectos, por favor vuelve a intentarlo')
            except dUser.DoesNotExist:
                messages.error(request, 'No existe un usuario con estas credenciales')

    context = {'herramientas': 'Herramienta de evaluación de rodales maduros', 'login_form': login_form}
    return render(request, 'registration/login.html', context)


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST or None)
        if user_form.is_valid():
            try:
                with transaction.atomic():
                    if request.POST['institucion'] == 'null':
                        raise Exception("La institucion es obligatoria, por favor seleccione una del desplegable")
                    id_inst = int(request.POST['institucion'])
                    institucion = Institucion.objects.get(pk=id_inst)
                    user = user_form.save(commit=False)
                    user.set_password(user.password)
                    user.is_active = False
                    user.save()
                    du = DatosUsuario()
                    du.user = user
                    du.institucion = institucion
                    du.save()
                    send_user_created_email(user.email)
                    return redirect('/redbosques')
            except Exception as e:
                messages.add_message(request,messages.ERROR, e)
                pass
    else:
        user_form = RegistrationForm()

    instituciones = Institucion.objects.all().order_by('nombre')
    context = {'user_form': user_form, 'instituciones': instituciones }
    return render(request, 'registration/registration.html', context)


@login_required(login_url="login/")
def editrodalForm(request, id=None):

    datos = get_object_or_404(Rodal, id=id)
    #form = rodalFormFields(instance=datos)




    if request.method == 'POST':
        form = rodalFormFields(request.POST or None, instance=datos)

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

            # return HttpResponseRedirect('/redbosques/rodalForm2/' + str(dades.id) + '/')
            return redirect('rodalForm2', id=dades.id)
    else:
        datos = get_object_or_404(Rodal, id=id)
        form = rodalFormFields(instance=datos)

        geom = datos.geom
        geom.transform(4326)
        g = ogr.CreateGeometryFromJson(geom.json)

        for idx, f in enumerate(g):
            geojson_string = f.ExportToJson()

        # print(geojson_string)

    context = {'form': form, 'geojson_string': geojson_string, 'id': id}
    return render(request, 'redbosques_main/editrodalForm.html', context)


@login_required(login_url="login/")
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





@login_required(login_url="login/")
def rodalForm2(request, id=None):

    datos = get_object_or_404(Rodal, id=id)
    geom = datos.geom
    area = geom.area

    categorias = TeCategoria.objects.all()

    val56 = categorias.filter(variable_rodal='valpropbosc56').order_by('categoria')
    valFrec = categorias.filter(variable_rodal='valfrecuent').order_by('categoria')
    valAgropastAnt = categorias.filter(variable_rodal='valagropasant').order_by('categoria')
    valCaza = categorias.filter(variable_rodal='valcaza').order_by('categoria')
    valDurab = categorias.filter(variable_rodal='valdurabusos').order_by('categoria')
    valEsp = categorias.filter(variable_rodal='valespinvas').order_by('categoria')
    valFor = categorias.filter(variable_rodal='valforestant').order_by('categoria')
    valForRec = categorias.filter(variable_rodal='valforestrec').order_by('categoria')
    valFrag = categorias.filter(variable_rodal='valfragment').order_by('categoria')
    valHerb = categorias.filter(variable_rodal='valforestrec').order_by('categoria')

    val56Array = []
    for v1 in val56:
        val56Array.append({'categoria': v1.categoria})

    valFrecArray = []
    for v2 in valFrec:
        valFrecArray.append({'categoria': v2.categoria})

    valAgropastAntArray = []
    for v3 in valAgropastAnt:
        valAgropastAntArray.append({'categoria': v3.categoria})

    valCazaArray = []
    for v4 in valCaza:
        valCazaArray.append({'categoria': v4.categoria})

    valDurabArray = []
    for v5 in valDurab:
        valDurabArray.append({'categoria': v5.categoria})

    valEspArray = []
    for v6 in valEsp:
        valEspArray.append({'categoria': v6.categoria})

    valForArray = []
    for v7 in valFor:
        valForArray.append({'categoria': v7.categoria})

    valForRecArray = []
    for v8 in valForRec:
        valForRecArray.append({'categoria': v8.categoria})

    valFragArray = []
    for v9 in valFrag:
        valFragArray.append({'categoria': v9.categoria})

    valHerbArray = []
    for v10 in valHerb:
        valHerbArray.append({'categoria': v10.categoria})

    cursor = connection.cursor()

    ######## Continuidad mancha forestal #########

    contManchForestSQL = cursor.execute('select (stats).mean from '
                                        '( select st_summarystats(st_clip( st_union(rast), ST_GeomFromText(%s, 25830),true)) '
                                        'as stats from carto.bosque_cf '
                                        'WHERE ST_Intersects(rast, ST_GeomFromText(%s, 25830)) ) as foo',
                                        [geom.wkt, geom.wkt])

    contManchForest = cursor.fetchall()

    ##############################################

    ######## Densidad de bosque #########

    densBosqueSQL = cursor.execute('select (stats).mean from '
                                   '( select st_summarystats(st_clip( st_union(rast), ST_GeomFromText(%s, 25830),true)) '
                                   'as stats from carto.bosque_sf '
                                   'WHERE ST_Intersects(rast, ST_GeomFromText(%s, 25830)) ) as foo',
                                   [geom.wkt, geom.wkt])

    densBosque = cursor.fetchall()

    ##############################################

    ######## Distancia a la core área #########

    distCoreAreaSql = cursor.execute('select (stats).mean from '
                                     '( select st_summarystats(st_clip( st_union(rast), ST_GeomFromText(%s, 25830),true)) '
                                     'as stats from carto.bosque_ps '
                                     'WHERE ST_Intersects(rast, ST_GeomFromText(%s, 25830)) ) as foo',
                                     [geom.wkt, geom.wkt])

    distCoreArea = cursor.fetchall()
    ##############################################

    areaHectareas = round(area / 10000, 2)
    contManchForestKM2 = round(contManchForest[0][0] / 1000, 2)
    densBosquexcent = round(densBosque[0][0] / 100, 2)
    distCoreAreaKM = round(distCoreArea[0][0] / 1000, 2)

    # print("Área: " + str(areaHectareas) + " ha")
    # print("Continuidad mancha forestal: " + str(contManchForestKM2) + " km2")
    # print("Densidad de bosque: " + str(densBosquexcent) + " %")
    # print("Distancia a la core área: " + str(distCoreAreaKM) + " Km")

    if request.method == 'POST':
        form = rodalFormFields2(request.POST or None, instance=datos)
        #form = rodalFormFields2(request.POST or None)
        #current_user = request.user
        #user = User.objects.get(usuario=current_user)

        #form = form.validate_numesparb()
        if form.is_valid():
            dades = form.save(commit=False)
            dades.save()
            return redirect('rodalForm3', id=id)

        '''
        else:
            url = reverse('rodalForm2', kwargs={'id': form.instance.id})
            return HttpResponseRedirect(url)
            #return render(request, 'redbosques_main/rodalesForm2.html',{'form' : form})
        '''

    else:
        #form = rodalFormFields2()
        #datos = get_object_or_404(Rodal, pk=id)
        form = rodalFormFields2(instance=datos)

    context = {'herramientas': 'Herramienta de evaluación de rodales maduros',
               'areaHectareas': areaHectareas,
               'contManchForestKM2': contManchForestKM2,
               'densBosquexcent': densBosquexcent,
               'distCoreAreaKM': distCoreAreaKM,
               'form': form,
               'id': id,
               'val56': val56Array,
               'valFrec': valFrecArray,
               'valAgropAnt': valAgropastAntArray,
               'valCaza': valCazaArray,
               'valDurab': valDurabArray,
               'valEsp': valEspArray,
               'valFor': valForArray,
               'valForRec': valForRecArray,
               'valFrag': valFragArray,
               'valHerb': valHerbArray
               }

    return render(request, 'redbosques_main/rodalesForm2.html', context)


@login_required(login_url="login/")
def rodalForm3(request, id):

    datos = get_object_or_404(Rodal, id=id)

    if request.method == 'POST':

        form = rodalFormFields3(request.POST, instance=datos)

        if form.is_valid():
            dades = form.save(commit=False)
            dades.save()

        return redirect('menu')
    else:
        id_rodal = id

        form = rodalFormFields3(instance=datos)

        allFotos = FotosRodal.objects.all()
        listaFotos = allFotos.filter(id_rodal=id_rodal)

        fotos = []
        for lf in listaFotos:
            fotos.append({
                'id_foto': lf.id_foto,
                'nombre_foto': lf.nombre_foto,
                'foto': lf.foto
            })

        allDocs = DocsRodal.objects.all()
        listaDocs = allDocs.filter(id_rodal=id_rodal)

        docs = []
        for ld in listaDocs:
            docs.append({
                'id_doc': ld.id_doc,
                'nombre_doc': ld.nombre_doc,
                'doc': ld.doc
            })

        context = {'listaFotos': fotos, 'id': id_rodal, 'listaDocs': docs, 'form': form}
        return render(request, 'redbosques_main/rodalesForm3.html', context)



'''@login_required(login_url="login/")
def rodalForm3(request, id):

    if request.method == 'POST':
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
        return render(request, 'redbosques_main/rodalesForm3.html', context)'''



@login_required(login_url="login/")
def uploadImage(request, id):

    if request.method == 'POST':

        form = rodalFormFields3Foto(request.POST, request.FILES)

        if form.is_valid():
            foto = form.save(commit=False)
            foto.id_rodal = Rodal.objects.get(id=id)
            foto.nombre_foto = foto.foto.name
            foto.save()
            data = {'is_valid': True, 'nombre_foto': foto.nombre_foto, 'url': foto.foto.url, 'id_foto': foto.id_foto}
        else:
            errorMessage = "La imagen supera el tamaño permitido (2MB)"
            data = {'is_valid': False, 'error_imagen': form.errors['foto']}
        return JsonResponse(data)
    else:
        id_rodal = id
        allFotos = FotosRodal.objects.all()
        listaFotos = allFotos.filter(id_rodal=id_rodal)

        fotos = []
        for lf in listaFotos:
            fotos.append({
                'id_foto': lf.id_foto,
                'nombre_foto': lf.nombre_foto,
                'foto': lf.foto
            })

        context = {'listaFotos': fotos, 'id': id_rodal}
        return render(request, 'redbosques_main/rodalesForm3.html', context)

@api_view(['POST'])
@login_required(login_url="login/")
def deleteImage(request, id):

    rd = FotosRodal.objects.filter(id_foto=id).values('id_rodal')

    rodalFotos = []
    for r in rd:
        id_rodal = r['id_rodal']
        '''rodalFotos.append({
            'id_rodal': 
        })'''

    #id_rodal = rodalFotos[0].id_rodal

    if request.method == 'POST':
        foto = FotosRodal.objects.get(id_foto=id)
        foto.delete()
    #return redirect('rodalForm3', id=id_rodal)

    context = {'id': id_rodal, 'imagen': 'imagen'}

    return Response(context)


@login_required(login_url="login/")
def uploadDocs(request, id):

    if request.method == 'POST':

        form = rodalFormFields3Doc(request.POST, request.FILES)

        if form.is_valid():
            doc = form.save(commit=False)
            doc.id_rodal = Rodal.objects.get(id=id)
            doc.nombre_doc = doc.doc.name
            doc.save()
            data = {'is_valid': True, 'nombre_doc': doc.nombre_doc, 'url': doc.doc.url, 'id_doc': doc.id_doc}
        else:
            data = {'is_valid': False, 'error_documento': form.errors['doc']}
        return JsonResponse(data)
    else:
        id_rodal = id
        allDocs = DocsRodal.objects.all()
        listaDocs = allDocs.filter(id_rodal=id_rodal)

        docs = []
        for ld in listaDocs:
            docs.append({
                'id_doc': ld.id_doc,
                'nombre_doc': ld.nombre_doc,
                'doc': ld.doc
            })

        context = {'listaFotos': docs, 'id': id_rodal}
        return render(request, 'redbosques_main/rodalesForm3.html', context)

@api_view(['POST'])
@login_required(login_url="login/")
def deleteDoc(request, id):

    rd = DocsRodal.objects.filter(id_doc=id).values('id_rodal')

    rodalFotos = []
    for d in rd:
        id_rodal = d['id_rodal']
        '''rodalFotos.append({
            'id_rodal': 
        })'''

    if request.method == 'POST':
        doc = DocsRodal.objects.get(id_doc=id)
        doc.delete()
    #return redirect('rodalForm3', id=id_rodal)

    context = {'id': id_rodal, 'docs': 'docs'}

    return Response(context)

######################## Filtres data table rodales ##################################

@api_view(['GET'])
def habitats_ajax(request):
    codiTb = request.query_params.get('tb', None)
    data = []
    if codiTb is not None:
        hab_in_data = WebMapaValAmb.objects.all().distinct().values('habitat_cod')
        if codiTb == 'null':
            hab = Habitat.objects.filter(cod__in=hab_in_data).order_by('nombre')
        else:
            hab = Habitat.objects.filter(cod__in=hab_in_data).filter(cod__contains= codiTb ).exclude(cod=codiTb).order_by('nombre')
        for h in hab:
            data.append( { 'habitat_cod': h.cod, 'habitat_nombre': h.nombre } )
    return Response(data)


@api_view(['GET'])
def ccaa_ajax(request):
    codiHab = request.query_params.get('hab', None)
    data = []
    if codiHab is not None:
        ccaa_in_data = WebMapaValAmb.objects.filter(habitat_cod=codiHab).distinct().values('ccaa_nom')
        ccaa = TeProvincia.objects.filter(codigo__in=ccaa_in_data).filter(nivel='Com. autònoma').order_by('nombre_es')
        for c in ccaa:
            data.append( { 'codigo': c.codigo, 'nombre_es': c.nombre_es } )
    return Response(data)

@api_view(['GET'])
def rodals_ajax(request):
    codiHabitat = request.query_params.get('idHab', None)
    codiComaut = request.query_params.get('comAut', None)
    codiregBiogeo = request.query_params.get('regBiogeo', None)
    rodalReferencia = request.query_params.get('rodRef', None)

    rodalesTable = WebCompDataValAmb.objects.all()

    if codiregBiogeo is not None and codiregBiogeo != 'all':
        rodalesTable = rodalesTable.filter(regbio_cod=codiregBiogeo).order_by('nombre')


    if codiComaut is not None and codiComaut != 'all':
        rodalesTable = rodalesTable.filter(ccaa_nom=codiComaut).order_by('nombre')

    if codiHabitat is not None:
        rodalesTable = rodalesTable.filter(habitat_cod=codiHabitat).order_by('nombre')

    if rodalReferencia is not None and rodalReferencia=='1':
        rodalesTable = rodalesTable.filter(rodalref=True).order_by('nombre')

    rodalesTable = rodalesTable.distinct().values('id_rodal','nombre','rodalref')

    rodales = []
    for r in rodalesTable:
        rodales.append({
            'id_rodal': r['id_rodal'],
            'nombre': r['nombre'],
            'rodalref': r['rodalref']
        })

    return Response(rodales)


@api_view(['GET'])
def regbiogeo_ajax(request):
    codiCa = request.query_params.get('ca', None)
    codiHab = request.query_params.get('hab', None)
    data = []
    regbio_in_data = WebMapaValAmb.objects.all()
    if codiCa is not None and codiCa != 'all':
        regbio_in_data = regbio_in_data.filter(ccaa_nom=codiCa)
    if codiHab is not None:
        regbio_in_data = regbio_in_data.filter(habitat_cod=codiHab)
    regbio_in_data = regbio_in_data.distinct().values('regbio_cod')
    regsbio = TeRegbio.objects.filter(cod__in=regbio_in_data).order_by('nombre_es')
        # hab = Habitat.objects.filter(cod__in=hab_in_data).order_by('nombre')
    for r in regsbio:
        data.append({'cod': r.cod, 'nombre_es': r.nombre_es})
    return Response(data)


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


import_uploader = AjaxFileUploader()


@api_view(['GET'])
def process_shapefile(request):
    if request.method == 'GET':
        path = request.query_params.get('path', None)
        if path is None:
            content = {'success': False, 'detail': 'Ruta de fichero incorrecta o fichero no encontrado'}
            return Response(data=content, status=400)
        else:
            filepath = BASE_DIR + path
            filename = ntpath.basename(os.path.splitext(filepath)[0])
            presumed_zipfile = magic.from_file(filepath)
            if not presumed_zipfile.lower().startswith('zip archive'):
                content = {'success': False, 'detail': 'No parece que el fichero sea un zip correcto. El fichero es de tipo ' + presumed_zipfile}
                return Response(data=content, status=400)
            else:
                # Extract file
                zip_ref = zipfile.ZipFile(filepath, 'r')
                zip_ref.extractall(BASE_DIR + "/media/uploads/" + filename)
                zip_ref.close()
                # Find and import shapefile
                os.chdir(BASE_DIR + "/media/uploads/" + filename)
                for file in glob.glob("*.shp"):
                    presumed_shapefile = magic.from_file(BASE_DIR + "/media/uploads/" + filename + "/" + file)
                    if presumed_shapefile.lower().startswith('esri shapefile'):
                        sf = shapefile.Reader(BASE_DIR + "/media/uploads/" + filename + "/" + file)
                        fields = sf.fields[1:]
                        field_names = [field[0] for field in fields]
                        buffer = []
                        for sr in sf.shapeRecords():
                            atr = dict(zip(field_names, sr.record))
                            geom = sr.shape.__geo_interface__
                            buffer.append(dict(type="Feature", geometry=geom, properties=atr))
                        geojson = json.dumps({"type": "FeatureCollection", "features": buffer})
                        content = {'success': True, 'detail': geojson}
                        return Response(data=content, status=200)
                    else:
                        content = {'success': False, 'detail': 'El fitxer shapefile té un format incorrecte'}
                        return Response(data=content, status=200)
                content = {'success': False,
                           'detail': 'No he trobat cap fitxer amb extensió *.shp dins del zip, no puc importar res.'}
                return Response(data=content, status=200)


@login_required(login_url="login/")
def user_admin(request):
    current_user = request.user
    try:
        du = DatosUsuario.objects.get(user=current_user)
        if du.admin_institucion:
            return render(request, 'redbosques_main/user_admin.html', {})
        else:
            return HttpResponse("Necesitas privilegios de administrador para acceder a esta página")
    except DatosUsuario.DoesNotExist:
        return HttpResponse("Necesitas privilegios de administrador para acceder a esta página")


def get_order_clause(params_dict, translation_dict=None):
    order_clause = []
    try:
        order = params_dict['order']
        if len(order) > 0:
            for key in order:
                sort_dict = order[key]
                column_index_str = sort_dict['column']
                if translation_dict:
                    column_name = translation_dict[params_dict['columns'][int(column_index_str)]['data']]
                else:
                    column_name = params_dict['columns'][int(column_index_str)]['data']
                direction = sort_dict['dir']
                if direction != 'asc':
                    order_clause.append('-' + column_name)
                else:
                    order_clause.append(column_name)
    except KeyError:
        pass
    return order_clause


def get_filter_clause(params_dict, fields, translation_dict=None):
    filter_clause = []
    try:
        q = params_dict['search']['value']
        if q != '':
            for field in fields:
                if translation_dict:
                    translated_field_name = translation_dict[field]
                    filter_clause.append( Q(**{translated_field_name+'__icontains':q}) )
                else:
                    filter_clause.append(Q(**{field + '__icontains': q}))
    except KeyError:
        pass
    return filter_clause

def generic_datatable_list_endpoint(request,search_field_list,queryset, classSerializer, field_translation_dict=None, order_translation_dict=None):
    draw = request.query_params.get('draw', -1)
    start = request.query_params.get('start', 0)
    #length = request.query_params.get('length', 25)
    length = 25

    get_dict = parser.parse(request.GET.urlencode())

    order_clause = get_order_clause(get_dict, order_translation_dict)

    filter_clause = get_filter_clause(get_dict, search_field_list, field_translation_dict)

    if len(filter_clause) == 0:
        queryset = queryset.order_by(*order_clause)
    else:
        queryset = queryset.order_by(*order_clause).filter(functools.reduce(operator.or_, filter_clause))

    paginator = Paginator(queryset, length)

    recordsTotal = queryset.count()
    recordsFiltered = recordsTotal
    page = int(start) / int(length) + 1

    serializer = classSerializer(paginator.page(page), many=True)
    return Response({'draw': draw, 'recordsTotal': recordsTotal, 'recordsFiltered': recordsFiltered, 'data': serializer.data})


@api_view(['GET'])
def revision_usuarios_datatable_list(request):
    if request.method == 'GET':
        current_user = request.user
        current_user_data = DatosUsuario.objects.get(user=current_user)
        institucion = current_user_data.institucion
        sort_translation_list = {'user.first_name': 'user__first_name', 'user.last_name': 'user__last_name', 'user.username': 'user__username', 'user.is_active': 'user__is_active', 'institucion.nombre': 'institucion__nombre' }
        field_translation_list = {'user.first_name': 'user__first_name', 'user.last_name': 'user__last_name', 'user.username': 'user__username', 'user.is_active': 'user__is_active', 'institucion.nombre': 'institucion__nombre' }
        search_field_list = ('user.first_name', 'user.last_name', 'user.username')
        queryset = DatosUsuario.objects.filter(institucion=institucion).exclude(user=current_user)
        response = generic_datatable_list_endpoint(request, search_field_list, queryset, DatosUsuarioSerializer, field_translation_list,sort_translation_list)
        return response


@api_view(['POST'])
def activate_user(request):
    if request.method == 'POST':
        current_user = request.user
        id = request.POST.get('id', None)
        value = request.POST.get('value', None)
        if id is None:
            content = {'status': 'KO', 'detail': 'mandatory param missing'}
            return Response(data=content, status=400)
        if value is None:
            content = {'status': 'KO', 'detail': 'mandatory param missing'}
            return Response(data=content, status=400)
        else:
            if value == 'true':
                b_val = True
            else:
                b_val = False
        try:
            user = dUser.objects.get(pk=int(id))
            user.is_active = b_val
            user.save()
            send_activated_email(user.email)
            content = {'status': 'OK', 'detail': 'all cool'}
            return Response(data=content, status=200)
        except User.DoesNotExist as e:
            content = {'status': 'KO', 'detail': 'user not found'}
            return Response(data=content, status=400)


def send_activated_email(email):
    send_to = [email]
    context = {
        'login_url': settings.APP_BASE_URL + reverse('redirect_from_root'),
        'email': email
    }
    plaintext = get_template('email_templates/activated_email_template.txt')
    text_content = plaintext.render(context)
    email = EmailMessage("Tu cuenta de RedBosques ha sido activada", text_content, to=send_to)
    email.send()


def send_user_created_email(email):
    send_to = [email]
    try:
        u = dUser.objects.get(email=email)
        du = DatosUsuario.objects.get(user=u)
        institucion = du.institucion
        capi = DatosUsuario.objects.filter(institucion=institucion).filter(admin_institucion=True)
        for capo in capi:
            send_to.append(capo.user.email)
        context = {
            'email': email,
            'institution': institucion.nombre
        }
        plaintext = get_template('email_templates/created_email_template.txt')
        text_content = plaintext.render(context)
        email = EmailMessage("Tu cuenta de RedBosques ha sido creada", text_content, to=send_to)
        email.send()
    except dUser.DoesNotExist:
        print("No se puede mandar el correo a " + email + ", no existe un usuario con este correo electrónico")



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
