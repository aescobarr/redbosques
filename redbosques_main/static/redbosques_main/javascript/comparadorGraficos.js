$(document).ready(function() {
    graficaScatterDefault();
    graficaBarrasDefault();
    blockSelectores();
});

var dataGraph2;
var datosEjesGraph2 = {};
var dotsGraphData = [];
var barCharData = [];
var barData = [];
var g1EjeYSelectedPoints = [];
var g1EjeXSelectedPoints = [];
var g2EjeYSelectedPoints;
var g2EjeXSelectedPoints;
var g3EjeYSelectedPoints;
var g3EjeXSelectedPoints;

var rodalX1 = null;
var rodalReferenciaX1 = null;
var rodalY1 = null;
var rodalReferenciaY1 = null;

var rodalX2 = null;
var rodalReferenciaX2 = null;
var rodalY2 = null;
var rodalReferenciaY2 = null;

var rodalX3 = null;
var rodalReferenciaX3 = null;
var rodalY3 = null;
var rodalReferenciaY3 = null;

var rodalXY1 = null;
var rodalReferenciaXY1 = null;
var rodalXY2 = null;
var rodalReferenciaXY2 = null;
var rodalXY3 = null;
var rodalReferenciaXY3 = null;
var grafico;
var coordenadasPuntos;
var valoresBarrasEjes;
var valoresBarrasCrite;

var rodNombres = [];
var rodValores = [];
var rodVal = [];
var valores = [];
var rodalName = [];
var rodalNameRef = [];

var desv = [];
var desvNeg = [];
var desvPos = [];



var dataGraphEixosCrite = function(valoresRodal, valoresRodalComp, rodalName, rodalNameRef){



    var datosEjes = {
        "0": { "ref": "naturalidad",
                "valorRodal": valoresRodal.naturalidad.valor,
                "valorRodalComp": valoresRodalComp.naturalidad.valor,
                "desv": valoresRodalComp.naturalidad.valor_desv },
        "1": { "ref": "huellaHumana",
                "valorRodal": valoresRodal.huellaHumana.valor,
                "valorRodalComp": valoresRodalComp.huellaHumana.valor,
                "desv": valoresRodalComp.huellaHumana.valor_desv },
        "2": { "ref": "integridadEspacial",
                "valorRodal": valoresRodal.integridadEspacial.valor,
                "valorRodalComp": valoresRodalComp.integridadEspacial.valor,
                "desv": valoresRodalComp.integridadEspacial.valor_desv },
    }



    var datosCritNat = {
        "0": { "ref": "composicion",
                "valorRodal": valoresRodal.naturalidad.composicion.valor,
                "valorRodalComp": valoresRodalComp.naturalidad.composicion.valor,
                "desv": valoresRodalComp.naturalidad.composicion.valor_desv },
        "1": { "ref": "complejidad",
                "valorRodal": valoresRodal.naturalidad.complejidad.valor,
                "valorRodalComp": valoresRodalComp.naturalidad.complejidad.valor,
                "desv": valoresRodalComp.naturalidad.complejidad.valor_desv },

        "2": { "ref": "senectud",
                "valorRodal": valoresRodal.naturalidad.senectud.valor,
                "valorRodalComp": valoresRodalComp.naturalidad.senectud.valor,
                "desv": valoresRodalComp.naturalidad.senectud.valor_desv },

        "3": { "ref": "micro_habitats",
                "valorRodal": valoresRodal.naturalidad.micro_habitats.valor,
                "valorRodalComp": valoresRodalComp.naturalidad.micro_habitats.valor,
                "desv": valoresRodalComp.naturalidad.micro_habitats.valor_desv },
        "4": { "ref": "dinamica",
                "valorRodal": valoresRodal.naturalidad.dinamica.valor,
                "valorRodalComp": valoresRodalComp.naturalidad.dinamica.valor,
                "desv": valoresRodalComp.naturalidad.dinamica.valor_desv },

    }



    var datosCritHu = {
        "0": { "ref": "antigua",
                "valorRodal": valoresRodal.huellaHumana.antigua.valor,
                "valorRodalComp": valoresRodalComp.huellaHumana.antigua.valor,
                "desv": valoresRodalComp.huellaHumana.antigua.valor_desv },

        "1": { "ref": "reciente",
                "valorRodal": valoresRodal.huellaHumana.reciente.valor,
                "valorRodalComp": valoresRodalComp.huellaHumana.reciente.valor,
                "desv": valoresRodalComp.huellaHumana.reciente.valor_desv },
    }




    var datosCritIe = {
        "0": { "ref": "tamano",
                "valorRodal": valoresRodal.integridadEspacial.tamano.valor,
                "valorRodalComp": valoresRodalComp.integridadEspacial.tamano.valor,
                "desv": valoresRodalComp.integridadEspacial.tamano.valor_desv },
        "1": { "ref": "cont_forest",
                "valorRodal": valoresRodal.integridadEspacial.cont_forest.valor,
                "valorRodalComp": valoresRodalComp.integridadEspacial.cont_forest.valor,
                "desv": valoresRodalComp.integridadEspacial.cont_forest.valor_desv },
        "2": { "ref": "efect_borde",
                "valorRodal": valoresRodal.integridadEspacial.efect_borde.valor,
                "valorRodalComp": valoresRodalComp.integridadEspacial.efect_borde.valor,
                "desv": valoresRodalComp.integridadEspacial.efect_borde.valor_desv },
        "3": { "ref": "conect",
                "valorRodal": valoresRodal.integridadEspacial.conect.valor,
                "valorRodalComp": valoresRodalComp.integridadEspacial.conect.valor,
                "desv": valoresRodalComp.integridadEspacial.conect.valor_desv },
    }



    graficaEjes(datosEjes, rodalName, rodalNameRef);
    graficaCritNat(datosCritNat, rodalName, rodalNameRef);
    graficaCritHu(datosCritHu, rodalName, rodalNameRef);
    graficaCritIe(datosCritIe, rodalName, rodalNameRef);



}

function dataScatterGraph(rodalPuntosData, rodalRefPuntosData){

    dotsGraphData = []

    nmRodal = []
    ieRodal = []
    hhRodal = []

    nmRodalRef = []
    ieRodalRef = []
    hhRodalRef = []

    rodalPuntos = []
    rodalReferenciaPuntos = []


    for(z=0; z<=rodalRefPuntosData.length; z++){
        if(rodalRefPuntosData[i]){
            if(rodalPuntosData[0].id_rodal == rodalRefPuntosData[i].id_rodal){
                rodalRefPuntosData.splice(i,1);

            }
        }
    }


    for(i=0; i<rodalPuntosData.length; i++){
        if(rodalPuntosData[i].indicador_cod == 'nm'){
            NM = {
                "rodal": {
                    "eje": rodalPuntosData[i].indicador_cod,
                    "id_rodal": rodalPuntosData[i].id_rodal,
                    "name": rodalPuntosData[i].nombre,
                    "valor": rodalPuntosData[i].valor
                }
            }
            nmRodal.push(NM);
        }else if(rodalPuntosData[i].indicador_cod == 'ie'){
            IE = {
                "rodal": {
                    "eje" :rodalPuntosData[i].indicador_cod,
                    "id_rodal": rodalPuntosData[i].id_rodal,
                    "name": rodalPuntosData[i].nombre,
                    "valor": rodalPuntosData[i].valor
                }
            }
            ieRodal.push(IE);
        }else if(rodalPuntosData[i].indicador_cod == 'hh'){
            HH = {
                "rodal": {
                    "eje" :rodalPuntosData[i].indicador_cod,
                    "id_rodal": rodalPuntosData[i].id_rodal,
                    "name": rodalPuntosData[i].nombre,
                    "valor": rodalPuntosData[i].valor
                }
            }
            hhRodal.push(HH);
        }

    }

    rodalPuntos.push(nmRodal,ieRodal,hhRodal)

    for(i=0; i<rodalRefPuntosData.length; i++){
        if(rodalRefPuntosData[i].indicador_cod == 'nm'){
            NM = {
                "rodal": {
                    "eje": rodalRefPuntosData[i].indicador_cod,
                    "id_rodal": rodalRefPuntosData[i].id_rodal,
                    "name": rodalRefPuntosData[i].nombre,
                    "valor": rodalRefPuntosData[i].valor
                }
            }
            nmRodalRef.push(NM);
        }else if(rodalRefPuntosData[i].indicador_cod == 'ie'){
            IE = {
                "rodal": {
                    "eje" :rodalRefPuntosData[i].indicador_cod,
                    "id_rodal": rodalRefPuntosData[i].id_rodal,
                    "name": rodalRefPuntosData[i].nombre,
                    "valor": rodalRefPuntosData[i].valor
                }
            }
            ieRodalRef.push(IE);
        }else if(rodalRefPuntosData[i].indicador_cod == 'hh'){
            HH = {
                "rodal": {
                    "eje" :rodalRefPuntosData[i].indicador_cod,
                    "id_rodal": rodalRefPuntosData[i].id_rodal,
                    "name": rodalRefPuntosData[i].nombre,
                    "valor": rodalRefPuntosData[i].valor
                }
            }
            hhRodalRef.push(HH);
        }

    }

    rodalReferenciaPuntos.push(nmRodalRef,ieRodalRef,hhRodalRef);
    dotsGraphData.push(rodalPuntos, rodalReferenciaPuntos);

    return dotsGraphData;
}

function dataChartCrite(rodalChart, rodalRefChart){

    var arRodal = [];
    var ceRodal = [];
    var cfRodal = [];
    var cnRodal = [];
    var cpRodal = [];
    var dnRodal = [];
    var ebRodal = [];
    var haRodal = [];
    var hmRodal = [];
    var hrRodal = [];
    var snRodal = [];
    var nmRodal = [];
    var hhRodal = [];
    var ieRodal = [];
    var rodalBarras = [];
    var arRefRodal = [];
    var ceRefRodal = [];
    var cfRefRodal = [];
    var cnRefRodal = [];
    var cpRefRodal = [];
    var dnRefRodal = [];
    var ebRefRodal = [];
    var haRefRodal = [];
    var hmRefRodal = [];
    var hrRefRodal = [];
    var snRefRodal = [];
    var nmRefRodal = [];
    var hhRefRodal = [];
    var ieRefRodal = [];
    var rodalRefBarras = [];
    barCharData = [];

    for(i=0; i<rodalChart.length; i++){
        if(rodalChart[i].indicador_cod == 'ar'){
            AR = {
                "rodal": {
                    "eje": rodalChart[i].indicador_cod,
                    "id_rodal": rodalChart[i].id_rodal,
                    "name": rodalChart[i].nombre,
                    "y": rodalChart[i].valor,
                    "color": "#339933"
                }
            }
            arRodal.push(AR);
        }else if(rodalChart[i].indicador_cod == 'ce'){
            CE = {
                "rodal": {
                    "eje" :rodalChart[i].indicador_cod,
                    "id_rodal": rodalChart[i].id_rodal,
                    "name": rodalChart[i].nombre,
                    "y": rodalChart[i].valor,
                    "color": "#339933"

                }
            }
            ceRodal.push(CE);
        }else if(rodalChart[i].indicador_cod == 'cf'){
            CF = {
                "rodal": {
                    "eje" :rodalChart[i].indicador_cod,
                    "id_rodal": rodalChart[i].id_rodal,
                    "name": rodalChart[i].nombre,
                    "y": rodalChart[i].valor,
                    "color": "#339933"
                }
            }
            cfRodal.push(CF);
        }else if(rodalChart[i].indicador_cod == 'cn'){
            CN = {
                "rodal": {
                    "eje" :rodalChart[i].indicador_cod,
                    "id_rodal": rodalChart[i].id_rodal,
                    "name": rodalChart[i].nombre,
                    "y": rodalChart[i].valor,
                    "color": "#339933"
                }
            }
            cnRodal.push(CN);
        }else if(rodalChart[i].indicador_cod == 'cp'){
            CP = {
                "rodal": {
                    "eje" :rodalChart[i].indicador_cod,
                    "id_rodal": rodalChart[i].id_rodal,
                    "name": rodalChart[i].nombre,
                    "y": rodalChart[i].valor,
                    "color": "#339933"
                }
            }
            cpRodal.push(CP);
        }else if(rodalChart[i].indicador_cod == 'dn'){
            DN = {
                "rodal": {
                    "eje" :rodalChart[i].indicador_cod,
                    "id_rodal": rodalChart[i].id_rodal,
                    "name": rodalChart[i].nombre,
                    "y": rodalChart[i].valor,
                    "color": "#339933"
                }
            }
            dnRodal.push(DN);
        }else if(rodalChart[i].indicador_cod == 'eb'){
            EB = {
                "rodal": {
                    "eje" :rodalChart[i].indicador_cod,
                    "id_rodal": rodalChart[i].id_rodal,
                    "name": rodalChart[i].nombre,
                    "y": rodalChart[i].valor,
                    "color": "#339933"
                }
            }
            ebRodal.push(EB);
        }else if(rodalChart[i].indicador_cod == 'ha'){
            HA = {
                "rodal": {
                    "eje" :rodalChart[i].indicador_cod,
                    "id_rodal": rodalChart[i].id_rodal,
                    "name": rodalChart[i].nombre,
                    "y": rodalChart[i].valor,
                    "color": "#339933"
                }
            }
            haRodal.push(HA);
        }else if(rodalChart[i].indicador_cod == 'hm'){
            HM = {
                "rodal": {
                    "eje" :rodalChart[i].indicador_cod,
                    "id_rodal": rodalChart[i].id_rodal,
                    "name": rodalChart[i].nombre,
                    "y": rodalChart[i].valor,
                    "color": "#339933"
                }
            }
            hmRodal.push(HM);
        }else if(rodalChart[i].indicador_cod == 'hr'){
            HR = {
                "rodal": {
                    "eje" :rodalChart[i].indicador_cod,
                    "id_rodal": rodalChart[i].id_rodal,
                    "name": rodalChart[i].nombre,
                    "y": rodalChart[i].valor,
                    "color": "#339933"
                }
            }
            hrRodal.push(HR);
        }else if(rodalChart[i].indicador_cod == 'sn'){
            SN = {
                "rodal": {
                    "eje" :rodalChart[i].indicador_cod,
                    "id_rodal": rodalChart[i].id_rodal,
                    "name": rodalChart[i].nombre,
                    "y": rodalChart[i].valor,
                    "color": "#339933"
                }
            }
            snRodal.push(SN);
        }else if(rodalChart[i].indicador_cod == 'hh'){
            HH = {
                "rodal": {
                    "eje" :rodalChart[i].indicador_cod,
                    "id_rodal": rodalChart[i].id_rodal,
                    "name": rodalChart[i].nombre,
                    "y": rodalChart[i].valor,
                    "color": "#339933"
                }
            }
            hhRodal.push(HH);
        }else if(rodalChart[i].indicador_cod == 'ie'){
            IE = {
                "rodal": {
                    "eje" :rodalChart[i].indicador_cod,
                    "id_rodal": rodalChart[i].id_rodal,
                    "name": rodalChart[i].nombre,
                    "y": rodalChart[i].valor,
                    "color": "#339933"
                }
            }
            ieRodal.push(IE);
        }else if(rodalChart[i].indicador_cod == 'nm'){
            NM = {
                "rodal": {
                    "eje" :rodalChart[i].indicador_cod,
                    "id_rodal": rodalChart[i].id_rodal,
                    "name": rodalChart[i].nombre,
                    "y": rodalChart[i].valor,
                    "color": "#339933"
                }
            }
            nmRodal.push(NM);
        }


    }
    rodalBarras.push(arRodal,ceRodal, cfRodal, cnRodal, cpRodal, dnRodal,ebRodal, haRodal,hmRodal,hrRodal, snRodal, hhRodal, ieRodal, nmRodal);



    for(i=0; i<rodalRefChart.length; i++){
        if(rodalRefChart[i].indicador_cod == 'ar'){
            AR = {
                "rodal": {
                        "eje": rodalRefChart[i].indicador_cod,
                    "id_rodal": rodalRefChart[i].id_rodal,
                    "name": rodalRefChart[i].nombre,
                    "y": rodalRefChart[i].valor
                }
            }
            arRefRodal.push(AR);
        }else if(rodalRefChart[i].indicador_cod == 'ce'){
            CE = {
                "rodal": {
                    "eje" :rodalRefChart[i].indicador_cod,
                    "id_rodal": rodalRefChart[i].id_rodal,
                    "name": rodalRefChart[i].nombre,
                    "y": rodalRefChart[i].valor
                }
            }
            ceRefRodal.push(CE);
        }else if(rodalRefChart[i].indicador_cod == 'cf'){
            CF = {
                "rodal": {
                    "eje" :rodalRefChart[i].indicador_cod,
                    "id_rodal": rodalRefChart[i].id_rodal,
                    "name": rodalRefChart[i].nombre,
                    "y": rodalRefChart[i].valor
                }
            }
            cfRefRodal.push(CF);
        }else if(rodalRefChart[i].indicador_cod == 'cn'){
            CN = {
                "rodal": {
                    "eje" :rodalRefChart[i].indicador_cod,
                    "id_rodal": rodalRefChart[i].id_rodal,
                    "name": rodalRefChart[i].nombre,
                    "y": rodalRefChart[i].valor
                }
            }
            cnRefRodal.push(CN);
        }else if(rodalRefChart[i].indicador_cod == 'cp'){
            CP = {
                "rodal": {
                    "eje" :rodalRefChart[i].indicador_cod,
                    "id_rodal": rodalRefChart[i].id_rodal,
                    "name": rodalRefChart[i].nombre,
                    "y": rodalRefChart[i].valor
                }
            }
            cpRefRodal.push(CP);
        }else if(rodalRefChart[i].indicador_cod == 'dn'){
            DN = {
                "rodal": {
                    "eje" :rodalRefChart[i].indicador_cod,
                    "id_rodal": rodalRefChart[i].id_rodal,
                    "name": rodalRefChart[i].nombre,
                    "y": rodalRefChart[i].valor
                }
            }
            dnRefRodal.push(DN);
        }else if(rodalRefChart[i].indicador_cod == 'eb'){
            EB = {
                "rodal": {
                    "eje" :rodalRefChart[i].indicador_cod,
                    "id_rodal": rodalRefChart[i].id_rodal,
                    "name": rodalRefChart[i].nombre,
                    "y": rodalRefChart[i].valor
                }
            }
            ebRefRodal.push(EB);
        }else if(rodalRefChart[i].indicador_cod == 'ha'){
            HA = {
                "rodal": {
                    "eje" :rodalRefChart[i].indicador_cod,
                    "id_rodal": rodalRefChart[i].id_rodal,
                    "name": rodalRefChart[i].nombre,
                    "y": rodalRefChart[i].valor
                }
            }
            haRefRodal.push(HA);
        }else if(rodalRefChart[i].indicador_cod == 'hm'){
            HM = {
                "rodal": {
                    "eje" :rodalRefChart[i].indicador_cod,
                    "id_rodal": rodalRefChart[i].id_rodal,
                    "name": rodalRefChart[i].nombre,
                    "y": rodalRefChart[i].valor
                }
            }
            hmRefRodal.push(HM);
        }else if(rodalRefChart[i].indicador_cod == 'hr'){
            HR = {
                "rodal": {
                    "eje" :rodalRefChart[i].indicador_cod,
                    "id_rodal": rodalRefChart[i].id_rodal,
                    "name": rodalRefChart[i].nombre,
                    "y": rodalRefChart[i].valor
                }
            }
            hrRefRodal.push(HR);
        }else if(rodalRefChart[i].indicador_cod == 'sn'){
            SN = {
                "rodal": {
                    "eje" :rodalRefChart[i].indicador_cod,
                    "id_rodal": rodalRefChart[i].id_rodal,
                    "name": rodalRefChart[i].nombre,
                    "y": rodalRefChart[i].valor
                }
            }
            snRefRodal.push(SN);
        }else if(rodalRefChart[i].indicador_cod == 'hh'){
            HH = {
                "rodal": {
                    "eje" :rodalRefChart[i].indicador_cod,
                    "id_rodal": rodalRefChart[i].id_rodal,
                    "name": rodalRefChart[i].nombre,
                    "y": rodalRefChart[i].valor

                }
            }
            hhRefRodal.push(HH);
        }else if(rodalRefChart[i].indicador_cod == 'ie'){
            IE = {
                "rodal": {
                    "eje" :rodalRefChart[i].indicador_cod,
                    "id_rodal": rodalRefChart[i].id_rodal,
                    "name": rodalRefChart[i].nombre,
                    "y": rodalRefChart[i].valor
                }
            }
            ieRefRodal.push(IE);
        }else if(rodalRefChart[i].indicador_cod == 'nm'){
            NM = {
                "rodal": {
                    "eje" :rodalRefChart[i].indicador_cod,
                    "id_rodal": rodalRefChart[i].id_rodal,
                    "name": rodalRefChart[i].nombre,
                    "y": rodalRefChart[i].valor
                }
            }
            nmRefRodal.push(NM);
        }
    }
    rodalRefBarras.push(arRefRodal,ceRefRodal, cfRefRodal, cnRefRodal, cpRefRodal, dnRefRodal,ebRefRodal, haRefRodal,hmRefRodal,hrRefRodal, snRefRodal, hhRefRodal, ieRefRodal, nmRefRodal)



    barCharData.push(rodalBarras, rodalRefBarras);

    return barCharData;
}

var blockSelectores = function(){
    $('.scatterSelector').attr('disabled', 'disabled');
    $('.barChartselector').attr('disabled', 'disabled');
}

var unblockSelectores = function(){
    $('.scatterSelector').removeAttr('disabled');
    $('.barChartselector').removeAttr('disabled');
}

function rodalData(valorRodal, valRodComp){

    if(valorRodal != 'null'){
        if(valRodComp != 'null'){

            var rodPrincip = valorRodal;
            var idHabitat = $('#habitat').val();
            var idComAut = $('#selector_ComAut_Comp').val();
            var idRegBiogeo = $('#selector_RegBio_Comp').val();
            var valRod = $('#selector_rodales_comp option:selected').val();
            load_rodal_ref(idHabitat, idComAut, idRegBiogeo, valRod, rodPrincip);
        }


        $('.data-table').addClass("asyncload-big");
        var url = '/redbosques/valorRodal';
        url = url + '?vr=' + valorRodal;
        $.ajax({
            url: url,
            method: "GET",
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success: function(data, textStatus, jqXHR) {
                rodalSelData = data.rodal;
                rodalName = data.rodalNombre;
                rodalPuntosData = data.rodalGraficoPuntos;
                rodalChartData = data.rodalChart;

                //graficaScatterDefault();

                if(rodalReferencia){
                    unblockSelectores();
                    //dataGraph(rodalSelData, rodalReferencia);
                    dataGraphEixosCrite(rodalSelData, rodalReferencia, rodalName, rodalNameRef);
                    dataGraph2 = dataScatterGraph(rodalPuntosData, rodalRefPuntosData);
                    dataChartGraph = dataChartCrite(rodalChartData, rodalRefChartData);

                    grafica1();
                    grafica2();
                    grafica3();

                    graficaBarras1();
                    graficaBarras2();

                    g1EjeYSelectedPoints = null;
                    g1EjeXSelectedPoints = null;
                    g2EjeYSelectedPoints = null;
                    g2EjeXSelectedPoints = null;
                    g3EjeYSelectedPoints = null;
                    g3EjeXSelectedPoints = null;
                }else{
                    blockSelectores();
                }

                $('.data-table').removeClass("asyncload-big");

            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
                //$('.data-table').removeClass("asyncload-big");
            }
        });


    }else{
        console.log("borrar datos");
        console.log("limpiar graficos");

    }



};

function load_rodal_ref(idHabitat, idComAut, idRegBiogeo, valRod, rodPrincip){
    url = _rodal_ref_list;


    if(rodPrincip == 'null'){
        console.log("el valor es NULL");

    }else{
        var params = [];
        if(idHabitat != "null"){
            params.push('idHab='+escape(idHabitat));
        }
        if(idComAut != "null"){
            params.push('comAut='+escape(idComAut));
        }
        if(idRegBiogeo != "null"){
            params.push('regBiogeo='+escape(idRegBiogeo));
        }
        if(valRod != "null"){
            params.push('vr='+escape(valRod));
        }
        if(rodPrincip != "null"){
            params.push('rodPrincip='+escape(rodPrincip));
        }

        url = url + "?" + params.join('&');


        if(valRod == "null"){
            resetUITable();
        }else{
            resetUITable();
            //$('.data-table').addClass("asyncload-big");
            $.ajax({
                url: url,
                method: "GET",
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type)) {
                        var csrftoken = getCookie('csrftoken');
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                success: function( data, textStatus, jqXHR ) {
                    rodalNameRef = data.rodalNombre;


                    rodalReferencia = data.rodal_referencia;
                    rodalRefPuntosData = data.rodalRefGraficoPuntos;
                    rodalRefChartData = data.rodalRefChart;
                    recorreArbre('', rodalReferencia);

                    //graficaScatterDefault();
                    //graficaBarrasDefault();

                    if(rodalSelData){
                        if(rodalReferencia != null){
                            //calcDiferencia();
                            unblockSelectores();
                            $('.grafico div').html('');
                            //dataGraph(rodalSelData, rodalReferencia);
                            dataGraphEixosCrite(rodalSelData, rodalReferencia, rodalName, rodalNameRef);
                            dataGraph2 = dataScatterGraph(rodalPuntosData, rodalRefPuntosData);
                            dataChartGraph = dataChartCrite(rodalChartData, rodalRefChartData);

                            grafica1();
                            grafica2();
                            grafica3();
                            graficaBarras1();
                            graficaBarras2();

                            var ejeSelected = $(".scatterSelector").attr('id');
                            var ejeId = "#" + ejeSelected;
                            var ejeOptionSelected = $(ejeId).val();

                            g1EjeYSelectedPoints = null;
                            g1EjeXSelectedPoints = null;
                            g2EjeYSelectedPoints = null;
                            g2EjeXSelectedPoints = null;
                            g3EjeYSelectedPoints = null;
                            g3EjeXSelectedPoints = null;
                        }
                    }else{
                        blockSelectores();
                    }

                },
                error: function(jqXHR, textStatus, errorThrown){
                    console.log(errorThrown);
                    //$('.data-table').removeClass("asyncload-big");
                }
            });
        }
    }
};

function grafica1(){
    var ejeX = "#ejeXGrafica1";
    var ejeY = "#ejeYGrafica1";
    var dotsGraphDataSize = Object.keys(dotsGraphData[1]).length;
    var ejeLeyenda = [];
    var ejesXYNom = {}
    var ejeXSelected = $(ejeX).val();
    var ejeYSelected = $(ejeY).val();

    if(ejeXSelected != "null" && ejeYSelected != "null"){
        rodal = [];
        rodalReferencia = [];
        ejeOptionSelected = [ejeXSelected, ejeYSelected];
        coordenadasPuntos = setPoints(dotsGraphDataSize, ejeOptionSelected);

        rodal = coordenadasPuntos[0];
        rodalReferencia = coordenadasPuntos[1];

        if(rodal != null && rodalReferencia != null ){

            var coordenadas = setCoordenadas(rodal, rodalReferencia);
            rodalCord = coordenadas[0];
            rodalReferenciaCord = coordenadas[1];

            grafico = 'scatter1';
            graficaScatter(rodalCord, rodalReferenciaCord, grafico, ejeXSelected, ejeYSelected);
        }
    }
};

function grafica2(){
    var ejeX = "#ejeXGrafica2";
    var ejeY = "#ejeYGrafica2";
    var dotsGraphDataSize = Object.keys(dotsGraphData[1]).length;
    var ejeLeyenda = [];
    var ejesXYNom = {}
    var ejeXSelected = $(ejeX).val();
    var ejeYSelected = $(ejeY).val();

    if(ejeXSelected != "null" && ejeYSelected != "null"){
        rodal = [];
        rodalReferencia = [];
        ejeOptionSelected = [ejeXSelected, ejeYSelected];
        coordenadasPuntos = setPoints(dotsGraphDataSize, ejeOptionSelected);
        rodal = coordenadasPuntos[0];
        rodalReferencia = coordenadasPuntos[1];

        if(rodal != null && rodalReferencia != null ){
            var coordenadas = setCoordenadas(rodal, rodalReferencia);
            rodalCord = coordenadas[0];
            rodalReferenciaCord = coordenadas[1];
            grafico = 'scatter2';
            graficaScatter(rodalCord, rodalReferenciaCord, grafico, ejeXSelected, ejeYSelected);
        }
    }
};

function grafica3(){
    var ejeX = "#ejeXGrafica3";
    var ejeY = "#ejeYGrafica3";
    var dotsGraphDataSize = Object.keys(dotsGraphData[1]).length;
    var ejeLeyenda = [];
    var ejesXYNom = {}
    var ejeXSelected = $(ejeX).val();
    var ejeYSelected = $(ejeY).val();

    if(ejeXSelected != "null" && ejeYSelected != "null"){
        rodal = [];
        rodalReferencia = [];
        ejeOptionSelected = [ejeXSelected, ejeYSelected];
        coordenadasPuntos = setPoints(dotsGraphDataSize, ejeOptionSelected);
        rodal = coordenadasPuntos[0];
        rodalReferencia = coordenadasPuntos[1];

        if(rodal != null && rodalReferencia != null ){
            var coordenadas = setCoordenadas(rodal, rodalReferencia);
            rodalCord = coordenadas[0];
            rodalReferenciaCord = coordenadas[1];
            grafico = 'scatter3';
            graficaScatter(rodalCord, rodalReferenciaCord, grafico, ejeXSelected, ejeYSelected);
        }
    }
};

function setBars(barGraphDataSize, optionSelected){
    var rodalBarVal = [];
    var rodalRefBarVal = [];
    var barData = [];

    /*Rodal inicial*/
    for (i=0; i<barGraphDataSize; i++){
        if(barCharData[0][i][0]['rodal']['eje'] == optionSelected){
            rodalBarVal.push(barCharData[0][i][0]['rodal']);
        }
    }

    /*Rodal con el que comparamos*/
    for (t=0; t<barGraphDataSize; t++){
        if(barCharData[1][t][0]['rodal']['eje'] == optionSelected){
            rodalRefBarVal.push(barCharData[1][t][0]['rodal']);
        }
    }

    barData.push(rodalBarVal,rodalRefBarVal);

    return barData;
}

function setPoints(dotsGraphDataSize, ejeOptionSelected){
    rodalVal = [];
    var rodalReferenciaValX = [];
    var rodalReferenciaValY = [];
    var rodalNombre = null;
    rodalReferenciaNombres = [];
    var pointsData = [];

    /*Rodal inicial*/
    for (i=0; i<dotsGraphDataSize; i++){
        for (x=0; x<dotsGraphData[0][i].length; x++){
            for (t=0; t<ejeOptionSelected.length; t++){
                if(dotsGraphData[0][i][x]['rodal']['eje'] == ejeOptionSelected[t]){
                    rodalVal.push(dotsGraphData[0][i][x]['rodal']['valor']);
                }
            }
            if(rodalNombre == null){
                rodalNombre = dotsGraphData[0][i][x]['rodal']['name'];
            }
        }
    }

    /*Rodal con el que comparamos*/
    for (i=0; i<dotsGraphDataSize; i++){
        for (x=0; x<dotsGraphData[1][i].length; x++){
            if(dotsGraphData[1][i][x]['rodal']['eje'] == ejeOptionSelected[0]){
                rodalReferenciaValX.push(dotsGraphData[1][i][x]['rodal']);
            }else if(dotsGraphData[1][i][x]['rodal']['eje'] == ejeOptionSelected[1]){
                rodalReferenciaValY.push(dotsGraphData[1][i][x]['rodal']);
            }
        }
    }

    var rodal2 = [];
    var rodalReferencia2 = [];
    var rodSizes = rodalReferenciaValX.length;

    for(z=0; z<rodSizes; z++){
        if(rodalReferenciaValX[z]['id_rodal'] == rodalReferenciaValY[z]['id_rodal']){

            rodalReferencia2[z] = [{
                'id_rodal': rodalReferenciaValX[z]['id_rodal'],
                'name': rodalReferenciaValY[z]['name'],
                'x': rodalReferenciaValX[z]['valor'],
                'y': rodalReferenciaValY[z]['valor'],

            }]
        }

    }

    rodal2 = {
        'name': rodalNombre,
        'val': rodalVal,
        'x': rodalVal[0],
        'y': rodalVal[1],
        'color': '#339933'
    }


    pointsData.push(rodal2, rodalReferencia2);
    return pointsData;
};

function setCoordenadas(rodal, rodalReferencia){
    var rXY = [];
    var rRefXY = [];
    var coordenadasRodales = [];

    rXY = [{
        'name': rodal.name,
        'x': rodal.x,
        'y': rodal.y
    }];

    for(r=0; r<rodalReferencia.length; r++){
        rRefXY[r] = {
            'name': rodalReferencia[r][0]['name'],
            'x': rodalReferencia[r][0]['x'],
            'y': rodalReferencia[r][0]['y']
        }
    }

    coordenadasRodales.push(rXY, rRefXY);
    return coordenadasRodales;
}

var graficaEjes = function(datosEjes, rodalName, rodalNameRef){

    var dataSize = Object.keys(datosEjes).length;
    var datosDesv = [];
    desv = [];
    desvNeg = [];
    desvPos = [];

    for (i=0; i<=dataSize; i++){
        if(datosEjes[i] != null){
            desv = Math.round(datosEjes[i].desv * 100) / 100;
            desvNeg = Math.round((datosEjes[i].valorRodalComp - datosEjes[i].desv) * 100) / 100;
            desvPos = Math.round((datosEjes[i].valorRodalComp + datosEjes[i].desv) * 100) / 100;

            datosDesv[i] =
                {
                    "desv": desv,
                    "desvNeg" : desvNeg,
                    "desvPos" : desvPos,
                 }
        }
    }

    Highcharts.chart('container', {
        chart: {
            zoomType: 'xy'
        },
        exporting: { enabled: false },
        title: {
            text: ' '
        },
        xAxis: [{
            categories: ['Nat', 'HH', 'IE']
        }],
        yAxis: [{ // Primary yAxis
            labels: {
                format: '{value}',
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            },
            title: {
                text: ' ',
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            },
            min: 0,
            max: 10,
            tickInterval: 1,
        }],
        /*tooltip: {

            useHTML: true,
            headerFormat: '<small>{point.key}</small><br>',
            pointFormat: '<span style="font-weight: bold; color: #339933">{series.name}</span>: <b>{point.y:.1f}</b> ',
            shared: true
        },*/

        series: [{
            name: ' ',
            type: 'errorbar',
            yAxis: 0,
            data: [
                /*[datosDesv[0].desvNeg, datosDesv[0].desvPos, datosDesv[0].desv],
                [datosDesv[1].desvNeg, datosDesv[1].desvPos, datosDesv[1].desv],
                [datosDesv[2].desvNeg, datosDesv[2].desvPos, datosDesv[2].desv]]*/
                {

                    low: datosDesv[0].desvNeg,
                    high: datosDesv[0].desvPos,
                    name: datosDesv[0].desv,


                },{

                    low: datosDesv[1].desvNeg,
                    high: datosDesv[1].desvPos,
                    name: datosDesv[1].desv,


                },{

                    low: datosDesv[2].desvNeg,
                    high: datosDesv[2].desvPos,
                    name: datosDesv[2].desv,


                }
            ],

            tooltip: {
                useHTML: true,
                headerFormat: '<small>{point.x}</small><br>',
                pointFormat: '<span style="font-weight: bold; color: black">Desv. Std.</span>: <b>± {point.name}</b> '
            }

        }, {
            //name: 'Rodal 1',
            name: rodalName[0].nombre,
            type: 'scatter',
            data: [datosEjes[0].valorRodal, datosEjes[1].valorRodal, datosEjes[2].valorRodal],
            marker: {
                symbol: 'circle',
                fillColor: '#339933',
                lineColor: '#339933',
            },
            tooltip: {
                useHTML: true,
                headerFormat: '<small>{point.key}</small><br>',
                pointFormat: '<span style="font-weight: bold; color: #339933">{series.name}</span>: <b>{point.y:.1f}</b> '
                /*pointFormatter: function(){
                    return '<small>'+ this.point.key +'</small><br><span style="font-weight: bold; color: #FF6600">'+ this.series.name +'</span>: <b>'+ this.point.y +'</b>';
                }*/
            }

        },
        {
            //name: 'Rodal 2',
            name: rodalNameRef[0].nombre,
            type: 'scatter',
            data: [datosEjes[0].valorRodalComp, datosEjes[1].valorRodalComp, datosEjes[2].valorRodalComp],
            marker: {
                symbol: 'circle',
                fillColor: '#FF6600',
                lineColor: '#FF6600'
            },
            tooltip: {
                useHTML: true,
                headerFormat: '<small>{point.key}</small><br>',
                pointFormat: '<span style="font-weight: bold; color: #FF6600">{series.name}</span>: <b>{point.y:.1f}</b> '
                /*pointFormatter: function(){
                    return '<small>'+ this.point.key +'</small><br><span style="font-weight: bold; color: #FF6600">'+ this.series.name +'</span>: <b>'+ this.point.y +'</b>';
                }*/
            }
        }]
    });
};

var graficaCritNat = function(datosCritNat, rodalName, rodalNameRef){

    var dataSize = Object.keys(datosCritNat).length;
    var datosDesv = [];
    desv = [];
    desvNeg = [];
    desvPos = [];

    for (i=0; i<=dataSize; i++){
        if(datosCritNat[i] != null){

            var desv = Math.round(datosCritNat[i].desv * 100) / 100;
            var desvNeg = Math.round((datosCritNat[i].valorRodalComp - datosCritNat[i].desv) * 100) / 100;
            var desvPos = Math.round((datosCritNat[i].valorRodalComp + datosCritNat[i].desv) * 100) / 100;

            datosDesv[i] =
                {
                    "desv": desv,
                    "desvNeg" : desvNeg,
                    "desvPos" : desvPos,
                 }
        }
    }


    Highcharts.chart('container2', {
        chart: {
            zoomType: 'xy'
        },
        exporting: { enabled: false },
        title: {
            text: ' '
        },
        xAxis: [{
            categories: ['Comp', 'Compl', 'Mad', 'MicHab', 'Din']
        }],
        yAxis: [{ // Primary yAxis
            labels: {
                format: '{value}',
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            },
            title: {
                text: ' ',
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            },
            min: 0,
            max: 10,
            tickInterval: 1,
        }],

        tooltip: {
            shared: true
        },

        series: [{
            name: 'Rainfall error',
            type: 'errorbar',
            yAxis: 0,
            data: [{
                    low: datosDesv[0].desvNeg,
                    high: datosDesv[0].desvPos,
                    name: datosDesv[0].desv,
                },{
                    low: datosDesv[1].desvNeg,
                    high: datosDesv[1].desvPos,
                    name: datosDesv[1].desv,
                },{
                    low: datosDesv[2].desvNeg,
                    high: datosDesv[2].desvPos,
                    name: datosDesv[2].desv,
                },{
                    low: datosDesv[3].desvNeg,
                    high: datosDesv[3].desvPos,
                    name: datosDesv[3].desv,
                },{
                    low: datosDesv[4].desvNeg,
                    high: datosDesv[4].desvPos,
                    name: datosDesv[4].desv,
                }

            ],

            tooltip: {
                useHTML: true,
                headerFormat: '<small>{point.x}</small><br>',
                pointFormat: '<span style="font-weight: bold; color: black">Desv. Std.</span>: <b>± {point.name}</b> '
            }

        }, {
            name: rodalName[0].nombre,
            type: 'scatter',
            data: [
                datosCritNat[0].valorRodal,
                datosCritNat[1].valorRodal,
                datosCritNat[2].valorRodal,
                datosCritNat[3].valorRodal,
                datosCritNat[4].valorRodal],

            marker: {
                symbol: 'circle',
                fillColor: '#339933',
                lineColor: '#339933'
            },

            tooltip: {
                useHTML: true,
                headerFormat: '<small>{point.key}</small><br>',
                pointFormat: '<span style="font-weight: bold; color: #339933">{series.name}</span>: <b>{point.y:.1f}</b> '
            }
        },
        {
            name: rodalNameRef[0].nombre,
            type: 'scatter',
            data: [
                datosCritNat[0].valorRodalComp,
                datosCritNat[1].valorRodalComp,
                datosCritNat[2].valorRodalComp,
                datosCritNat[3].valorRodalComp,
                datosCritNat[4].valorRodalComp,
             ],

            marker: {
                symbol: 'circle',
                fillColor: '#FF6600',
                lineColor: '#FF6600'
            },

            tooltip: {
                useHTML: true,
                headerFormat: '<small>{point.key}</small><br>',
                pointFormat: '<span style="font-weight: bold; color: #FF6600">{series.name}</span>: <b>{point.y:.1f}</b> '
            }
        }]
    });

}

var graficaCritHu = function(datosCritHu, rodalName, rodalNameRef){

    var dataSize = Object.keys(datosCritHu).length;
    var datosDesv = [];
    desv = [];
    desvNeg = [];
    desvPos = [];

    for (i=0; i<=dataSize; i++){
        if(datosCritHu[i] != null){

            var desv = Math.round(datosCritHu[i].desv * 100) / 100;
            var desvNeg = Math.round((datosCritHu[i].valorRodalComp - datosCritHu[i].desv) * 100) / 100;
            var desvPos = Math.round((datosCritHu[i].valorRodalComp + datosCritHu[i].desv) * 100) / 100;

            datosDesv[i] =
                {
                    "desv": desv,
                    "desvNeg" : desvNeg,
                    "desvPos" : desvPos,
                 }

        }
    }

    Highcharts.chart('container3', {
        chart: {
            zoomType: 'xy'
        },
        exporting: { enabled: false },
        title: {
            text: ' '
        },
        xAxis: [{
            categories: ['HAnt', 'HRec']
        }],
        yAxis: [{ // Primary yAxis
            labels: {
                format: '{value}',
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            },
            title: {
                text: ' ',
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            },
            min: 0,
            max: 10,
            tickInterval: 1,
        }],

        tooltip: {
            shared: true
        },

        series: [{
            name: 'Rainfall error',
            type: 'errorbar',
            yAxis: 0,
            data: [{
                    low: datosDesv[0].desvNeg,
                    high: datosDesv[0].desvPos,
                    name: datosDesv[0].desv,
                },{
                    low: datosDesv[1].desvNeg,
                    high: datosDesv[1].desvPos,
                    name: datosDesv[1].desv,
                }

            ],

            tooltip: {
                useHTML: true,
                headerFormat: '<small>{point.x}</small><br>',
                pointFormat: '<span style="font-weight: bold; color: black">Desv. Std.</span>: <b>± {point.name}</b> '
            }

        }, {
            name: rodalName[0].nombre,
            type: 'scatter',
            data: [datosCritHu[0].valorRodal, datosCritHu[1].valorRodal],
            marker: {
                symbol: 'circle',
                fillColor: '#339933',
                lineColor: '#339933'
            },
            tooltip: {
                useHTML: true,
                headerFormat: '<small>{point.key}</small><br>',
                pointFormat: '<span style="font-weight: bold; color: #339933">{series.name}</span>: <b>{point.y:.1f}</b> '
            }
        },
        {
            name: rodalNameRef[0].nombre,
            type: 'scatter',
            data: [datosCritHu[0].valorRodalComp, datosCritHu[1].valorRodalComp],
            marker: {
                symbol: 'circle',
                fillColor: '#FF6600',
                lineColor: '#FF6600'
            },
            tooltip: {
                useHTML: true,
                headerFormat: '<small>{point.key}</small><br>',
                pointFormat: '<span style="font-weight: bold; color: #FF6600">{series.name}</span>: <b>{point.y:.1f}</b> '
            }
        }]
    });
};

var graficaCritIe = function(datosCritIe, rodalName, rodalNameRef){

    var dataSize = Object.keys(datosCritIe).length;
    var datosDesv = [];
    desv = [];
    desvNeg = [];
    desvPos = [];

    for (i=0; i<=dataSize; i++){
        if(datosCritIe[i] != null){
            var desv = Math.round(datosCritIe[i].desv * 100) / 100;
            var desvNeg = Math.round((datosCritIe[i].valorRodalComp - datosCritIe[i].desv) * 100) / 100;
            var desvPos = Math.round((datosCritIe[i].valorRodalComp + datosCritIe[i].desv) * 100) / 100;

            datosDesv[i] =
                {
                    "desv": desv,
                    "desvNeg" : desvNeg,
                    "desvPos" : desvPos,
                 }
        }
    }

    Highcharts.chart('container4', {
        chart: {
            zoomType: 'xy'
        },
        exporting: { enabled: false },
        title: {
            text: ' '
        },
        xAxis: [{
            categories: ['Tam', 'CF', 'EB', 'Conec']
        }],
        yAxis: [{ // Primary yAxis
            labels: {
                format: '{value}',
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            },
            title: {
                text: ' ',
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            },
            min: 0,
            max: 10,
            tickInterval: 1,
        }],

        tooltip: {
            shared: true
        },

        series: [{
            name: 'Rainfall error',
            type: 'errorbar',
            yAxis: 0,
            data: [
                {
                    low: datosDesv[0].desvNeg,
                    high: datosDesv[0].desvPos,
                    name: datosDesv[0].desv,
                },{
                    low: datosDesv[1].desvNeg,
                    high: datosDesv[1].desvPos,
                    name: datosDesv[1].desv,
                },{
                    low: datosDesv[2].desvNeg,
                    high: datosDesv[2].desvPos,
                    name: datosDesv[2].desv,
                },{
                    low: datosDesv[3].desvNeg,
                    high: datosDesv[3].desvPos,
                    name: datosDesv[3].desv,
                }

            ],

            tooltip: {
                useHTML: true,
                headerFormat: '<small>{point.x}</small><br>',
                pointFormat: '<span style="font-weight: bold; color: black">Desv. Std.</span>: <b>± {point.name}</b> '
            }
        }, {
            name: rodalName[0].nombre,
            type: 'scatter',
            data: [
                datosCritIe[0].valorRodal,
                datosCritIe[1].valorRodal,
                datosCritIe[2].valorRodal,
                datosCritIe[3].valorRodal,],
            marker: {
                symbol: 'circle',
                fillColor: '#339933',
                lineColor: '#339933'
            },
            tooltip: {
                useHTML: true,
                headerFormat: '<small>{point.key}</small><br>',
                pointFormat: '<span style="font-weight: bold; color: #339933">{series.name}</span>: <b>{point.y:.1f}</b> '
            }
        },
        {
            name: rodalNameRef[0].nombre,
            type: 'scatter',
            data: [
                datosCritIe[0].valorRodalComp,
                datosCritIe[1].valorRodalComp,
                datosCritIe[2].valorRodalComp,
                datosCritIe[3].valorRodalComp,],
            marker: {
                symbol: 'circle',
                fillColor: '#FF6600',
                lineColor: '#FF6600'
            },
            tooltip: {
                useHTML: true,
                headerFormat: '<small>{point.key}</small><br>',
                pointFormat: '<span style="font-weight: bold; color: #FF6600">{series.name}</span>: <b>{point.y:.1f}</b> '
            }
        }]
    });
};

var graficaScatter = function(rodalCord, rodalReferenciaCord, grafico, ejeXSelected, ejeYSelected){

    if(ejeXSelected == 'nm'){
        ejeXSelected = 'Naturalidad';
    }else if(ejeXSelected == 'hh'){
        ejeXSelected = 'Huella Humana';
    }else if(ejeXSelected == 'ie'){
        ejeXSelected = 'Integridad Espacial';
    }

    if(ejeYSelected == 'nm'){
        ejeYSelected = 'Naturalidad';
    }else if(ejeYSelected == 'hh'){
        ejeYSelected = 'Huella Humana';
    }else if(ejeYSelected == 'ie'){
        ejeYSelected = 'Integridad Espacial';
    }

    Highcharts.chart(grafico, {
    chart: {
        type: 'scatter',
        zoomType: 'xy',

    },
    exporting: { enabled: false },
    title: {
        text: ''
    },
    /*subtitle: {
        text: 'Source: Heinz  2003'
    },*/
    xAxis: {
        title: {
            enabled: true,
            text: ejeXSelected
        },
        startOnTick: true,
        endOnTick: true,
        showLastLabel: true,
        min: 0,
        max: 10,
        tickInterval: 1,
        gridLineWidth: 1,
        width: 325,
        height: 325

    },
    yAxis: {
        title: {
            text: ejeYSelected,
            enabled: true,
        },
        min: 0,
        max: 10,
        tickInterval: 1,
        height: 325,
        width: 325,

    },
    tooltip: {
        formatter: function(){
            var nombreRodal = this.point.name;
            return '<b>' + nombreRodal + '</b><br>Eje X: ' + this.x + '<br> Eje Y: ' + this.y;
        }
    },
    plotOptions: {
        scatter: {
            marker: {
                radius: 5,
                states: {
                    hover: {
                        enabled: true,
                        lineColor: 'rgb(100,100,100)'
                    }
                }
            },
            states: {
                hover: {
                    marker: {
                        enabled: false
                    }
                }
            },

        }
    },
    series: [{
        name: rodalCord[0].name,
        color: 'rgba(223, 83, 83, .5)',
        data: rodalCord,
        marker: {
                symbol: 'circle',
                fillColor: '#339933',
                lineColor: '#339933',
                radius: 10,
                //height: 40
            },
    }, {
        //name: rodalReferenciaXY[0].name,
        name: 'Rodal 2',
        color: 'rgba(119, 152, 191, .5)',
        data: rodalReferenciaCord,
        marker: {
                symbol: 'circle',
                fillColor: '#FF6600',
                lineColor: '#FF6600',
            },
        }]
    });


}

var graficaScatterDefault = function(){
    rodalX1 = null;
    rodalReferenciaX1 = null;
    rodalY1 = null;
    rodalReferenciaY1 = null;

    rodalX2 = null;
    rodalReferenciaX2 = null;
    rodalY2 = null;
    rodalReferenciaY2 = null;

    rodalX3 = null;
    rodalReferenciaX3 = null;
    rodalY3 = null;
    rodalReferenciaY3 = null;

    $("#ejeXGrafica1").val('null');
    $("#ejeYGrafica1").val('null');
    $("#ejeXGrafica2").val('null');
    $("#ejeYGrafica2").val('null');
    $("#ejeXGrafica3").val('null');
    $("#ejeYGrafica3").val('null');

    var scatters = ['scatter1', 'scatter2', 'scatter3'];
    for(i=0; i<scatters.length; i++){


        Highcharts.chart(scatters[i], {
        chart: {
            type: 'scatter',
            zoomType: 'xy',

        },
        exporting: { enabled: false },
        title: {
            text: ''
        },
        /*subtitle: {
            text: 'Source: Heinz  2003'
        },*/
        xAxis: {
            title: {
                enabled: true,
                text: ' '
            },
            startOnTick: true,
            endOnTick: true,
            showLastLabel: true,
            min: 0,
            max: 10,
            tickInterval: 1,
            gridLineWidth: 1,
            width: 325,
            height: 325

        },
        yAxis: {
            title: {
                text: ' ',
                enabled: true,
            },
            min: 0,
            max: 10,
            tickInterval: 1,
            height: 325,
            width: 325,

        },
        series: [{
            name: 'Rodal 1',
            color: 'rgba(223, 83, 83, .5)',
            data: null,
             marker: {
                    symbol: 'circle',
                    fillColor: '#339933',
                    lineColor: '#339933'
                },

        }, {
            name: 'Rodal 2',
            color: 'rgba(119, 152, 191, .5)',
            data: null,
            marker: {
                    symbol: 'circle',
                    fillColor: '#FF6600',
                    lineColor: '#FF6600'
                },
        }]
        });
    }
}

var graficaBarras1 = function(){
    console.log("grafica1");
    var rodNombres = [];
    var rodValores = [];
    var rodVal = [];

    var barGraphDataSize = Object.keys(dataChartGraph[0]).length;
    //console.log(barGraphDataSize);
    var optionSelected = $("#selecGrafBar1").val();
    //console.log(optionSelected);

    valoresBarrasEjes = setBars(barGraphDataSize, optionSelected);
    //console.log(valoresBarrasEjes);


    for(t=0; t<valoresBarrasEjes.length; t++){
        for(x=0; x<valoresBarrasEjes[t].length; x++){
            rodValores.push(valoresBarrasEjes[t][x]);
        }
    }

    var ord = rodValores.sort(function (a, b){
        return (b.y - a.y)
    })


    for(t=0; t<rodValores.length; t++){
        //for(x=0; x<rodValores[t].length; x++){
            //rodValores.push(valoresBarrasEjes[t][x]);
            rodNombres.push(rodValores[t].name);
            //rodVal.push(rodValores[t].val);

            rodVal[t] = {
                'y': rodValores[t].y,
                'color': rodValores[t].color
            }
        //}
    }




    Highcharts.chart('graficaBarras1', {
        chart: {
            type: 'bar'
        },
        title: {
            text: ''
        },
        exporting: { enabled: false },
        xAxis: {
            categories: rodNombres,
            title: {
                text: null
            }
        },
        yAxis: {
            min: 0,
            max: 10,
            tickInterval: 1,
            title: {
                text: '',

            },
            labels: {
                overflow: 'justify'
            }
        },
        tooltip: {
            formatter: function(){
                var nombreRodal = this.x;
                return '<b>' + nombreRodal + '</b><br>Valor: ' + this.y;
            }
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: false
                }
            }
        },
        credits: {
            enabled: false
        },
        series: [{
            color: '#FF6600',
            showInLegend: false,
            name: rodVal.name,
            //data: [6, 5, {y:3, color:'#339933'}, 2, 2]
            data: rodVal
        }]
    });
}

var graficaBarras2 = function(){
    console.log("grafica2");
    var rodNombres = [];
    var rodValores = [];
    var rodVal = [];
    var valores = [];

    var barGraphDataSize = Object.keys(dataChartGraph[1]).length;
    console.log(barGraphDataSize);
    var optionSelected = $("#selecGrafBar2").val();
    console.log(optionSelected);
    valoresBarrasCrite = setBars(barGraphDataSize, optionSelected);

    for(t=0; t<valoresBarrasCrite.length; t++){
        for(x=0; x<valoresBarrasCrite[t].length; x++){
            valores.push(valoresBarrasCrite[t][x]);
        }
    }

    var ord = valores.sort(function (a, b){
        return (b.y - a.y)
    });

    for(z=0; z<valores.length; z++){
        rodNombres.push(valores[z]['name']);

        rodVal[z] = {
            'y': valores[z]['y'],
            'color': valores[z]['color']
        }
    }


    Highcharts.chart('graficaBarras2', {
        chart: {
            type: 'bar'
        },
        title: {
            text: ''
        },
        exporting: { enabled: false },
        xAxis: {
            categories: rodNombres,
            title: {
                text: null
            }
        },
        yAxis: {
            min: 0,
            max: 10,
            tickInterval: 1,
            title: {
                text: '',

            },
            labels: {
                overflow: 'justify'
            }
        },
        tooltip: {
            formatter: function(){
                var nombreRodal = this.x;
                return '<b>' + nombreRodal + '</b><br>Valor: ' + this.y;
            }
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: false
                }
            }
        },
        credits: {
            enabled: false
        },
        series: [{
            color: '#FF6600',
            showInLegend: false,
            name: 'Year 1800',
            //data: [6, 5, {y:3, color:'#339933'}, 2, 2]
            data: rodVal
        }]
    });
}

var graficaBarrasDefault = function(){

    rodNombres = null;
    rodValores = null;
    rodVal = null;
    valores = null;

    $("#selecGrafBar1").val('null');
    $("#selecGrafBar2").val('null');

    var grafs = ['graficaBarras1', 'graficaBarras2'];
    var rod = ['Rodal 1', 'Rodal 2'];

    for (t=0; t<grafs.length; t++){

        Highcharts.chart(grafs[t], {
            chart: {
                type: 'bar'
            },
            title: {
                text: ''
            },
            exporting: { enabled: false },
            xAxis: {
                categories: ['Rodal 1', 'Rodal 2'],

            },
            yAxis: {
                min: 0,
                max: 10,
                tickInterval: 1,
                title: {
                    text: '',

                },
                labels: {
                    overflow: 'justify'
                }
            },

            plotOptions: {
                bar: {
                    dataLabels: {
                        enabled: false
                    }
                }
            },
            credits: {
                enabled: false
            },
            series: [{
                name: 'Rodal 1',
                color: '#339933',
                data: [0,0],
            },
            {
                name: 'Rodal 2',
                color: '#FF6600',
                data: [0,0],
            }],

        });
    }
}

function resetUITable(){
    /*$('td.diff-col').html('---');
    $('td.col-diff').html('---');
    $('.valGraf').html('---');
    $('.valGraf').css("background-color", "#FFFFFF");
    $('.divGraf').empty();
    $('.col-diff').removeAttr("style");
    $('.diff-col').removeAttr("style");*/
}


