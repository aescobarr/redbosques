from django.shortcuts import render, redirect, get_object_or_404
from redbosques_main.models import WebMapa, Habitat, Rodal, RodalValorres2, TeRegbio, TeProvincia, RodalValoresAmbito, \
    WebMapaValAmb, WebCompData, WebCompDataValAmb, TeHic, TeLpeht, Tesaurus, User, TeCategoria, FotosRodal, DocsRodal, \
    Institucion, DatosUsuario, AuthUser,TeMunicipi,TeIndicador, RodalProsp, WebMapaRodalProsp, DatosGeneralesRodal, \
    FotosRodalProsp, DocsRodalProsp, RodalProspDatosgen, RodalProspValores, Parcelaifn3Valorres, RodalValorres
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.urls import reverse
from django.http import JsonResponse
from django.http import HttpResponse
import decimal
import json
from django.db.models import Avg, StdDev, Max
from redbosques.settings_local import URL_BASE
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from redbosques.forms import RegistrationForm, LoginForm, rodalFormFields, rodalFormFields2, rodalFormFields3, \
    rodalFormFields3Foto, rodalFormFields3Doc, rodalFormFields3Fotoprincipal, rodalFormFase1Fields, \
    rodalFormFieldsFase1Foto, rodalFormFieldsFase1Doc
from django.contrib import messages
from django.contrib import auth
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Point
from osgeo import ogr
import tempfile


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
from django.core.mail import EmailMessage
from redbosques import settings
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string, get_template
from weasyprint import HTML, CSS
from django.db.models import Q
from json.decoder import JSONDecodeError
from django.contrib import messages
from django.db.models import Count
import numpy

import reportlab
import io
from reportlab.pdfgen import canvas
from django.core.files import File
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.template import RequestContext
from django.utils import translation
from django.utils.translation import gettext as _
import logging

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
    context = menuData(request)

    '''current_user = request.user
    du = None
    try:
        du = DatosUsuario.objects.get(user=current_user)
        print(du)
    except DatosUsuario.DoesNotExist:
        pass

    #user = User.objects.get(usuario=current_user)


    rodalesSelector = []
    #rodals_list = WebMapa.objects.filter(eje_cod='nm').order_by('nombre')
    #rodals_list = Rodal.objects.filter(usuario=user).order_by('nombre')

    rodals_list = Rodal.objects.all().order_by('nombre')

    for r in rodals_list:
        #rodalesSelector.append({'id_rodal': r.id_rodal, 'nombre': r.nombre})
        if r.usuario.id == du.id:
            rodalesSelector.append({'id_rodal': r.id , 'nombre': r.nombre + '(*)'})
        else:
            rodalesSelector.append({'id_rodal': r.id, 'nombre': r.nombre})


    rodalesSelectorEditor = []

    if du.admin_institucion:
        usDat = DatosUsuario.objects.filter(institucion_id=du.institucion_id).values('user_id')

        usuarios = AuthUser.objects.filter(id__in=usDat).values('id')
        rodals_list_2 = Rodal.objects.filter(usuario__in=usuarios).values('id', 'nombre').order_by('nombre')

        for test in rodals_list_2:
            rodalesSelectorEditor.append({'id_rodal': test['id'], 'nombre': test['nombre']})


    else:
        usDat = DatosUsuario.objects.filter(id=du.id).values('user_id')
        usuarios = AuthUser.objects.filter(id__in=usDat).values('id')
        rodals_list_2 = Rodal.objects.filter(usuario__in=usuarios).values('id', 'nombre').order_by('nombre')

        for test in rodals_list_2:
            rodalesSelectorEditor.append({'id_rodal': test['id'], 'nombre': test['nombre']})


    context = {'herramientas': 'Herramienta de evaluación de rodales maduros', 'rodalesSelector': rodalesSelector, 'du': du, 'rodalesSelectorEditor': rodalesSelectorEditor}'''
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


    context = {'herramientas': 'Herramienta de evaluación de rodales maduros',
               'habitatData': habitatData,
               'subHabitatData': subHabitatData,
               'rodalesData': rodalesData
               }

    return context


def initialDataFase1():
    # Carga de datos para el selector de Habitat
    habitatData=[]
    habData = Habitat.objects.filter(seleccion=True).exclude(cod='4').exclude(cod__contains='.').order_by('nombre')
    for h in habData:
        habitatData.append({'cod': h.cod, 'nombre': h.nombre})

    subHabitatDataProsp=[]
    hp = WebMapaRodalProsp.objects.all()

    shabProsp = hp.values_list('habitat_cod', flat=True)

    habpr = Habitat.objects.filter(cod__in=shabProsp.values_list('habitat_cod', flat=True)).order_by('nombre')

    for hprosp in habpr:
        subHabitatDataProsp.append({'cod': hprosp.cod, 'nombre': hprosp.nombre})


    rodalesProspData = []

    rodProsp = WebMapaRodalProsp.objects.all().order_by('nombre')

    for rd in rodProsp:
        rodalesProspData.append({'id_rodal': rd.id_rodal, 'nombre': rd.nombre})

    context = {'herramientas': 'Herramienta de evaluación de rodales maduros',
               'habitatData': habitatData,
               'subHabitatDataProsp': subHabitatDataProsp,
               'rodalesProspData': rodalesProspData}

    return context


#@login_required(login_url="login/")
def herramientas(request, id=None):

    if id is None:
        data = initialData()
        dataFase1 = initialDataFase1()
        context = {'initial_data': data, 'initial_data_fase1': dataFase1, 'coordenadas_rodal': 'null'}
    else:
        coordenadas_rodal = cordRodal(id)
        data = initialData()
        dataFase1 = initialDataFase1()
        context = {'initial_data': data, 'initial_data_fase1': dataFase1,'coordenadas_rodal': coordenadas_rodal}

    return render(request, 'redbosques_main/herramientas.html', context)


def cordRodal(id):

    rodal = WebMapaValAmb.objects.filter(id_rodal=id).filter(eje_cod='nm')
    coordenadas_rodal = []
    for punt in rodal:
        coordenadas_rodal.append({
            'id_rodal': punt.id_rodal,
            'x': punt.geom.x,
            'y': punt.geom.y,
            'nombre': punt.nombre,
            'test': punt.foto
        })

    return coordenadas_rodal


@api_view(['GET'])
def dataCleaner(request):
    fase = request.query_params.get('f', None)

    if fase == 'fase2':
        resultado = initialData()
    elif fase == 'fase1':
        resultado = initialDataFase1()
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
            'imagen': r.foto,
            'valor_hh': r.hh,
            'valor_ie': r.ie,
            'valor_nm': r.nm,
            'regionBiogeo': r.nombre_es
        })

    context = {'newSubHabitatData': newSubHabitatData, 'newRodalesData': newRodalesData}
    return Response(context)


@api_view(['GET'])
def habitatDataProsp(request):
    codiHabitat = request.query_params.get('ch', None)
    newSubHabitatData = []
    newRodalesData = []

    allSub = WebMapaRodalProsp.objects.all()
    allSub2 = allSub.all().values_list('habitat_cod', flat=True)

    subHabExist = Habitat.objects.filter(cod__in=allSub2.values_list('habitat_cod', flat=True))

    if codiHabitat == 'null':
        subHabExistFilter = subHabExist.filter(cod__contains='.').order_by('nombre')
        rodales = WebMapaRodalProsp.objects.all().order_by('nombre')
    else:
        subHabExistFilter = subHabExist.filter(cod__startswith=codiHabitat).filter(cod__contains='.').order_by('nombre')
        rodales = WebMapaRodalProsp.objects.filter(habitat_cod__startswith=codiHabitat).order_by('nombre')

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
            'tipodebosque': r.tipobosque,
            'valor': r.volarrodal,
            'foto': r.foto
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
            'imagen': r.foto,
            'valor_hh': r.hh,
            'valor_ie': r.ie,
            'valor_nm': r.nm,
            'regionBiogeo': r.nombre_es
        })

    context = {'newRodalesData2': newRodalesData2}
    return Response(context)


@api_view(['GET'])
def subHabitatDataProsp(request):
    codiSubhabitat = request.query_params.get('csh', None)
    newRodalesData2 = []

    if codiSubhabitat == 'null':
        rodales = WebMapaRodalProsp.objects.all().order_by('nombre')
    else:
        rodales = WebMapaRodalProsp.objects.filter(habitat_cod__startswith=codiSubhabitat).order_by('nombre')


    for r in rodales:
        newRodalesData2.append({
            'id_rodal':r.id_rodal,
            'x':r.geom.x,
            'y':r.geom.y,
            'nombre': r.nombre,
            'Comunidad_autonoma': r.ccaa_nombre,
            'habitat_nom': r.habitat_nom,
            'tipodebosque': r.tipobosque,
            'valor': r.volarrodal,
            'foto': r.foto
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
            'imagen': r.foto,
            'valor_hh': r.hh,
            'valor_ie': r.ie,
            'valor_nm': r.nm,
            'regionBiogeo': r.nombre_es
        })

    context = {'rodalData': rodalData}
    return Response(context)


@api_view(['GET'])
def rodalDataProsp(request):
    codiRodal = request.query_params.get('cr', None)
    rodalData = []

    if codiRodal == 'null':
        rod = WebMapaRodalProsp.objects.all().order_by('nombre')
    else:
        rod = WebMapaRodalProsp.objects.filter(id_rodal=codiRodal).order_by('nombre')

    for r in rod:
        rodalData.append({
            'id_rodal':r.id_rodal,
            'x':r.geom.x,
            'y':r.geom.y,
            'nombre': r.nombre,
            'Comunidad_autonoma': r.ccaa_nombre,
            'habitat_nom': r.habitat_nom,
            'tipodebosque': r.tipobosque,
            'valor': r.volarrodal,
            'foto': r.foto
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

    #fotosSelected = FotosRodal.objects.filter(fotoprincipal=True)



    llista_punts = []
    for punt in dades_punts:
        llista_punts.append({
                    'id_rodal': punt.id_rodal,
                    'x': punt.geom.x,
                    'y': punt.geom.y,
                    'nombre': punt.nombre,
                    'Comunidad_autonoma': punt.ccaa_nombre,
                    'habitat_nom': punt.habitat_nom,
                    'tipobosque_nombre': punt.tipobosque_nombre,
                    'valor': punt.valor,
                    'imagen': punt.foto,
                    'valor_hh': punt.hh,
                    'valor_ie': punt.ie,
                    'valor_nm': punt.nm,
                    'regionBiogeo': punt.nombre_es
                })

    rodalesFase1 = []
    rod = WebMapaRodalProsp.objects.all()


    for t in rod:
        rodalesFase1.append({
            'id_rodal': t.id_rodal,
            'x': t.geom.x,
            'y': t.geom.y,
            'nombre': t.nombre,
            'Comunidad_autonoma': t.ccaa_nombre,
            'habitat_nom': t.habitat_nom,
            'tipodebosque': t.tipobosque,
            'valor': t.volarrodal,
            'foto': t.foto
        })

    #print(rodalesFase1)

    context = {'llista_punts': llista_punts, 'llista_habitats': llista_habitats, 'llista_punts_RodalsProsp': rodalesFase1}
    return Response(context)


def comparador_new(request, id=None):
    init_params = {}
    if id is not None:
        valors_ini = WebMapaValAmb.objects.filter(id_rodal=id).distinct().values('habitat_cod','ccaa_nom','regbio_cod').first()

        if valors_ini is None:
            raise Http404("No hay datos de comparacion para el rodal seleccionado")

        # recuperar hàbitat inicial, ccaa inicial, regio inicial
        habitat_ini = valors_ini['habitat_cod']
        #ccaa_ini = valors_ini['ccaa_nom']
        #regbio_ini = valors_ini['regbio_cod']

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
                if not d['id_rodal'] in already_in_there:
                    already_in_there.add(d['id_rodal'])
                    if d['rodalref'] == True:
                        rodals_ini_list.append({ 'id_rodal': d['id_rodal'],'nombre': d['nombre'],'rodalref': 1 })
                    else:
                        rodals_ini_list.append({'id_rodal': d['id_rodal'], 'nombre': d['nombre'],'rodalref': 0 })
            rodals_ini_list.sort(key=lambda x: x['nombre'])

            init_params['rodal_ini'] = id
            init_params['habitat_ini']=habitat_ini
            #init_params['ccaa_ini']=ccaa_ini
            #init_params['regbio_ini'] = regbio_ini
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
    rodPrincip = request.query_params.get('rodPrincip', None)



    if cordRod is not None and cordRod != 'medRod':
        if rodPrincip is not None:
            dades_rodal = RodalValorres2.objects.filter(id_rodal=cordRod).exclude(id_rodal=rodPrincip)
        else:
            dades_rodal = RodalValorres2.objects.filter(id_rodal=cordRod)

        rodal_referencia = crearArbol(dades_rodal)
        rodalNombre = Rodal.objects.filter(id=cordRod).values('id', 'nombre')

        dadesGraficosPuntos = RodalValorres2.objects.filter(id_rodal=cordRod).filter(nivel='eje').values('id_rodal', 'indicador_cod', 'valor')

        idRodales = []
        for infRod in dadesGraficosPuntos:
            if infRod['id_rodal'] not in idRodales:
                idRodales.append(infRod['id_rodal'])

        infoRodal = Rodal.objects.filter(id__in=idRodales).values('id','nombre')


        rodalRefValNom = []
        rodalRefValNom.append(rodal_referencia)
        rodalRefValNom.append(infoRodal)

        rodal_graficos_puntos = datosGraficasPuntos(dadesGraficosPuntos, infoRodal)

        #dadesGraficoBarrasCrite = RodalValorres2.objects.filter(id_rodal=cordRod).filter(nivel='crite').values('id_rodal', 'indicador_cod', 'valor')
        dadesGraficoBarras = RodalValorres2.objects.filter(id_rodal=cordRod).filter(Q(nivel='crite') | Q(nivel='eje')).values('id_rodal', 'indicador_cod', 'valor')



        idRodalesBarCrite = []
        for infRod in dadesGraficoBarras:
            if infRod['id_rodal'] not in idRodalesBarCrite:
                idRodalesBarCrite.append(infRod['id_rodal'])

        infoRodalBarCrite = Rodal.objects.filter(id__in=idRodalesBarCrite).values('id', 'nombre')
        rodal_graficos_barras = datosGraficasPuntos(dadesGraficoBarras, infoRodalBarCrite)

        context = {'rodal_referencia': rodal_referencia, 'rodalNombre': rodalNombre, 'rodalRefGraficos': rodalRefValNom, 'rodalRefGraficoPuntos': rodal_graficos_puntos, 'rodalRefChart' : rodal_graficos_barras, 'infoRodal': infoRodal}

    elif cordRod == 'medRod':

        dades_rodal2 = RodalValorres2.objects.all()

        if rodRef is not None and rodRef == 'True':
            dades_rodal2 = dades_rodal2.filter(rodalref=True)
            if idRegBiogeo is not None and idRegBiogeo != 'all':
                dades_rodal2 = dades_rodal2.filter(regbio_cod=idRegBiogeo)
            if idComAut is not None and idComAut != 'all':
                dades_rodal2 = dades_rodal2.filter(comautonom_cod=idComAut)
            if idHab is not None:
                dades_rodal2 = dades_rodal2.filter(lpeht_cod__startswith=idHab)
            #if rodRef is not None and rodRef == '1':
                #dades_rodal2 = dades_rodal2.filter(rodalref=True)
            if rodPrincip is not None:
                dades_rodal2 = dades_rodal2.exclude(id_rodal=rodPrincip)
        elif rodRef is None and rodRef == 'False':
            dades_rodal2 = dades_rodal2.filter(rodalref=False)

            if idRegBiogeo is not None and idRegBiogeo != 'all':
                dades_rodal2 = dades_rodal2.filter(regbio_cod=idRegBiogeo)
            if idComAut is not None and idComAut != 'all':
                dades_rodal2 = dades_rodal2.filter(comautonom_cod=idComAut)
            if idHab is not None:
                dades_rodal2 = dades_rodal2.filter(lpeht_cod__startswith=idHab)
            #if rodRef is not None and rodRef == '1':
                #dades_rodal2 = dades_rodal2.filter(rodalref=True)
            if rodPrincip is not None:
                dades_rodal2 = dades_rodal2.exclude(id_rodal=rodPrincip)

        rodalNombre = [{'nombre': 'Todos los rodales'}]
        dades_rodal = dades_rodal2.values('indicador_cod').annotate(mitjana=Avg('valor'), stddev=StdDev('valor'))
        print(dades_rodal)
        rodal_referencia = crearArbolMedia(dades_rodal)

        ### Grafica puntos
        dadesGraficosPuntos = dades_rodal2.filter(nivel='eje').values('id_rodal', 'indicador_cod', 'valor')

        idRodales = []
        for infRod in dadesGraficosPuntos:
            if infRod['id_rodal'] not in idRodales:
                idRodales.append(infRod['id_rodal'])

        infoRodal = Rodal.objects.filter(id__in=idRodales).values('id', 'nombre').order_by('id')

        rodalRefValNom = []
        rodalRefValNom.append(rodal_referencia)
        rodalRefValNom.append(infoRodal)


        rodal_graficos_puntos = datosGraficasPuntos(dadesGraficosPuntos, infoRodal)

        #dadesGraficoBarrasCrite = RodalValorres2.objects.filter(lpeht_cod=idHab).filter(nivel='crite').exclude(id_rodal=rodPrincip).values('id_rodal', 'indicador_cod', 'valor')
        dadesGraficoBarras = RodalValorres2.objects.filter(lpeht_cod=idHab).filter(Q(nivel='crite') | Q(nivel='eje')).exclude(id_rodal=rodPrincip).values('id_rodal', 'indicador_cod', 'valor')


        idRodalesBarCrite = []
        for infRod in dadesGraficoBarras:
            if infRod['id_rodal'] not in idRodalesBarCrite:
                idRodalesBarCrite.append(infRod['id_rodal'])

        infoRodalBarCrite = Rodal.objects.filter(id__in=idRodalesBarCrite).values('id', 'nombre').exclude(id=rodPrincip)
        rodal_graficos_barras = datosGraficasPuntos(dadesGraficoBarras, infoRodalBarCrite)



        context = {'rodal_referencia': rodal_referencia, 'rodalNombre': rodalNombre, 'rodalRefGraficos': rodalRefValNom, 'rodalRefGraficoPuntos': rodal_graficos_puntos, 'rodalRefChart': rodal_graficos_barras}


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
            rodalNombre = Rodal.objects.filter(id=cordRod).values('id', 'nombre')

            dadesGraficosPuntos = RodalValorres2.objects.filter(id_rodal=cordRod).filter(nivel='eje').values('id_rodal', 'indicador_cod', 'valor')

            idRodales = []
            for infRod in dadesGraficosPuntos:
                if infRod['id_rodal'] not in idRodales:
                    idRodales.append(infRod['id_rodal'])

            infoRodal = Rodal.objects.filter(id__in=idRodales).values('id', 'nombre')

            rodalValNom = []
            rodalValNom.append(rodal_referencia)
            rodalValNom.append(infoRodal)


            rodal_graficos_puntos = datosGraficasPuntos(dadesGraficosPuntos, infoRodal)

            #dadesGraficoBarrasCrite = RodalValorres2.objects.filter(id_rodal=cordRod).filter(nivel='crite').values('id_rodal', 'indicador_cod', 'valor')
            dadesGraficoBarras = RodalValorres2.objects.filter(id_rodal=cordRod).filter(Q(nivel='crite') | Q(nivel='eje')).values('id_rodal', 'indicador_cod', 'valor')


            idRodalesBarCrite = []
            for infRod in dadesGraficoBarras:
                if infRod['id_rodal'] not in idRodalesBarCrite:
                    idRodalesBarCrite.append(infRod['id_rodal'])

            infoRodalBarCrite = Rodal.objects.filter(id__in=idRodalesBarCrite).values('id', 'nombre')

            #rodal_graficos_barras = datosGraficasBarras(dadesGraficoBarrasCrite, infoRodalBarCrite)
            rodal_graficos_barras = datosGraficasPuntos(dadesGraficoBarras, infoRodalBarCrite)

        if cordRod == 'medRod':
            #dades_rodal2 = RodalValorres2.objects.all()
            #rodals_list = RodalValorres2.objects.all()
            #hab_cod = rodals_list.filter(id_rodal=selRod).values_list('lpeht_cod', flat=True).first()

            dades_rodal2 = RodalValorres2.objects.filter(lpeht_cod=habSel).values('indicador_cod').annotate(mitjana=Avg('valor'),stddev=StdDev('valor'))
            rodal_referencia = crearArbolMedia(dades_rodal2)
            rodalNombre = [{'nombre': 'Todos los rodales'}]

            dadesGraficosPuntos = RodalValorres2.objects.filter(lpeht_cod=habSel).filter(nivel='eje').values('id_rodal', 'indicador_cod', 'valor')

            idRodales = []
            for infRod in dadesGraficosPuntos:
                if infRod['id_rodal'] not in idRodales:
                    idRodales.append(infRod['id_rodal'])

            infoRodal = Rodal.objects.filter(id__in=idRodales).values('id', 'nombre')

            rodalValNom = []
            rodalValNom.append(rodal_referencia)
            rodalValNom.append(infoRodal)

            rodal_graficos_puntos = datosGraficasPuntos(dadesGraficosPuntos, infoRodal)



            dadesGraficoBarras = RodalValorres2.objects.filter(lpeht_cod=habSel).filter(Q(nivel='crite') | Q(nivel='eje')).values('id_rodal', 'indicador_cod', 'valor')
            #dadesGraficoBarrasCrite = RodalValorres2.objects.filter(lpeht_cod=habSel).filter(nivel='crite').values('id_rodal', 'indicador_cod', 'valor')


            idRodalesBarCrite = []
            for infRod in dadesGraficoBarras:
                if infRod['id_rodal'] not in idRodalesBarCrite:
                    idRodalesBarCrite.append(infRod['id_rodal'])

            infoRodalBarCrite = Rodal.objects.filter(id__in=idRodalesBarCrite).values('id', 'nombre')
            #rodal_graficos_barras = datosGraficasBarras(dadesGraficoBarrasCrite)
            rodal_graficos_barras = datosGraficasPuntos(dadesGraficoBarras, infoRodalBarCrite)

            print(rodal_graficos_barras);

        #rodal_referencia = crearArbol(dades_rodal2)
        context = {'rodal': rodal_referencia, 'rodalNombre': rodalNombre, 'rodalGraficos': rodalValNom, 'rodalGraficoPuntos': rodal_graficos_puntos, 'rodalChart': rodal_graficos_barras}

    return Response(context)

def datosGraficasPuntos(dades, infoRodal):

    #print(infoRodal)

    id_rodales = []
    lista = []
    for i in dades:
        if i['id_rodal'] not in id_rodales:
            id_rodales.append(i['id_rodal'])

        for t in id_rodales:
            if t == i['id_rodal']:
                for n in infoRodal:
                    if i['id_rodal'] == n['id']:
                        lista.append({
                            'id_rodal': i['id_rodal'],
                            'nombre': n['nombre'],
                            'indicador_cod': i['indicador_cod'],
                            'valor': i['valor']
                        })

    #print(lista)

    return(lista)

def datosGraficasBarras(dades, infoRodalBarCrite):
    print(dades)




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
    print(dades)
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
                cp_valor = round(indicador_cod['mitjana'], 2)

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
                ce_valor = round(indicador_cod['mitjana'], 2)

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
                sn_valor = round(indicador_cod['mitjana'], 2)

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
                hm_valor = round(indicador_cod['mitjana'], 2)

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
                dn_valor = round(indicador_cod['mitjana'], 2)

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
                hh_valor = round(indicador_cod['mitjana'], 2)

            if indicador_cod['stddev'] == None:
                hh_valor_desv = "---"
            else:
                hh_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'ha':
            if indicador_cod['mitjana'] == None:
                ha_valor = "---"
            else:
                ha_valor = round(indicador_cod['mitjana'], 2)

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
                hr_valor = round(indicador_cod['mitjana'], 2)

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
                ie_valor = round(indicador_cod['mitjana'], 2)

            if indicador_cod['stddev'] == None:
                ie_valor_desv = "---"
            else:
                ie_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'ar':
            if indicador_cod['mitjana'] == None:
                ar_valor = "---"
            else:
                ar_valor = round(indicador_cod['mitjana'], 2)

            if indicador_cod['stddev'] == None:
                ar_valor_desv = "---"
            else:
                ar_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'cf':
            if indicador_cod['mitjana'] == None:
                cf_valor = "---"
            else:
                cf_valor = round(indicador_cod['mitjana'], 2)

            if indicador_cod['stddev'] == None:
                cf_valor_desv = "---"
            else:
                cf_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'eb':
            if indicador_cod['mitjana'] == None:
                eb_valor = "---"
            else:
                eb_valor = round(indicador_cod['mitjana'], 2)

            if indicador_cod['stddev'] == None:
                eb_valor_desv = "---"
            else:
                eb_valor_desv = indicador_cod['stddev']

        if indicador_cod['indicador_cod'] == 'cn':
            if indicador_cod['mitjana'] == None:
                cn_valor = "---"
            else:
                cn_valor = round(indicador_cod['mitjana'], 2)

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

def crearArbolGraficos(dades):
    print(len(dades))

    lista = []
    ind = None
    list2 = []

    for indicador_cod in dades:
        if ind != indicador_cod.id_rodal:
            ind = indicador_cod.id_rodal
            lista.append(ind)

        if indicador_cod.indicador_cod == 'nm':
            if indicador_cod.valor == None:
                nm_valor = "---"
            else:
                nm_valor = round(indicador_cod.valor, 2)
            lista.append(nm_valor)

        if indicador_cod.indicador_cod == 'ie':
            if indicador_cod.valor == None:
                ie_valor = "---"
            else:
                ie_valor = round(indicador_cod.valor, 2)
            lista.append(ie_valor)
        if indicador_cod.indicador_cod == 'hh':
            if indicador_cod.valor == None:
                hh_valor = "---"
            else:
                hh_valor = round(indicador_cod.valor, 2)
            lista.append(hh_valor)
        if indicador_cod.indicador_cod == 'sn':
            if indicador_cod.valor == None:
                sn_valor = "---"
            else:
                sn_valor = round(indicador_cod.valor, 2)
            lista.append(sn_valor)
        if indicador_cod.indicador_cod == 'hr':
            if indicador_cod.valor == None:
                hr_valor = "---"
            else:
                hr_valor = round(indicador_cod.valor, 2)
            lista.append(hr_valor)
        if indicador_cod.indicador_cod == 'hm':
            if indicador_cod.valor == None:
                hm_valor = "---"
            else:
                hm_valor = round(indicador_cod.valor, 2)
            lista.append(hm_valor)
        if indicador_cod.indicador_cod == 'ha':
            if indicador_cod.valor == None:
                ha_valor = "---"
            else:
                ha_valor = round(indicador_cod.valor, 2)
            lista.append(ha_valor)
        if indicador_cod.indicador_cod == 'eb':
            if indicador_cod.valor == None:
                eb_valor = "---"
            else:
                eb_valor = round(indicador_cod.valor, 2)
            lista.append(eb_valor)
        if indicador_cod.indicador_cod == 'dn':
            if indicador_cod.valor == None:
                dn_valor = "---"
            else:
                dn_valor = round(indicador_cod.valor, 2)
            lista.append(dn_valor)
        if indicador_cod.indicador_cod == 'cp':
            if indicador_cod.valor == None:
                cp_valor = "---"
            else:
                cp_valor = round(indicador_cod.valor, 2)
            lista.append(cp_valor)
        if indicador_cod.indicador_cod == 'cn':
            if indicador_cod.valor == None:
                cn_valor = "---"
            else:
                cn_valor = round(indicador_cod.valor, 2)
            lista.append(cn_valor)
        if indicador_cod.indicador_cod == 'cf':
            if indicador_cod.valor == None:
                cf_valor = "---"
            else:
                cf_valor = round(indicador_cod.valor, 2)
            lista.append(cf_valor)
        if indicador_cod.indicador_cod == 'ce':
            if indicador_cod.valor == None:
                ce_valor = "---"
            else:
                ce_valor = round(indicador_cod.valor, 2)
            lista.append(ce_valor)
        if indicador_cod.indicador_cod == 'ar':
            if indicador_cod.valor == None:
                ar_valor = "---"
            else:
                ar_valor = round(indicador_cod.valor, 2)
            lista.append(ar_valor)

    list2.extend(lista)

    #print(list2)

######   Valores del rodal    #########
    rodal_graficos = {
        'naturalidad': {
            'valor': nm_valor,
            'composicion': {
                'valor': cp_valor,
            },
            'complejidad': {
                'valor': ce_valor,
            },
            'senectud': {
                'valor': sn_valor,
            },
            'micro_habitats': {
                'valor': hm_valor,
            },
            'dinamica': {
                'valor': dn_valor,
            }
        },
        'huellaHumana': {
            'valor': hh_valor,
            'antigua': {
                'valor': ha_valor,
            },
            'reciente': {
                'valor': hr_valor,
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
    return rodal_graficos

def login(request):

    login_form = LoginForm()

    if request.user.is_authenticated:
        return redirect('herramientas')

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
                    return redirect('registration_complete')
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

    ccaa = TeProvincia.objects.filter(nivel='Com. autònoma').order_by('nombre_es')
    prov = TeProvincia.objects.filter(nivel='Província').order_by('nombre_es')
    muni = TeMunicipi.objects.all().order_by('nombre').order_by('nombre')

    comAut = []
    for x in ccaa:
        comAut.append({
            'cod': x.cod,
            'nombre': x.nombre_es
        })

    provincias = []
    for p in prov:
        provincias.append({
            'cod': p.cod,
            'nombre': p.nombre_es
        })

    municipio = []
    for m in muni:
        municipio.append({
            'id': m.id,
            'nombre': m.nombre
        })

    geojsoncollection_string = None

    if request.method == 'POST':
        form = rodalFormFields(request.POST or None, instance=datos)

        current_user = request.user.id
        user = AuthUser.objects.get(id=current_user)
        json_geometry = None
        multipoligon = []

        if request.POST.get("geometria_string","") != '':
            try:
                #json_geometry = json.loads(request.POST["geometria_string"])
                json_geometry = request.POST["geometria_string"]
                json_geometry_dict = json.loads(json_geometry)
                for feature in json_geometry_dict['features']:
                    feature_geometry = GEOSGeometry(json.dumps(feature['geometry']))
                    feature_geometry.transform(25830)
                    multipoligon.append(feature_geometry)
            except JSONDecodeError:
                pass

        if len(multipoligon) == 0:
            messages.add_message(request, messages.ERROR,'No has entrado los límites del rodal. Por favor, éntralos y vuelve a intentar guardar')
        else:
            if form.is_valid():
                dades = form.save(commit=False)
                dades.usuario = user

                mp = MultiPolygon(multipoligon)
                dades.geom = mp
                dades.save()

                # return HttpResponseRedirect('/redbosques/rodalForm2/' + str(dades.id) + '/')
                return redirect('rodalForm2', id=dades.id)
            else:
                geojsoncollection_string = request.POST["geometria_string"]
    else:
        datos = get_object_or_404(Rodal, id=id)
        form = rodalFormFields(instance=datos)

        buffer = []
        if datos.geom != 'null':
            geom = datos.geom
            geom.transform(4326)
            g = ogr.CreateGeometryFromJson(geom.json)

            #buffer = []
            for idx, f in enumerate(g):
                geojson_string = f.ExportToJson()
                buffer.append(dict(type="Feature", geometry=json.loads(geojson_string)))

            geojsoncollection_string = json.dumps({"type": "FeatureCollection", "features": buffer})
        else:
            buffer.append(dict(type="Feature", geometry=""))
            geojsoncollection_string = json.dumps({"type": "FeatureCollection", "features": buffer})

    context = {'form': form, 'geojson_string': geojsoncollection_string, 'id': id, 'comAut': comAut, 'provincias': provincias, 'municipio': municipio}
    return render(request, 'redbosques_main/editrodalForm.html', context)




@login_required(login_url="login/")
def eliminarRodal(request, id=None):
    Rodal.objects.filter(id=id).delete()
    context = menuData(request)
    return redirect('menu')



def menuData(request):
    current_user = request.user
    du = None
    try:
        du = DatosUsuario.objects.get(user=current_user)
        print(du)
    except DatosUsuario.DoesNotExist:
        pass

    #user = User.objects.get(usuario=current_user)


    rodalesSelector = []
    rodalesFase1Selector = []
    rodals_list = Rodal.objects.exclude(geom__isnull=True).order_by('nombre')
    rodalsF1_list = RodalProsp.objects.exclude(geom__isnull=True).order_by('nombre')

    for r in rodals_list:
        if r.usuario.id == du.id:
            rodalesSelector.append({'id_rodal': r.id, 'nombre': r.nombre + '(*)'})
        else:
            rodalesSelector.append({'id_rodal': r.id, 'nombre': r.nombre})

    for f1 in rodalsF1_list:
        if f1.usuario.id == du.id:
            rodalesFase1Selector.append({'id_rodal': f1.id, 'nombre': f1.nombre + '(*)'})
        else:
            rodalesFase1Selector.append({'id_rodal': f1.id, 'nombre': f1.nombre})

    rodalesFicha = []
    rodPDF = DatosGeneralesRodal.objects.all().order_by('nombre_rodal')

    for t in rodPDF:
        rodalesFicha.append({
            'id_rodal': t.id_rodal,
            'nombre': t.nombre_rodal
        })


    rodalesSelectorEditor = []

    if du.admin_institucion:
        usDat = DatosUsuario.objects.filter(institucion_id=du.institucion_id).values('user_id')

        usuarios = AuthUser.objects.filter(id__in=usDat).values('id')
        rodals_list_2 = Rodal.objects.filter(usuario__in=usuarios).exclude(geom__isnull=True).values('id', 'nombre').order_by('nombre')

        for test in rodals_list_2:
            rodalesSelectorEditor.append({'id_rodal': test['id'], 'nombre': test['nombre']})


    else:
        usDat = DatosUsuario.objects.filter(id=du.id).values('user_id')
        usuarios = AuthUser.objects.filter(id__in=usDat).values('id')
        rodals_list_2 = Rodal.objects.filter(usuario__in=usuarios).exclude(geom__isnull=True).values('id', 'nombre').order_by('nombre')

        for test in rodals_list_2:
            rodalesSelectorEditor.append({'id_rodal': test['id'], 'nombre': test['nombre']})


    context = {'herramientas': 'Herramienta de evaluación de rodales maduros', 'rodalesSelector': rodalesSelector, 'du': du, 'rodalesSelectorEditor': rodalesSelectorEditor, 'datosGenFichaPDF': rodalesFicha, 'rodalesFase1Selector': rodalesFase1Selector}

    return context




@login_required(login_url="login/")
def rodalForm(request):
    ccaa = TeProvincia.objects.filter(nivel='Com. autònoma').order_by('nombre_es')
    prov = TeProvincia.objects.filter(nivel='Província').order_by('nombre_es')
    muni = TeMunicipi.objects.all().order_by('nombre').order_by('nombre')

    selected_ccaa = None
    selected_prov = None
    selected_muni = None
    json_geometry = None
    multipoligon = []

    comAut = []
    for x in ccaa:
        comAut.append({
            'cod': x.cod,
            'nombre': x.nombre_es
        })

    provincias = []
    for p in prov:
        provincias.append({
            'cod': p.cod,
            'nombre': p.nombre_es
        })

    municipio = []
    for m in muni:
        municipio.append({
            'id': m.id,
            'nombre': m.nombre
        })

    json_geometry = None
    form = rodalFormFields()
    if request.method == 'POST':
        form = rodalFormFields(request.POST or None)

        #ccaa = TeProvincia.objects.get(codigo=form.data['comautonom_cod'], nivel='Com. autònoma')
        selected_ccaa = form.data['comautonom_cod']
        #prov = TeProvincia.objects.get(codigo=form.data['provincia_cod'], nivel='Província')
        selected_prov = form.data['provincia_cod']
        #muni = TeMunicipi.objects.get(id=form.data['municipio1'])
        selected_muni = form.data['municipio1']
        current_user = request.user.id
        user = AuthUser.objects.get(id=current_user)

        if request.POST.get("geometria_string","") != '':
            try:
                json_geometry = request.POST["geometria_string"]
                json_geometry_dict = json.loads(json_geometry)
                for feature in json_geometry_dict['features']:
                    feature_geometry = GEOSGeometry(json.dumps(feature['geometry']))
                    feature_geometry.transform(25830)
                    multipoligon.append(feature_geometry)
            except JSONDecodeError:
                pass

        if len(multipoligon) == 0:
            messages.add_message(request, messages.ERROR, 'No has entrado los límites del rodal. Por favor, éntralos y vuelve a intentar guardar')
        else:
            if form.is_valid():
                dades = form.save(commit=False)

                dades.usuario = user
                #dades.comautonom_cod = ccaa
                #dades.provincia_cod = prov
                #dades.municipio1 = muni

                mp = MultiPolygon(multipoligon)
                dades.geom = mp
                dades.save()

                return redirect('rodalForm2', id=dades.id)
    else:
        form = rodalFormFields()

    #else:
    #    form = rodalFormFields()
    #    json_geometry = ''

    #context = {'form': form, 'comAut': comAut, 'provincias': provincias, 'municipio': municipio, 'json_geometry': json_geometry}

    context = {
        'form': form,
        'comAut': comAut, 'provincias': provincias, 'municipio': municipio,
        'selected_ccaa': selected_ccaa, 'selected_prov': selected_prov, 'selected_muni': selected_muni,
        'json_geometry': json_geometry
    }

    return render(request, 'redbosques_main/rodalesForm.html', context)


@api_view(['GET'])
@login_required(login_url="login/")
def comAutFilt(request):


    idCcaa = request.query_params.get('id', None)

    prov = TeProvincia.objects.filter(parent=idCcaa).order_by('nombre_es')
    # prov2 = TeProvincia.objects.filter(parent=idCcaa).values('codigo')

    provincias = []
    for p in prov:
        provincias.append({
            'cod': p.cod,
            'nombre': p.nombre_es
        })


    for x in prov:
        provMun = TeMunicipi.objects.filter(codprov=x.codigo).order_by('nombre')


    municipios = []
    for m in provMun:
        municipios.append({
            'id': m.id,
            'nombre': m.nombre
        })

    print(municipios)

    context = {'provincias': provincias, 'municipios': municipios}
    return Response(context)

@api_view(['GET'])
@login_required(login_url="login/")
def provFilt(request):
    idProv = request.query_params.get('id', None)
    test = idProv.split(".", 2)
    print(test[1])
    muni = TeMunicipi.objects.filter(codprov=test[1]).order_by('nombre')

    municipios = []
    for m in muni:
        municipios.append({
            'id': m.id,
            'nombre': m.nombre
        })

    context = {'municipios': municipios}
    return Response(context)



@login_required(login_url="login/")
def rodalForm2(request, id=None):

    adminInstitucion = request.user.datosusuario.admin_institucion
    #du = DatosUsuario.objects.get(user=current_user)
    #print(du)

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
                                        'as stats from carto.bosque_ps '
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
                                     'as stats from carto.bosque_cf '
                                     'WHERE ST_Intersects(rast, ST_GeomFromText(%s, 25830)) ) as foo',
                                     [geom.wkt, geom.wkt])

    distCoreArea = cursor.fetchall()
    ##############################################

    # print("Área: " + str(round(area/10000, 1)) + " ha")
    # print("Continuidad mancha forestal: " + str(round(contManchForest[0][0]/100, 2)) + " km2")
    # print("Densidad de bosque: " + str(densBosque[0][0]) + " %")
    # print("Distancia a la core área: " + str(round(distCoreArea[0][0]/1000, 1)) + " Km")


    areaHectareas = round(area / 10000, 1)

    if contManchForest[0][0] == None:
        contManchForestKM2 = 0
    else:
        contManchForestKM2 = round(contManchForest[0][0]/100, 2)


    if densBosque[0][0] == None:
        densBosquexcent = 0
    else:
        densBosquexcent = round(densBosque[0][0], 2)


    if distCoreArea[0][0] == None:
        distCoreAreaKM = 68000/1000
    else:
        distCoreAreaKM = round(distCoreArea[0][0] / 1000, 1)

    # contManchForestKM2 = round(contManchForest[0][0] / 1000, 2)
    # densBosquexcent = round(densBosque[0][0] / 100, 2)
    # distCoreAreaKM = round(distCoreArea[0][0] / 1000, 2)

    # print("Área: " + str(areaHectareas) + " ha")
    # print("Continuidad mancha forestal: " + str(contManchForestKM2) + " km2")
    # print("Densidad de bosque: " + str(densBosquexcent) + " %")
    # print("Distancia a la core área: " + str(distCoreAreaKM) + " Km")

    valMedios = TeIndicador.objects.filter(val_alerta__isnull=False).values('variable_rodal', 'val_alerta')

    valMediosAlerta = []
    for va in valMedios:
        valMediosAlerta.append({
            'nom_variable': va['variable_rodal'],
            'valorAlerta': va['val_alerta']
        })

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
               'valHerb': valHerbArray,
               'adminInstitucion': adminInstitucion,
               'valMediosAlerta': valMediosAlerta
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
                'foto': lf.foto,
                'fotoPrincipal': lf.fotoprincipal
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


############################ CRUD Images/Docs ##################################

@login_required(login_url="login/")
def uploadImage(request, id):

    if request.method == 'POST':

        form = rodalFormFields3Foto(request.POST, request.FILES)

        if form.is_valid():
            foto = form.save(commit=False)
            foto.id_rodal = Rodal.objects.get(id=id)
            foto.nombre_foto = foto.foto.name
            foto.fotoprincipal = False
            foto.save()


            oldSelectedExists = FotosRodal.objects.filter(id_rodal=id).filter(fotoprincipal=True)

            oldSelected = None

            if(oldSelectedExists):
                oldSelected = FotosRodal.objects.filter(id_rodal=id).filter(fotoprincipal=True).update(fotoprincipal=False)
                newSelected = FotosRodal.objects.filter(id_foto=foto.id_foto).update(fotoprincipal=True)
            else:
                newSelected = FotosRodal.objects.filter(id_foto=foto.id_foto).update(fotoprincipal=True)

            data = {'is_valid': True, 'nombre_foto': foto.nombre_foto, 'url': foto.foto.url, 'id_foto': foto.id_foto, 'oldSelected': oldSelected, 'newSelected': newSelected}

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


@api_view(['POST'])
def mainImage(request, idRodal, fotoSelected):
    oldSelected = FotosRodal.objects.filter(id_rodal=idRodal).filter(fotoprincipal=True).update(fotoprincipal=False)
    newSelected = FotosRodal.objects.filter(id_foto=fotoSelected).update(fotoprincipal=True)

    context = {'oldSelected': oldSelected, 'newSelected': newSelected}

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

######################################################################################

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

    rodalesTable = rodalesTable.distinct().values('id_rodal','nombre','rodalref','ccaa_nom','ccaa_nombre','regbio_cod','nombre_es').order_by('nombre')

    rodales = []
    for r in rodalesTable:
        rodales.append({
            'id_rodal': r['id_rodal'],
            'nombre': r['nombre'],
            'rodalref': r['rodalref'],
            'codi_ccaa' : r['ccaa_nom'],
            'ccaa_nombre': r['ccaa_nombre'],
            'codi_rb': r['regbio_cod'],
            'nom_rb': r['nombre_es']
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

    #print(codiHabitat)
    #print(codiComaut)
    #print(codiregBiogeo)
    #print(rodalReferencia)


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
                        if sf.shapeTypeName == 'POLYGONZ':
                            content = {'success': False, 'detail': 'El archivo shapefile tiene que ser en 2D'}
                            return Response(data=content, status=400)
                        else:
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
                        content = {'success': False, 'detail': 'El archivo shapefile tiene un formato incorrecto'}
                        return Response(data=content, status=400)
                content = {'success': False,
                           'detail': 'No se ha encontrado ningún fichero con exetensión *.shp dentro del zip, no puedo importar nada.'}
                return Response(data=content, status=400)


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
    send_to_admin = []
    try:
        u = dUser.objects.get(email=email)
        du = DatosUsuario.objects.get(user=u)
        institucion = du.institucion
        capi = DatosUsuario.objects.filter(institucion=institucion).filter(admin_institucion=True)
        for capo in capi:
            send_to_admin.append(capo.user.email)
        context = {
            'email': email,
            'institution': institucion.nombre
        }
        context_admin = {
            'solicitant_email': email,
            'institution': institucion.nombre,
            'user_activation_link': settings.APP_BASE_URL + reverse('user_admin')
        }

        #send email to solicitant
        plaintext = get_template('email_templates/created_email_template.txt')
        text_content = plaintext.render(context)
        milio = EmailMessage("Tu cuenta de RedBosques ha sido creada", text_content, to=send_to)
        milio.send()

        #send copy to admins
        plaintext = get_template('email_templates/user_created_admin_notif.txt')
        text_content = plaintext.render(context_admin)
        milio = EmailMessage("Redbosques - usuario " + email + " solicita activación de cuenta", text_content, to=send_to_admin)
        milio.send()

    except dUser.DoesNotExist:
        print("No se puede mandar el correo a " + email + ", no existe un usuario con este correo electrónico")


def registration_complete(request):
    return render(request, 'registration/registration_complete.html', {})


def contacto(request):
    return render(request, 'redbosques_main/contacto.html')

@api_view(['GET','POST'])
def crearPDF(request, id):

    #print(request.query_params.get('imagen', None))
    #test = request.query_params.get('img', None)
    #print(test)

    imagenMapa = request.data['image']

    logger = logging.getLogger('weasyprint')
    logger.addHandler(logging.FileHandler('/tmp/weasyprint.log'))

    dades_rodal = RodalValorres2.objects.filter(id_rodal=id)
    info_rodal = WebCompDataValAmb.objects.filter(id_rodal=id).filter(eje_cod="nm")
    rodalArbol = crearArbol(dades_rodal)
    datgen = DatosGeneralesRodal.objects.filter(id_rodal=id)
    imgRodal = FotosRodal.objects.filter(id_rodal=id).filter(fotoprincipal="True")


    if imgRodal is not None:
        imagenRodal = []
        for i in imgRodal:
            foto = i.foto.url
            urlFoto = APP_BASE_URL + foto

            imagenRodal = {
                'id_rodal': i.id_rodal,
                'id_foto': i.id_foto,
                'nombre_foto': i.nombre_foto,
                'foto': foto,
                'fotoprincipal': i.fotoprincipal
            }
    else:
        imagenRodal = ""
        foto = ""


    datosGenerales = []
    for dg in datgen:
        area = dg.geom.area
        areaHect = round(area / 10000, 1)

        datosGenerales = {
            'id_rodal': dg.id_rodal,
            'nombre': dg.nombre_rodal,
            'geom': dg.geom,
            'datosRestringidos': dg.datosrestringidos,
            'regbio_cod': dg.regbio_cod,
            'regbio': dg.regbio,
            'provincia': dg.provincia,
            'comAut': dg.com_aut,
            'muni': dg.nombre,
            'propietario': dg.propietario,
            'lpeht': dg.lpeht,
            'hic': dg.hic,
            'lpeht_cod': dg.lpeht_cod,
            'hic_cod': dg.hic_cod,
            'fecha': dg.fecha,
            'equipo': dg.equipo,
            'otroespflora': dg.otroespflora,
            'otrohics': dg.otrohics,
            'otroinfo': dg.otroinfo,
            'area': areaHect
        }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'
    response['Content-Disposition'] = 'filename="RODAL.pdf"'
    html_string = render_to_string("pdf_templates/pdf_template.html", {'rodal': rodalArbol, 'datosGenerales': datosGenerales, 'imagenMapa': imagenMapa, 'imagenRodal': imagenRodal, 'app_base_url': APP_BASE_URL, 'fotoRodal': foto})
    #response.write(HTML(string=html_string, base_url='http://127.0.0.1:8000/redbosques/crearPDF/91').write_pdf())
    #response.write(HTML(string=html_string).write_pdf())
    pdf_file = HTML(string=html_string, base_url=STATIC_PDF_ROOT).write_pdf()
    response.write(pdf_file)



    #response.write(HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(settings.STATIC_URL + 'redbosques_main/css/redbosques.css')],presentational_hints=True))
    #pdf = response.write_pdf(stylesheets=[CSS(settings.STATIC_URL + '/css/redbosques.css')],presentational_hints=True);

    return response

@login_required(login_url="login/")
def verFichaRodal(request, id):
    dades_rodal = RodalValorres2.objects.filter(id_rodal=id)
    info_rodal = WebCompDataValAmb.objects.filter(id_rodal=id).filter(eje_cod="nm")
    rodalArbol = crearArbol(dades_rodal)
    datgen = DatosGeneralesRodal.objects.filter(id_rodal=id)
    imgRodal = FotosRodal.objects.filter(id_rodal=id).filter(fotoprincipal="True")


    imagenRodal = []
    for i in imgRodal:
        imagenRodal = {
            'id_rodal': i.id_rodal,
            'id_foto': i.id_foto,
            'nombre_foto': i.nombre_foto,
            'foto': i.foto,
            'fotoprincipal': i.fotoprincipal
        }



    datosGenerales = []
    for dg in datgen:
        area = dg.geom.area
        areaHect = round(area/10000, 1)

        datosGenerales = {
            'id_rodal': dg.id_rodal,
            'nombre': dg.nombre_rodal,
            'geom': dg.geom,
            'datosRestringidos': dg.datosrestringidos,
            'regbio_cod': dg.regbio_cod,
            'regbio': dg.regbio,
            'provincia': dg.provincia,
            'comAut': dg.com_aut,
            'muni': dg.nombre,
            'propietario': dg.propietario,
            'lpeht': dg.lpeht,
            'hic': dg.hic,
            'lpeht_cod': dg.lpeht_cod,
            'hic_cod': dg.hic_cod,
            'fecha': dg.fecha,
            'equipo': dg.equipo,
            'otroespflora': dg.otroespflora,
            'otrohics': dg.otrohics,
            'otroinfo': dg.otroinfo,
            'area': areaHect
        }

        buffer = []
        if dg.geom != 'null':
            geom = dg.geom
            geom.transform(4326)
            g = ogr.CreateGeometryFromJson(geom.json)

            # buffer = []
            for idx, f in enumerate(g):
                geojson_string = f.ExportToJson()
                buffer.append(dict(type="Feature", geometry=json.loads(geojson_string)))

            geojsoncollection_string = json.dumps({"type": "FeatureCollection", "features": buffer})
        else:
            buffer.append(dict(type="Feature", geometry=""))
            geojsoncollection_string = json.dumps({"type": "FeatureCollection", "features": buffer})



    #########333############ FUNCIONA ###
    #paragraphs = ['first paragraph', 'second paragraph', 'third paragraph']
    #html_string = render_to_string('pdf_templates/pdf_template.html', {'paragraphs': paragraphs, 'rodal': rodalArbol})
    #css_string = render_to_string('pdf_templates/pdfStyles.css')
    #css = CSS(string=css_string)
    #response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment'
    #html_string = render_to_string("pdf_templates/pdf_template.html", {'rodal': rodalArbol})
    #response.write(HTML(string=html_string).write_pdf(response))
    #return response
    ####################################################
    print(rodalArbol)
    print(datosGenerales)
    print(geojsoncollection_string)
    print(imagenRodal)

    context = {'rodal': rodalArbol, 'datosGenerales': datosGenerales, 'geojson_string': geojsoncollection_string, 'imagenRodal': imagenRodal}
    return render(request, 'redbosques_main/fichaRodal.html', context)

def comparadorGraficos(request, id = None):
    init_params = {}
    if id is not None:
        valors_ini = WebMapaValAmb.objects.filter(id_rodal=id).distinct().values('habitat_cod', 'ccaa_nom',
                                                                                 'regbio_cod').first()

        if valors_ini is None:
            raise Http404("No hay datos de comparacion para el rodal seleccionado")

        # recuperar hàbitat inicial, ccaa inicial, regio inicial
        habitat_ini = valors_ini['habitat_cod']
        # ccaa_ini = valors_ini['ccaa_nom']
        # regbio_ini = valors_ini['regbio_cod']

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
                if not d['id_rodal'] in already_in_there:
                    already_in_there.add(d['id_rodal'])
                    if d['rodalref'] == True:
                        rodals_ini_list.append({'id_rodal': d['id_rodal'], 'nombre': d['nombre'], 'rodalref': 1})
                    else:
                        rodals_ini_list.append({'id_rodal': d['id_rodal'], 'nombre': d['nombre'], 'rodalref': 0})
            rodals_ini_list.sort(key=lambda x: x['nombre'])

            init_params['rodal_ini'] = id
            init_params['habitat_ini'] = habitat_ini
            # init_params['ccaa_ini']=ccaa_ini
            # init_params['regbio_ini'] = regbio_ini
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
        context = {'tiposDeBosque': tipoBosqueData, 'habitats': habitatData}
    else:
        context = {'tiposDeBosque': tipoBosqueData, 'habitats': habitatData, 'init_params': init_params}

    return render(request, 'redbosques_main/comparadorGraficos.html', context)

@login_required(login_url="login/")
def rodalFormFase1(request, id=None):
    form = rodalFormFase1Fields()

    ccaa = TeProvincia.objects.filter(nivel='Com. autònoma').order_by('nombre_es')
    prov = TeProvincia.objects.filter(nivel='Província').order_by('nombre_es')
    muni = TeMunicipi.objects.all().order_by('nombre').order_by('nombre')

    selected_ccaa = None
    selected_prov = None
    selected_muni = None
    #json_geometry = None
    rodalMarker = []

    comAut = []
    for x in ccaa:
        comAut.append({
            'cod': x.cod,
            'nombre': x.nombre_es
        })

    provincias = []
    for p in prov:
        provincias.append({
            'cod': p.cod,
            'nombre': p.nombre_es
        })

    municipio = []
    for m in muni:
        municipio.append({
            'id': m.id,
            'nombre': m.nombre
        })

    #json_geometry = None

    if request.method == 'POST':

        form = rodalFormFase1Fields(request.POST or None)

        # ccaa = TeProvincia.objects.get(codigo=form.data['comautonom_cod'], nivel='Com. autònoma')
        selected_ccaa = form.data['comautonom_cod']
        # prov = TeProvincia.objects.get(codigo=form.data['provincia_cod'], nivel='Província')
        selected_prov = form.data['provincia_cod']
        # muni = TeMunicipi.objects.get(id=form.data['municipio1'])
        selected_muni = form.data['municipio1']
        current_user = request.user.id
        user = AuthUser.objects.get(id=current_user)

        if request.POST.get("marker_string", "") != '':
            try:
                json_marker = request.POST["marker_string"]
                json_marker_dict = json.loads(json_marker)

                feature_marker = GEOSGeometry(json.dumps(json_marker_dict['geometry']))
                feature_marker.transform(25830)

            except JSONDecodeError:
                pass

        if len(feature_marker) == 0:
            messages.add_message(request, messages.ERROR,
                                 'No has entrado los límites del rodal. Por favor, éntralos y vuelve a intentar guardar')
        else:

            if form.is_valid():
                dades = form.save(commit=False)
                dades.usuario = user
                dades.geom = feature_marker
                dades.save()

                return redirect('rodalFormFase1_2', id=dades.id)

    else:
        form = rodalFormFase1Fields()


    context = {
        'form': form,
        'comAut': comAut, 'provincias': provincias, 'municipio': municipio,
        'selected_ccaa': selected_ccaa, 'selected_prov': selected_prov, 'selected_muni': selected_muni,
        #'json_geometry': json_geometry
    }


    return render(request, 'redbosques_main/rodalFormFase1.html', context)


@login_required(login_url="login/")
def rodalFormFase1_2(request, id=None):
    #datos = get_object_or_404(Rodal, id=id)

    id_rodal = id

    allFotos = FotosRodalProsp.objects.all()
    listaFotos = allFotos.filter(id_rodal=id_rodal)

    fotos = []
    for lf in listaFotos:
        fotos.append({
            'id_foto': lf.id_foto,
            'nombre_foto': lf.nombre_foto,
            'foto': lf.foto,
            'fotoPrincipal': lf.fotoprincipal
        })

    allDocs = DocsRodalProsp.objects.all()
    listaDocs = allDocs.filter(id_rodal=id_rodal)

    docs = []
    for ld in listaDocs:
        docs.append({
            'id_doc': ld.id_doc,
            'nombre_doc': ld.nombre_doc,
            'doc': ld.doc
        })

    #context = {'listaFotos': fotos, 'id': id_rodal, 'listaDocs': docs, 'form': form}
    context = {'listaFotos': fotos, 'id': id_rodal, 'listaDocs': docs}
    return render(request, 'redbosques_main/rodalFormFase1_2.html', context)



    #return redirect('menu')


@login_required(login_url="login/")
def editRodalFormFase1(request, id=None):

    datos = get_object_or_404(RodalProsp, id=id)
    #form = rodalFormFields(instance=datos)

    ccaa = TeProvincia.objects.filter(nivel='Com. autònoma').order_by('nombre_es')
    prov = TeProvincia.objects.filter(nivel='Província').order_by('nombre_es')
    muni = TeMunicipi.objects.all().order_by('nombre').order_by('nombre')

    comAut = []
    for x in ccaa:
        comAut.append({
            'cod': x.cod,
            'nombre': x.nombre_es
        })

    provincias = []
    for p in prov:
        provincias.append({
            'cod': p.cod,
            'nombre': p.nombre_es
        })

    municipio = []
    for m in muni:
        municipio.append({
            'id': m.id,
            'nombre': m.nombre
        })

    geojsoncollection_string = None

    if request.method == 'POST':
        form = rodalFormFase1Fields(request.POST or None, instance=datos)
        

        current_user = request.user.id
        user = AuthUser.objects.get(id=current_user)
        json_geometry = None
        multipoligon = []

        if request.POST.get("marker_string", "") != '':
            try:
                json_marker = request.POST["marker_string"]
                json_marker_dict = json.loads(json_marker)
                print(json_marker)
                print(json_marker_dict)

                #if hasattr(json_marker_dict, 'geometry'):
                #if (json_marker_dict).has_key('geometry'):
                if 'geometry' in json_marker_dict:
                    geometria = json.dumps(json_marker_dict["geometry"])
                else:
                    geometria = json.dumps(json_marker_dict)
                print(geometria)

                feature_marker = GEOSGeometry(geometria)
                feature_marker.transform(25830)


            except JSONDecodeError:
                pass

        if len(feature_marker) == 0:
            messages.add_message(request, messages.ERROR,'No has entrado los límites del rodal. Por favor, éntralos y vuelve a intentar guardar')
        else:
            if form.is_valid():
                dades = form.save(commit=False)
                dades.usuario = user

                #mp = MultiPolygon(multipoligon)
                dades.geom = feature_marker
                dades.save()

                return HttpResponseRedirect('/redbosques/rodalFormFase1_2/' + str(dades.id) + '/')
                # return redirect('menu')
            else:
                geojsoncollection_string = request.POST["marker_string"]
    else:
        datos = get_object_or_404(RodalProsp, id=id)
        form = rodalFormFase1Fields(instance=datos)

        buffer = []
        if datos.geom != 'null':
            geom = datos.geom
            geom.transform(4326)
            buffer = geom.geojson
            geojsoncollection_string = json.dumps(buffer)

        else:
            buffer.append(dict(type="Feature", geometry=""))
            geojsoncollection_string = json.dumps({"type": "Feature", "properties": {}, "geometry": buffer})


    context = {'form': form, 'geojson_string': buffer, 'id': id, 'comAut': comAut, 'provincias': provincias, 'municipio': municipio}
    return render(request, 'redbosques_main/editRodalFormFase1.html', context)



@login_required(login_url="login/")
def eliminarRodalFase1(request, id=None):
    RodalProsp.objects.filter(id=id).delete()
    context = menuData(request)
    return redirect('menu')


@login_required(login_url="login/")
def verFichaRodalFase1(request, id):
    dades_rodal = RodalProspDatosgen.objects.filter(id_rodal=id)
    valRod = RodalProspValores.objects.filter(id_rodal=id)
    imgRodal = FotosRodalProsp.objects.filter(id_rodal=id).filter(fotoprincipal="True")

    imagenRodal = []
    for i in imgRodal:
        imagenRodal = {
            'id_rodal': i.id_rodal,
            'id_foto': i.id_foto,
            'nombre_foto': i.nombre_foto,
            'foto': i.foto,
            'fotoprincipal': i.fotoprincipal
        }

    datosGenerales = []

    for dg in dades_rodal:
        datosGenerales = {
            'id_rodal': dg.id_rodal,
            'nombre': dg.nombre_rodal,
            'geom': dg.geom,
            'datosRestringidos': dg.datosrestringidos,
            'regbio_cod': dg.regbio_cod,
            'regbio': dg.regbio,
            'provincia': dg.provincia,
            'comAut': dg.com_aut,
            'muni': dg.nombre,
            'propietario': dg.propietario,
            'lpeht': dg.lpeht,
            'hic': dg.hic,
            'lpeht_cod': dg.lpeht_cod,
            'hic_cod': dg.hic_cod,
            'fecha': dg.fecha,
            'equipo': dg.equipo,
            'otroespflora': dg.otroespflora,
            'otrohics': dg.otrohics,
            'otroinfo': dg.otroinfo,
        }


        buffer = []
        if dg.geom != 'null':
            geom = dg.geom
            geom.transform(4326)
            g = ogr.CreateGeometryFromJson(geom.json)

            # buffer = []
            buffer.append(dict(type="Feature", geometry=json.loads(geom.json)))
            geojsoncollection_string = json.dumps({"type": "FeatureCollection", "features": buffer})
            '''for idx, f in enumerate(g):
                geojson_string = f.ExportToJson()
                buffer.append(dict(type="Feature", geometry=json.loads(g)))

            geojsoncollection_string = json.dumps({"type": "FeatureCollection", "features": buffer})'''
        else:
            buffer.append(dict(type="Feature", geometry=""))
            geojsoncollection_string = json.dumps({"type": "FeatureCollection", "features": buffer})


    valores = []
    for v in valRod:
        valores = {
            'valspparb': v.valspparb,
            'valmasa': v.valmasa,
            'valestratos': v.valestratos,
            'valarboexcep': v.valarboexcep,
            'valmmpie': v.valmmpie,
            'valmmsuelo': v.valmmsuelo,
            'valmicrohab': v.valmicrohab,
            'valhuecos': v.valhuecos,
            'valregen': v.valregen,
            'volarrodal': v.volarrodal

        }

    print(datosGenerales)
    print(valores)
    print(imagenRodal)

    context = {'datosGenerales': datosGenerales, 'geojson_string': geojsoncollection_string,
               'imagenRodal': imagenRodal, 'valores': valores}
    return render(request, 'redbosques_main/fichaRodalFase1.html', context)





############################ CRUD Images/Docs ##################################

@login_required(login_url="login/")
def uploadImageFase1(request, id):
    if request.method == 'POST':

        form = rodalFormFieldsFase1Foto(request.POST, request.FILES)

        if form.is_valid():
            foto = form.save(commit=False)
            foto.id_rodal = RodalProsp.objects.get(id=id)
            foto.nombre_foto = foto.foto.name
            foto.fotoprincipal = False
            foto.save()

            oldSelectedExists = FotosRodalProsp.objects.filter(id_rodal=id).filter(fotoprincipal=True)

            oldSelected = None

            if (oldSelectedExists):
                oldSelected = FotosRodalProsp.objects.filter(id_rodal=id).filter(fotoprincipal=True).update(
                    fotoprincipal=False)
                newSelected = FotosRodalProsp.objects.filter(id_foto=foto.id_foto).update(fotoprincipal=True)
            else:
                newSelected = FotosRodalProsp.objects.filter(id_foto=foto.id_foto).update(fotoprincipal=True)

            data = {'is_valid': True, 'nombre_foto': foto.nombre_foto, 'url': foto.foto.url, 'id_foto': foto.id_foto,
                    'oldSelected': oldSelected, 'newSelected': newSelected}

        else:
            errorMessage = "La imagen supera el tamaño permitido (2MB)"
            data = {'is_valid': False, 'error_imagen': form.errors['foto']}
        return JsonResponse(data)
    else:
        id_rodal = id
        allFotos = FotosRodalProsp.objects.all()
        listaFotos = allFotos.filter(id_rodal=id_rodal)

        fotos = []
        for lf in listaFotos:
            fotos.append({
                'id_foto': lf.id_foto,
                'nombre_foto': lf.nombre_foto,
                'foto': lf.foto
            })

        context = {'listaFotos': fotos, 'id': id_rodal}
        return render(request, 'redbosques_main/rodalesFormFase1_2.html', context)

@api_view(['POST'])
@login_required(login_url="login/")
def deleteImageFase1(request, id):

    rd = FotosRodalProsp.objects.filter(id_foto=id).values('id_rodal')

    rodalFotos = []
    for r in rd:
        id_rodal = r['id_rodal']
        '''rodalFotos.append({
            'id_rodal': 
        })'''

    if request.method == 'POST':
        foto = FotosRodalProsp.objects.get(id_foto=id)
        foto.delete()

    context = {'id': id_rodal, 'imagen': 'imagen'}

    return Response(context)


@api_view(['POST'])
def mainImageFase1(request, idRodal, fotoSelected):
    oldSelected = FotosRodalProsp.objects.filter(id_rodal=idRodal).filter(fotoprincipal=True).update(fotoprincipal=False)
    newSelected = FotosRodalProsp.objects.filter(id_foto=fotoSelected).update(fotoprincipal=True)

    context = {'oldSelected': oldSelected, 'newSelected': newSelected}

    return Response(context)


@login_required(login_url="login/")
def uploadDocsFase1(request, id):

    if request.method == 'POST':

        form = rodalFormFieldsFase1Doc(request.POST, request.FILES)

        if form.is_valid():
            doc = form.save(commit=False)
            doc.id_rodal = RodalProsp.objects.get(id=id)
            doc.nombre_doc = doc.doc.name
            doc.save()
            data = {'is_valid': True, 'nombre_doc': doc.nombre_doc, 'url': doc.doc.url, 'id_doc': doc.id_doc}
        else:
            data = {'is_valid': False, 'error_documento': form.errors['doc']}
        return JsonResponse(data)
    else:
        id_rodal = id
        allDocs = DocsRodalProsp.objects.all()
        listaDocs = allDocs.filter(id_rodal=id_rodal)

        docs = []
        for ld in listaDocs:
            docs.append({
                'id_doc': ld.id_doc,
                'nombre_doc': ld.nombre_doc,
                'doc': ld.doc
            })

        context = {'listaFotos': docs, 'id': id_rodal}
        return render(request, 'redbosques_main/rodalesFormFase1.html', context)

@api_view(['POST'])
@login_required(login_url="login/")
def deleteDocFase1(request, id):

    rd = DocsRodalProsp.objects.filter(id_doc=id).values('id_rodal')

    rodalFotos = []
    for d in rd:
        id_rodal = d['id_rodal']
        '''rodalFotos.append({
            'id_rodal': 
        })'''

    if request.method == 'POST':
        doc = DocsRodalProsp.objects.get(id_doc=id)
        doc.delete()
    #return redirect('rodalForm3', id=id_rodal)

    context = {'id': id_rodal, 'docs': 'docs'}

    return Response(context)

######################################################################################

@api_view(['GET','POST'])
def crearPDFFase1(request, id):
    imagenMapa = request.data['image']

    logger = logging.getLogger('weasyprint')
    logger.addHandler(logging.FileHandler('/tmp/weasyprint.log'))

    dades_rodal = RodalProspDatosgen.objects.filter(id_rodal=id)
    valRod = RodalProspValores.objects.filter(id_rodal=id)
    imgRodal = FotosRodalProsp.objects.filter(id_rodal=id).filter(fotoprincipal="True")

    if not imgRodal:
        imagenRodal = ""
        foto = ""
    else:
        imagenRodal = []
        for i in imgRodal:
            foto = i.foto.url
            urlFoto = APP_BASE_URL + foto

            imagenRodal = {
                'id_rodal': i.id_rodal,
                'id_foto': i.id_foto,
                'nombre_foto': i.nombre_foto,
                'foto': foto,
                'fotoprincipal': i.fotoprincipal
            }

    datosGenerales = []

    for dg in dades_rodal:
        datosGenerales = {
            'id_rodal': dg.id_rodal,
            'nombre': dg.nombre_rodal,
            'geom': dg.geom,
            'datosRestringidos': dg.datosrestringidos,
            'regbio_cod': dg.regbio_cod,
            'regbio': dg.regbio,
            'provincia': dg.provincia,
            'comAut': dg.com_aut,
            'muni': dg.nombre,
            'propietario': dg.propietario,
            'lpeht': dg.lpeht,
            'hic': dg.hic,
            'lpeht_cod': dg.lpeht_cod,
            'hic_cod': dg.hic_cod,
            'fecha': dg.fecha,
            'equipo': dg.equipo,
            'otroespflora': dg.otroespflora,
            'otrohics': dg.otrohics,
            'otroinfo': dg.otroinfo,
        }

    valores = []
    for v in valRod:
        valores = {
            'valspparb': v.valspparb,
            'valmasa': v.valmasa,
            'valestratos': v.valestratos,
            'valarboexcep': v.valarboexcep,
            'valmmpie': v.valmmpie,
            'valmmsuelo': v.valmmsuelo,
            'valmicrohab': v.valmicrohab,
            'valhuecos': v.valhuecos,
            'valregen': v.valregen,
            'volarrodal': v.volarrodal

        }



    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'
    response['Content-Disposition'] = 'filename="RODAL.pdf"'
    html_string = render_to_string("pdf_templates/pdf_template_fase1.html", {'datosGenerales': datosGenerales, 'valores': valores, 'imagenMapa': imagenMapa, 'imagenRodal': imagenRodal, 'app_base_url': APP_BASE_URL, 'fotoRodal': foto})
    pdf_file = HTML(string=html_string, base_url=STATIC_PDF_ROOT).write_pdf()
    response.write(pdf_file)

    return response


############################# IFN #############################################

def comparadorIFN(request, id=None):

    init_params = {}
    if id is not None:
        valors_ini = WebMapaValAmb.objects.filter(id_rodal=id).distinct().values('habitat_cod','ccaa_nom','regbio_cod').first()

        if valors_ini is None:
            raise Http404("No hay datos de comparacion para el rodal seleccionado")

        # recuperar hàbitat inicial, ccaa inicial, regio inicial
        habitat_ini = valors_ini['habitat_cod']
        #ccaa_ini = valors_ini['ccaa_nom']
        #regbio_ini = valors_ini['regbio_cod']

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
                if not d['id_rodal'] in already_in_there:
                    already_in_there.add(d['id_rodal'])
                    if d['rodalref'] == True:
                        rodals_ini_list.append({ 'id_rodal': d['id_rodal'],'nombre': d['nombre'],'rodalref': 1 })
                    else:
                        rodals_ini_list.append({'id_rodal': d['id_rodal'], 'nombre': d['nombre'],'rodalref': 0 })
            rodals_ini_list.sort(key=lambda x: x['nombre'])

            init_params['rodal_ini'] = id
            init_params['habitat_ini']=habitat_ini
            #init_params['ccaa_ini']=ccaa_ini
            #init_params['regbio_ini'] = regbio_ini
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

    return render(request, 'redbosques_main/comparador_ifn.html', context)



'''def crearArbolrodalIFN(dades):

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

            if valor2.indicador_cod == 'mp':
                if valor2.valor == None:
                    mp_valor = "---"
                else:
                    mp_valor = round(valor2.valor)

            if valor2.indicador_cod == 'pi':
                if valor2.valor == None:
                    pi_valor = "---"
                else:
                    pi_valor = round(valor2.valor)

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
                    'diversidad_estructural': {'valor': de_valor}
                },
                'senectud': {
                    'valor': sn_valor,
                    'arb_tam_excep': {'valor': ae_valor},
                    'abund_mad_muerta': {'valor': mp_valor},
                    'prop_madera_muerta': {'valor': pi_valor}
                }
            }
        }

        return rodal_referencia

'''


@api_view(['GET'])
def valorRodalParcelaIFN(request):

    cordRod = request.query_params.get('vr', None)
    habSel = request.query_params.get('idHab', None)
    comAut = request.query_params.get('comAut', None)
    regBiogeo = request.query_params.get('regBiogeo', None)
    comAutComp = request.query_params.get('comAutComp', None)
    regBiogeoComp = request.query_params.get('regBiogeoComp', None)

    ab_parIFN = {}
    cp_parIFN = {}
    ea_parIFN = {}
    ce_parIFN = {}
    de_parIFN = {}
    ae_parIFN = {}
    mp_parIFN = {}
    pi_parIFN = {}
    nm_parIFN = {}
    sn_parIFN = {}

    ab_rod = {}
    cp_rod = {}
    ea_rod = {}
    ce_rod = {}
    de_rod = {}
    ae_rod = {}
    mp_rod = {}
    pi_rod = {}
    nm_rod = {}
    sn_rod = {}

    ab_parIFN_2_val = []
    ea_parIFN_2_val = []
    de_parIFN_2_val = []
    ae_parIFN_2_val = []
    mp_parIFN_2_val = []
    pi_parIFN_2_val = []


    if cordRod == None:
        context = {}

    if cordRod != None:

        if comAutComp != None and regBiogeoComp != None:
            parIFN = Parcelaifn3Valorres.objects.filter(lpeht_cod=habSel).filter(comautonom_cod=comAutComp).filter(regbio_cod=regBiogeoComp).values('valor', 'indicador_cod').annotate(total=Count('valor')).order_by('indicador_cod')
            parIFN_2 = Parcelaifn3Valorres.objects.filter(lpeht_cod=habSel).filter(comautonom_cod=comAutComp).filter(regbio_cod=regBiogeoComp).values('dato', 'indicador_cod').order_by('indicador_cod', '-dato')
            #parIFN_2 = Parcelaifn3Valorres.objects.filter(lpeht_cod=habSel).filter(comautonom_cod=comAutComp).filter(regbio_cod=regBiogeoComp).values('dato', 'indicador_cod').aggregate(Max('dato'))
        elif comAutComp != None and regBiogeoComp == None:
            parIFN = Parcelaifn3Valorres.objects.filter(lpeht_cod=habSel).filter(comautonom_cod=comAutComp).values('valor', 'indicador_cod').annotate(total=Count('valor')).order_by('indicador_cod')
            parIFN_2 = Parcelaifn3Valorres.objects.filter(lpeht_cod=habSel).filter(comautonom_cod=comAutComp).values('dato', 'indicador_cod').order_by('indicador_cod', '-dato')
        elif comAutComp == None and regBiogeoComp != None:
            parIFN = Parcelaifn3Valorres.objects.filter(lpeht_cod=habSel).filter(regbio_cod=regBiogeoComp).values('valor', 'indicador_cod').annotate(total=Count('valor')).order_by('indicador_cod')
            parIFN_2 = Parcelaifn3Valorres.objects.filter(lpeht_cod=habSel).filter(regbio_cod=regBiogeoComp).values('dato', 'indicador_cod').order_by('indicador_cod', '-dato')
        elif comAutComp == None and regBiogeoComp == None:
            parIFN = Parcelaifn3Valorres.objects.filter(lpeht_cod=habSel).values('valor', 'indicador_cod').annotate(total=Count('valor')).order_by('indicador_cod')
            parIFN_2 = Parcelaifn3Valorres.objects.filter(lpeht_cod=habSel).values('dato', 'indicador_cod').order_by('indicador_cod', '-dato')
            parIFN_2_TEST = Parcelaifn3Valorres.objects.filter(lpeht_cod=habSel).values('dato', 'indicador_cod').annotate(total=Count('dato')).order_by('indicador_cod', '-dato')



        '''if comAut != None and regBiogeo != None:
            rod = RodalValorres.objects.filter(id=cordRod).filter(comautonom_cod=comAut).filter(regbio_cod=regBiogeo).values('valor', 'indicador_cod').annotate(total=Count('valor')).order_by('indicador_cod')
        elif comAut != None and regBiogeo == None:
            rod = RodalValorres.objects.filter(id=cordRod).filter(comautonom_cod=comAut).values('valor', 'indicador_cod').annotate(total=Count('valor')).order_by('indicador_cod')
        elif comAut == None and regBiogeo != None:
            rod = RodalValorres.objects.filter(id=cordRod).filter(regbio_cod=regBiogeo).values('valor', 'indicador_cod').annotate(total=Count('valor')).order_by('indicador_cod')
        elif comAut == None and regBiogeo == None:
            rod = RodalValorres.objects.filter(id=cordRod).values('valor', 'indicador_cod').annotate(total=Count('valor')).order_by('indicador_cod')'''

        if comAut != None and regBiogeo != None:
            #rod = RodalValorres2.objects.filter(id_rodal=cordRod).filter(comautonom_cod=comAut).filter(regbio_cod=regBiogeo).values('valor', 'indicador_cod').annotate(total=Count('valor')).order_by('indicador_cod')
            rod = RodalValorres.objects.filter(id=cordRod).filter(comautonom_cod=comAut).filter(regbio_cod=regBiogeo).values('valor', 'indicador_cod', 'dato').annotate(total=Count('valor')).order_by('indicador_cod')
            #rod = RodalValorres.objects.filter(id=cordRod).filter(comautonom_cod=comAut).filter(regbio_cod=regBiogeo).values('valor', 'indicador_cod', 'dato')
            rodName = Rodal.objects.filter(id=cordRod).filter(comautonom_cod=comAut).filter(regbio_cod=regBiogeo).values('nombre')
        elif comAut != None and regBiogeo == None:
            #rod = RodalValorres2.objects.filter(id_rodal=cordRod).filter(comautonom_cod=comAut).values('valor','indicador_cod').annotate(total=Count('valor')).order_by('indicador_cod')
            rod = RodalValorres.objects.filter(id=cordRod).filter(comautonom_cod=comAut).values('valor', 'indicador_cod', 'dato').annotate(total=Count('valor')).order_by('indicador_cod')
            #rod = RodalValorres.objects.filter(id=cordRod).filter(comautonom_cod=comAut).values('valor','indicador_cod', 'dato')
            rodName = Rodal.objects.filter(id=cordRod).filter(comautonom_cod=comAut).values('nombre')
        elif comAut == None and regBiogeo != None:
            #rod = RodalValorres2.objects.filter(id_rodal=cordRod).filter(regbio_cod=regBiogeo).values('valor', 'indicador_cod').annotate(total=Count('valor')).order_by('indicador_cod')
            rod = RodalValorres.objects.filter(id=cordRod).filter(regbio_cod=regBiogeo).values('valor', 'indicador_cod', 'dato').annotate(total=Count('valor')).order_by('indicador_cod')
            #rod = RodalValorres.objects.filter(id=cordRod).filter(regbio_cod=regBiogeo).values('valor','indicador_cod', 'dato')
            rodName = Rodal.objects.filter(id=cordRod).filter(regbio_cod=regBiogeo).values('nombre')
        elif comAut == None and regBiogeo == None:
            #rod = RodalValorres2.objects.filter(id_rodal=cordRod).values('valor', 'indicador_cod').annotate(total=Count('valor')).order_by('indicador_cod')
            rod = RodalValorres.objects.filter(id=cordRod).values('valor', 'indicador_cod', 'dato').annotate(total=Count('valor')).order_by('indicador_cod')
            #rod = RodalValorres.objects.filter(id=cordRod).values('valor', 'indicador_cod', 'dato')
            rodName = Rodal.objects.filter(id=cordRod).values('nombre')



        for n in rodName:
            nombreRodal = n['nombre']


        for p in parIFN:
            if p['indicador_cod'] == 'ab':
                val = p['valor']
                ab_parIFN[val] = p['total']
            elif p['indicador_cod'] == 'cp':
                val = p['valor']
                cp_parIFN[val] = p['total']
            elif p['indicador_cod'] == 'ea':
                val = p['valor']
                ea_parIFN[val] = p['total']
            elif p['indicador_cod'] == 'ce':
                val = p['valor']
                ce_parIFN[val] = p['total']
            elif p['indicador_cod'] == 'de':
                val = p['valor']
                de_parIFN[val] = p['total']
            elif p['indicador_cod'] == 'ae':
                val = p['valor']
                ae_parIFN[val] = p['total']
            elif p['indicador_cod'] == 'mp':
                val = p['valor']
                mp_parIFN[val] = p['total']
            elif p['indicador_cod'] == 'pi':
                val = p['valor']
                pi_parIFN[val] = p['total']
            elif p['indicador_cod'] == 'nm':
                val = p['valor']
                nm_parIFN[val] = p['total']
            elif p['indicador_cod'] == 'sn':
                val = p['valor']
                sn_parIFN[val] = p['total']

        for r in rod:
            if r['indicador_cod'] == 'ab':
                val = r['valor']
                ab_rod[val] = r['total']
            elif r['indicador_cod'] == 'cp':
                val = r['valor']
                cp_rod[val] = r['total']
            elif r['indicador_cod'] == 'ea':
                val = r['valor']
                ea_rod[val] = r['total']
            elif r['indicador_cod'] == 'ce':
                val = r['valor']
                ce_rod[val] = r['total']
            elif r['indicador_cod'] == 'de':
                val = r['valor']
                de_rod[val] = r['total']
            elif r['indicador_cod'] == 'ae':
                val = r['valor']
                ae_rod[val] = r['total']
            elif r['indicador_cod'] == 'mp':
                val = r['valor']
                mp_rod[val] = r['total']
            elif r['indicador_cod'] == 'pi':
                val = r['valor']
                pi_rod[val] = r['total']
            elif r['indicador_cod'] == 'nm':
                val = r['valor']
                nm_rod[val] = r['total']
            elif r['indicador_cod'] == 'sn':
                val = r['valor']
                sn_rod[val] = r['total']

        data = []

        cp = {'ind': 'cp', 'ifn': cp_parIFN, 'rod': cp_rod, 'cordText': _('CP_cord')}
        ea = {'ind': 'ea', 'ifn': ea_parIFN, 'rod': ea_rod, 'cordText': _('EA_cord')}
        ce = {'ind': 'ce', 'ifn': ce_parIFN, 'rod': ce_rod, 'cordText': _('CE_cord')}
        ab = {'ind': 'ab', 'ifn': ab_parIFN, 'rod': ab_rod, 'cordText': _('AB_cord')}
        de = {'ind': 'de', 'ifn': de_parIFN, 'rod': de_rod, 'cordText': _('DE_cord')}
        ae = {'ind': 'ae', 'ifn': ae_parIFN, 'rod': ae_rod, 'cordText': _('AE_cord')}
        mp = {'ind': 'mp', 'ifn': mp_parIFN, 'rod': mp_rod, 'cordText': _('MP_cord')}
        pi = {'ind': 'pi', 'ifn': pi_parIFN, 'rod': pi_rod, 'cordText': _('PI_cord')}
        nm = {'ind': 'nm', 'ifn': nm_parIFN, 'rod': nm_rod, 'cordText': _('NM_cord')}
        sn = {'ind': 'sn', 'ifn': sn_parIFN, 'rod': sn_rod, 'cordText': _('SN_cord')}

        data.append({"cp": cp})
        data.append({"ea": ea})
        data.append({"ce": ce})
        data.append({"ab": ab})
        data.append({"de": de})
        data.append({"ae": ae})
        data.append({"mp": mp})
        data.append({"pi": pi})
        data.append({"nm": nm})
        data.append({"sn": sn})

        valoresMetricos = calcValMetIFN(parIFN_2, rod)

    context = {'data': data, 'valoresMetricos': valoresMetricos, 'nombreRodal': nombreRodal}
    return Response(context)


def calcValMetIFN(parIFN_2, rod):
    ab_parIFN_2 = []
    ea_parIFN_2 = []
    de_parIFN_2 = []
    ae_parIFN_2 = []
    mp_parIFN_2 = []
    pi_parIFN_2 = []

    ab_rod_2 = {}
    ea_rod_2 = {}
    de_rod_2 = {}
    ae_rod_2 = {}
    mp_rod_2 = {}
    pi_rod_2 = {}

    nullValues = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

    for p in parIFN_2:
        if p['indicador_cod'] == 'ab':
            ab_parIFN_2.append(p['dato'])
        elif p['indicador_cod'] == 'ea':
            ea_parIFN_2.append(p['dato'])
        elif p['indicador_cod'] == 'de':
            de_parIFN_2.append(p['dato'])
        elif p['indicador_cod'] == 'ae':
            ae_parIFN_2.append(p['dato'])
        elif p['indicador_cod'] == 'mp':
            mp_parIFN_2.append(p['dato'])
        elif p['indicador_cod'] == 'pi':
            pi_parIFN_2.append(p['dato'])

    for r in rod:
        if r['indicador_cod'] == 'ab':
            val = r['dato']
            #ab_rod_2[val] = r['total']
            ab_rod_2[0] = val
        elif r['indicador_cod'] == 'ea':
            val = r['dato']
            #ea_rod_2[val] = r['total']
            ea_rod_2[0] = val
        elif r['indicador_cod'] == 'de':
            val = r['dato']
            #de_rod_2[val] = r['total']
            de_rod_2[0] = val
        elif r['indicador_cod'] == 'ae':
            val = r['dato']
            #ae_rod_2[val] = r['total']
            ae_rod_2[0] = val
        elif r['indicador_cod'] == 'mp':
            val = r['dato']
            #mp_rod_2[val] = r['total']
            mp_rod_2[0] = val
        elif r['indicador_cod'] == 'pi':
            val = r['dato']
            #pi_rod_2[val] = r['total']
            pi_rod_2[0] = val

    ab = {'ind': 'ab', 'ifn': ab_parIFN_2}
    ea = {'ind': 'ea', 'ifn': ea_parIFN_2}
    de = {'ind': 'de', 'ifn': de_parIFN_2}
    ae = {'ind': 'ae', 'ifn': ae_parIFN_2}
    mp = {'ind': 'mp', 'ifn': mp_parIFN_2}
    pi = {'ind': 'pi', 'ifn': pi_parIFN_2}

    if ab['ifn'][0] == 0 or ab['ifn'][0] is None:
        abInterv = nullValues
        abValoresMetricos = []
        array_length = len(abInterv)
        for t in range(array_length):
            abValoresMetricos.append({str(abInterv[t]): 0})
    elif ab['ifn'][0] > 0:
        valGran = ab['ifn'][0]
        abInterv = calcInterv(valGran)
        abValoresMetricos = clasValMetricos(abInterv, ab_parIFN_2)


    if ea['ifn'][0] == 0 or ea['ifn'][0] is None:
        eaInterv = nullValues
        eaValoresMetricos = []
        array_length = len(eaInterv)
        for t in range(array_length):
            eaValoresMetricos.append({str(eaInterv[t]): 0})
    elif ea['ifn'][0] > 0:
        valGran = ea['ifn'][0]
        eaInterv = calcInterv(valGran)
        eaValoresMetricos = clasValMetricos(eaInterv, ea_parIFN_2)

    if de['ifn'][0] == 0 or de['ifn'][0] is None:
        deInterv = nullValues
        deValoresMetricos = []
        array_length = len(deInterv)
        for t in range(array_length):
            deValoresMetricos.append({str(deInterv[t]): 0})
    elif de['ifn'][0] > 0:
        valGran = de['ifn'][0]
        deInterv = calcInterv(valGran)
        deValoresMetricos = clasValMetricos(deInterv, de_parIFN_2)

    if ae['ifn'][0] == 0 or ae['ifn'][0] is None:
        aeInterv = nullValues
        aeValoresMetricos = []
        array_length = len(aeInterv)
        for t in range(array_length):
            aeValoresMetricos.append({str(aeInterv[t]): 0})
    elif ae['ifn'][0] > 0:
        valGran = ae['ifn'][0]
        aeInterv = calcInterv(valGran)
        aeValoresMetricos = clasValMetricos(aeInterv, ae_parIFN_2)

    if mp['ifn'][0] == 0 or mp['ifn'][0] is None:
        mpInterv = nullValues
        mpValoresMetricos = []

        array_length = len(mpInterv)
        for t in range(array_length):
            mpValoresMetricos.append({str(mpInterv[t]): 0})
    elif mp['ifn'][0] > 0:
        valGran = mp['ifn'][0]
        mpInterv = calcInterv(valGran)
        mpValoresMetricos = clasValMetricos(mpInterv, mp_parIFN_2)

    if pi['ifn'][0] == 0 or pi['ifn'][0] is None:
        piInterv = nullValues
        piValoresMetricos = []

        array_length = len(piInterv)
        for t in range(array_length):
            piValoresMetricos.append({str(piInterv[t]): 0})
    elif pi['ifn'][0] > 0:
        valGran = pi['ifn'][0]
        piInterv = calcInterv(valGran)
        piValoresMetricos = clasValMetricos(piInterv, pi_parIFN_2)

    data2 = []

    data2.append({'ind': 'ab', "interv": abInterv, "valores": abValoresMetricos, "rodalValue": ab_rod_2, "intervEje": abInterv[0]['intervEje'], 'cordText': _('AB_met_cord')})
    data2.append({'ind': 'ea', "interv": eaInterv, "valores": eaValoresMetricos, "rodalValue": ea_rod_2, "intervEje": eaInterv[0]['intervEje'], 'cordText': _('EA_met_cord')})
    data2.append({'ind': 'de', "interv": deInterv, "valores": deValoresMetricos, "rodalValue": de_rod_2, "intervEje": deInterv[0]['intervEje'], 'cordText': _('DE_met_cord')})
    data2.append({'ind': 'ae', "interv": aeInterv, "valores": aeValoresMetricos, "rodalValue": ae_rod_2, "intervEje": aeInterv[0]['intervEje'], 'cordText': _('AE_met_cord')})
    data2.append({'ind': 'mp', "interv": mpInterv, "valores": mpValoresMetricos, "rodalValue": mp_rod_2, "intervEje": mpInterv[0]['intervEje'], 'cordText': _('MP_met_cord')})
    data2.append({'ind': 'pi', "interv": piInterv, "valores": piValoresMetricos, "rodalValue": pi_rod_2, "intervEje": piInterv[0]['intervEje'], 'cordText': _('PI_met_cord')})

    return data2


def calcInterv(valGran):
    inte = numpy.linspace(start=0, stop=valGran, num=12)
    interv = [[inte[0], inte[1]], [inte[1], inte[2]], [inte[2], inte[3]],
              [inte[3], inte[4]], [inte[4], inte[5]], [inte[5], inte[6]],
              [inte[6], inte[7]], [inte[7], inte[8]], [inte[8], inte[9]],
              [inte[9], inte[10]], [inte[10], inte[11]]]

    intervEje = [
        [round((interv[0][0] + interv[0][1])/2, 1)],
        [round((interv[1][0] + interv[1][1])/2, 1)],
        [round((interv[2][0] + interv[2][1])/2, 1)],
        [round((interv[3][0] + interv[3][1])/2, 1)],
        [round((interv[4][0] + interv[4][1])/2, 1)],
        [round((interv[5][0] + interv[5][1])/2, 1)],
        [round((interv[6][0] + interv[6][1])/2, 1)],
        [round((interv[7][0] + interv[7][1])/2, 1)],
        [round((interv[8][0] + interv[8][1])/2, 1)],
        [round((interv[9][0] + interv[9][1])/2, 1)],
        [round((interv[10][0] + interv[10][1])/2, 1)],
    ]

    intervalos = []
    intervalos.append({'interv': interv, 'intervEje': intervEje})

    return intervalos

def clasValMetricos(interv, valores):
    int_0 = 0
    int_1 = 0
    int_2 = 0
    int_3 = 0
    int_4 = 0
    int_5 = 0
    int_6 = 0
    int_7 = 0
    int_8 = 0
    int_9 = 0
    int_10 = 0

    for p in valores:
        if p >= interv[0]['interv'][0][0] and p < interv[0]['interv'][0][1]:
            int_0 += 1
        elif p >= interv[0]['interv'][1][0] and p < interv[0]['interv'][1][1]:
            int_1 += 1
        elif p >= interv[0]['interv'][2][0] and p < interv[0]['interv'][2][1]:
            int_2 += 1
        elif p >= interv[0]['interv'][3][0] and p < interv[0]['interv'][3][1]:
            int_3 += 1
        elif p >= interv[0]['interv'][4][0] and p < interv[0]['interv'][4][1]:
            int_4 += 1
        elif p >= interv[0]['interv'][5][0] and p < interv[0]['interv'][5][1]:
            int_5 += 1
        elif p >= interv[0]['interv'][6][0] and p < interv[0]['interv'][6][1]:
            int_6 += 1
        elif p >= interv[0]['interv'][7][0] and p < interv[0]['interv'][7][1]:
            int_7 += 1
        elif p >= interv[0]['interv'][8][0] and p < interv[0]['interv'][8][1]:
            int_8 += 1
        elif p >= interv[0]['interv'][9][0] and p < interv[0]['interv'][9][1]:
            int_9 += 1
        elif p >= interv[0]['interv'][10][0] and p <= interv[0]['interv'][10][1]:
            int_10 += 1

    valMetPar = []
    #valMetPar.append({str(interv[0]): int_0, str(interv[1]): int_1, str(interv[2]): int_2, str(interv[3]): int_3, str(interv[4]): int_4, str(interv[5]): int_5, str(interv[6]): int_6, str(interv[7]): int_7, str(interv[8]): int_8, str(interv[9]): int_9, str(interv[10]): int_10})
    #valMetPar.append({'0': int_0, '1': int_1, '2': int_2, '3': int_3, '4': int_4, '5': int_5, '6': int_6, '7': int_7, '8': int_8, '9': int_9, '10': int_10})
    valMetPar.append(int_0)
    valMetPar.append(int_1)
    valMetPar.append(int_2)
    valMetPar.append(int_3)
    valMetPar.append(int_4)
    valMetPar.append(int_5)
    valMetPar.append(int_6)
    valMetPar.append(int_7)
    valMetPar.append(int_8)
    valMetPar.append(int_9)
    valMetPar.append(int_10)

    return valMetPar

def herramRedbosques(request):
    return render(request, 'redbosques_main/herramRedbosques.html')

def evaluacionNaturalidad(request):
    return render(request, 'redbosques_main/evaluacionNat.html')