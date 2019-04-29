$(document).ready(function() {
    graficaScatterDefault();
    blockSelectores();
    //graficaBarras1(valoresBarrasEjes);
    graficaBarras2();
});

var dataGraph2;
var datosEjesGraph2 = {};
var dotsGraphData = []
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
//var rodalYNombres = [];
//var rodalReferenciaYNombres = [];
//var rodalXNombres = [];
//var rodalReferenciaXNombres = [];

var dataGraph = function(valoresRodal, valoresRodalComp){

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

    graficaEjes(datosEjes);
    graficaCritNat(datosCritNat);
    graficaCritHu(datosCritHu);
    graficaCritIe(datosCritIe);

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

    for(i=0; i<rodalPuntosData.length; i++){
        if(rodalPuntosData[i].indicador_cod == 'nm'){
            NM = {
                "rodal": {
                    "eje": rodalPuntosData[i].indicador_cod,
                    "id_rodal": rodalPuntosData[i].id_rodal,
                    "nombre": rodalPuntosData[i].nombre,
                    "valor": rodalPuntosData[i].valor
                }
            }
            nmRodal.push(NM);
        }else if(rodalPuntosData[i].indicador_cod == 'ie'){
            IE = {
                "rodal": {
                    "eje" :rodalPuntosData[i].indicador_cod,
                    "id_rodal": rodalPuntosData[i].id_rodal,
                    "nombre": rodalPuntosData[i].nombre,
                    "valor": rodalPuntosData[i].valor
                }
            }
            ieRodal.push(IE);
        }else if(rodalPuntosData[i].indicador_cod == 'hh'){
            HH = {
                "rodal": {
                    "eje" :rodalPuntosData[i].indicador_cod,
                    "id_rodal": rodalPuntosData[i].id_rodal,
                    "nombre": rodalPuntosData[i].nombre,
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
                    "nombre": rodalRefPuntosData[i].nombre,
                    "valor": rodalRefPuntosData[i].valor
                }
            }
            nmRodalRef.push(NM);
        }else if(rodalRefPuntosData[i].indicador_cod == 'ie'){
            IE = {
                "rodal": {
                    "eje" :rodalRefPuntosData[i].indicador_cod,
                    "id_rodal": rodalRefPuntosData[i].id_rodal,
                    "nombre": rodalRefPuntosData[i].nombre,
                    "valor": rodalRefPuntosData[i].valor
                }
            }
            ieRodalRef.push(IE);
        }else if(rodalRefPuntosData[i].indicador_cod == 'hh'){
            HH = {
                "rodal": {
                    "eje" :rodalRefPuntosData[i].indicador_cod,
                    "id_rodal": rodalRefPuntosData[i].id_rodal,
                    "nombre": rodalRefPuntosData[i].nombre,
                    "valor": rodalRefPuntosData[i].valor
                }
            }
            hhRodalRef.push(HH);
        }

    }

    rodalReferenciaPuntos.push(nmRodalRef,ieRodalRef,hhRodalRef);
    dotsGraphData.push(rodalPuntos, rodalReferenciaPuntos);
    //console.log(dotsGraphData);
    return dotsGraphData;
}


function dataChartCrite(rodalCriteChart, rodalRefCriteChart){

    console.log(rodalCriteChart);
    console.log(rodalRefCriteChart);


    for(i=0; i<rodalCriteChart.length; i++){
        if(rodalCriteChart[i].indicador_cod == 'ar'){
            AR = {
                "rodal": {
                    "eje": rodalPuntosData[i].indicador_cod,
                    "id_rodal": rodalPuntosData[i].id_rodal,
                    "nombre": rodalPuntosData[i].nombre,
                    "valor": rodalPuntosData[i].valor
                }
            }
            arRodal.push(AR);
        }else if(rodalPuntosData[i].indicador_cod == 'ce'){
            CE = {
                "rodal": {
                    "eje" :rodalPuntosData[i].indicador_cod,
                    "id_rodal": rodalPuntosData[i].id_rodal,
                    "nombre": rodalPuntosData[i].nombre,
                    "valor": rodalPuntosData[i].valor
                }
            }
            ceRodal.push(CE);
        }else if(rodalPuntosData[i].indicador_cod == 'cf'){
            CF = {
                "rodal": {
                    "eje" :rodalPuntosData[i].indicador_cod,
                    "id_rodal": rodalPuntosData[i].id_rodal,
                    "nombre": rodalPuntosData[i].nombre,
                    "valor": rodalPuntosData[i].valor
                }
            }
            cfRodal.push(CF);
        }else if(rodalPuntosData[i].indicador_cod == 'cn'){
            CN = {
                "rodal": {
                    "eje" :rodalPuntosData[i].indicador_cod,
                    "id_rodal": rodalPuntosData[i].id_rodal,
                    "nombre": rodalPuntosData[i].nombre,
                    "valor": rodalPuntosData[i].valor
                }
            }
            cnRodal.push(CN);
        }else if(rodalPuntosData[i].indicador_cod == 'cp'){
            CP = {
                "rodal": {
                    "eje" :rodalPuntosData[i].indicador_cod,
                    "id_rodal": rodalPuntosData[i].id_rodal,
                    "nombre": rodalPuntosData[i].nombre,
                    "valor": rodalPuntosData[i].valor
                }
            }
            cpRodal.push(CP);
        }else if(rodalPuntosData[i].indicador_cod == 'dn'){
            DN = {
                "rodal": {
                    "eje" :rodalPuntosData[i].indicador_cod,
                    "id_rodal": rodalPuntosData[i].id_rodal,
                    "nombre": rodalPuntosData[i].nombre,
                    "valor": rodalPuntosData[i].valor
                }
            }
            dnRodal.push(DN);
        }else if(rodalPuntosData[i].indicador_cod == 'eb'){
            EB = {
                "rodal": {
                    "eje" :rodalPuntosData[i].indicador_cod,
                    "id_rodal": rodalPuntosData[i].id_rodal,
                    "nombre": rodalPuntosData[i].nombre,
                    "valor": rodalPuntosData[i].valor
                }
            }
            ebRodal.push(EB);
        }else if(rodalPuntosData[i].indicador_cod == 'ha'){
            HA = {
                "rodal": {
                    "eje" :rodalPuntosData[i].indicador_cod,
                    "id_rodal": rodalPuntosData[i].id_rodal,
                    "nombre": rodalPuntosData[i].nombre,
                    "valor": rodalPuntosData[i].valor
                }
            }
            haRodal.push(HA);
        }else if(rodalPuntosData[i].indicador_cod == 'hm'){
            HM = {
                "rodal": {
                    "eje" :rodalPuntosData[i].indicador_cod,
                    "id_rodal": rodalPuntosData[i].id_rodal,
                    "nombre": rodalPuntosData[i].nombre,
                    "valor": rodalPuntosData[i].valor
                }
            }
            hmRodal.push(HM);
        }else if(rodalPuntosData[i].indicador_cod == 'hr'){
            HR = {
                "rodal": {
                    "eje" :rodalPuntosData[i].indicador_cod,
                    "id_rodal": rodalPuntosData[i].id_rodal,
                    "nombre": rodalPuntosData[i].nombre,
                    "valor": rodalPuntosData[i].valor
                }
            }
            hrRodal.push(HR);
        }else if(rodalPuntosData[i].indicador_cod == 'sn'){
            SN = {
                "rodal": {
                    "eje" :rodalPuntosData[i].indicador_cod,
                    "id_rodal": rodalPuntosData[i].id_rodal,
                    "nombre": rodalPuntosData[i].nombre,
                    "valor": rodalPuntosData[i].valor
                }
            }
            snRodal.push(SN);
        }


    }

    rodalPuntos.push(nmRodal,ieRodal,hhRodal)


}

var blockSelectores = function(){
    $('.scatterSelector').attr('disabled', 'disabled');
}

var unblockSelectores = function(){
    $('.scatterSelector').removeAttr('disabled');
}

function rodalData(valorRodal){
    if(valorRodal == 'null'){

    }else{
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
                rodalPuntosData = data.rodalGraficoPuntos;
                rodalCriteData = data.rodalCriteChart;

                graficaScatterDefault();
                console.log(data.rodalGraficoBarras);

                if(rodalReferencia){
                    unblockSelectores();
                    dataGraph(rodalSelData, rodalReferencia);
                    dataGraph2 = dataScatterGraph(rodalPuntosData, rodalRefPuntosData);
                    dataGraphCrite = dataChartCrite(rodalCriteData, rodalRefCriteData);



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
    }
};

function load_rodal_ref(idHabitat, idComAut, idRegBiogeo, valRod){
    url = _rodal_ref_list;
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

    //params.push('rodRef='+escape(rodRef));

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
                rodalReferencia = data.rodal_referencia;
                rodalRefPuntosData = data.rodalRefGraficoPuntos;
                rodalRefCriteData = data.rodalRefCriteChart;
                recorreArbre('', rodalReferencia);

                //infoRodal = fata.infoRodal;

                graficaScatterDefault();

                if(rodalSelData){
                    if(rodalReferencia != null){
                        //calcDiferencia();
                        unblockSelectores();
                        $('.grafico div').html('');
                        dataGraph(rodalSelData, rodalReferencia);
                        dataGraph2 = dataScatterGraph(rodalPuntosData, rodalRefPuntosData);
                        dataGraphCrite = dataChartCrite(rodalCriteData, rodalRefCriteData);

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
};

$('.grafica1').change(function(){
    var ejeX = "ejeXGrafica1";
    var ejeY = "ejeYGrafica1";
    var ejeSelected = $(this).val();
    var dotsGraphDataSize = Object.keys(dotsGraphData[1]).length;


    var ejeSelected = $(this).attr('id');
    var ejeOptionSelected = $(this).val();

    if(ejeSelected == ejeX){
        rodalX1 = [];
        rodalReferenciaX1 = [];

        coordenadasPuntos = setPoints(dotsGraphDataSize, ejeOptionSelected);
        rodalX1 = coordenadasPuntos[0];
        rodalReferenciaX1 = coordenadasPuntos[1];

        if(rodalY1 != null && rodalReferenciaY1 != null){
            var coordenadas = setCoordenadas(rodalX1, rodalReferenciaX1, rodalY1, rodalReferenciaY1);
            rodalXY1 = coordenadas[0];
            rodalReferenciaXY1 = coordenadas[1];
            grafico = 'scatter1';
            graficaScatter(rodalXY1, rodalReferenciaXY1, grafico);
        }

    }else if(ejeSelected == ejeY){
        rodalY1 = [];
        rodalReferenciaY1 = [];
        var coordenadasPuntos = setPoints(dotsGraphDataSize, ejeOptionSelected);
        rodalY1 = coordenadasPuntos[0];
        rodalReferenciaY1 = coordenadasPuntos[1];

        if(rodalX1 != null && rodalReferenciaX1 != null){
            var coordenadas = setCoordenadas(rodalX1, rodalReferenciaX1, rodalY1, rodalReferenciaY1);
            rodalXY1 = coordenadas[0];
            rodalReferenciaXY1 = coordenadas[1];
            grafico = 'scatter1';
            graficaScatter(rodalXY1, rodalReferenciaXY1, grafico);
        }
    }
});

$('.grafica2').change(function(){
    var ejeX = "ejeXGrafica2";
    var ejeY = "ejeYGrafica2";
    var ejeSelected = $(this).val();
    var dotsGraphDataSize = Object.keys(dotsGraphData[1]).length;


    var ejeSelected = $(this).attr('id');
    var ejeOptionSelected = $(this).val();

    if(ejeSelected == ejeX){
        rodalX2 = [];
        rodalReferenciaX2 = [];

        coordenadasPuntos = setPoints(dotsGraphDataSize, ejeOptionSelected);
        rodalX2 = coordenadasPuntos[0];
        rodalReferenciaX2 = coordenadasPuntos[1];

        if(rodalY2 != null && rodalReferenciaY2 != null){
            var coordenadas = setCoordenadas(rodalX2, rodalReferenciaX2, rodalY2, rodalReferenciaY2);
            rodalXY2 = coordenadas[0];
            rodalReferenciaXY2 = coordenadas[1];
            grafico = 'scatter2';
            graficaScatter(rodalXY2, rodalReferenciaXY2, grafico);
        }

    }else if(ejeSelected == ejeY){
        rodalY2 = [];
        rodalReferenciaY2 = [];
        var coordenadasPuntos = setPoints(dotsGraphDataSize, ejeOptionSelected);
        rodalY2 = coordenadasPuntos[0];
        rodalReferenciaY2 = coordenadasPuntos[1];

        if(rodalX2 != null && rodalReferenciaX2 != null){
            var coordenadas = setCoordenadas(rodalX2, rodalReferenciaX2, rodalY2, rodalReferenciaY2);
            rodalXY2 = coordenadas[0];
            rodalReferenciaXY2 = coordenadas[1];
            grafico = 'scatter2';
            graficaScatter(rodalXY2, rodalReferenciaXY2, grafico);
        }
    }
});

$('.grafica3').change(function(){
    var ejeX = "ejeXGrafica3";
    var ejeY = "ejeYGrafica3";
    var ejeSelected = $(this).val();
    var dotsGraphDataSize = Object.keys(dotsGraphData[1]).length;


    var ejeSelected = $(this).attr('id');
    var ejeOptionSelected = $(this).val();

    if(ejeSelected == ejeX){
        rodalX3 = [];
        rodalReferenciaX3 = [];

        coordenadasPuntos = setPoints(dotsGraphDataSize, ejeOptionSelected);
        rodalX3 = coordenadasPuntos[0];
        rodalReferenciaX3 = coordenadasPuntos[1];

        if(rodalY3 != null && rodalReferenciaY3 != null){
            var coordenadas = setCoordenadas(rodalX3, rodalReferenciaX3, rodalY3, rodalReferenciaY3);
            rodalXY3 = coordenadas[0];
            rodalReferenciaXY3 = coordenadas[1];
            grafico = 'scatter3';
            graficaScatter(rodalXY3, rodalReferenciaXY3, grafico);
        }

    }else if(ejeSelected == ejeY){
        rodalY3 = [];
        rodalReferenciaY3 = [];
        var coordenadasPuntos = setPoints(dotsGraphDataSize, ejeOptionSelected);
        rodalY3 = coordenadasPuntos[0];
        rodalReferenciaY3 = coordenadasPuntos[1];

        if(rodalX3 != null && rodalReferenciaX3 != null){
            var coordenadas = setCoordenadas(rodalX3, rodalReferenciaX3, rodalY3, rodalReferenciaY3);
            rodalXY3 = coordenadas[0];
            rodalReferenciaXY3 = coordenadas[1];
            grafico = 'scatter3';
            graficaScatter(rodalXY3, rodalReferenciaXY3, grafico);
        }
    }
});

$('.graficaBarEjes').change(function(){
    var dotsGraphDataSize = Object.keys(dotsGraphData[1]).length;
    var ejeOptionSelected = $(this).val();
    valoresBarrasEjes = setPoints(dotsGraphDataSize, ejeOptionSelected);
    graficaBarras1(valoresBarrasEjes);

});

$('.graficaBarCrite').change(function(){
    var dotsGraphDataSize = Object.keys(dotsGraphData[1]).length;
    var criteOptionSelected = $(this).val();

    console.log(dotsGraphDataSize);
    console.log(criteOptionSelected);

});

function setPoints(dotsGraphDataSize, ejeOptionSelected){
    rodalVal = [];
    rodalReferenciaVal = [];
    rodalNombres = [];
    rodalReferenciaNombres = [];
    var pointsData = [];

    /*Rodal inicial*/
    for (i=0; i<dotsGraphDataSize; i++){
        for (x=0; x<dotsGraphData[0][i].length; x++){
            if(dotsGraphData[0][i][x]['rodal']['eje'] == ejeOptionSelected){
                rodalVal.push(dotsGraphData[0][i][x]['rodal']['valor']);
                rodalNombres.push(dotsGraphData[0][i][x]['rodal']['nombre']);


            }
        }
         /*Rodal con el que comparamos*/
        for (x=0; x<dotsGraphData[1][i].length; x++){
            if(dotsGraphData[1][i][x]['rodal']['eje'] == ejeOptionSelected){
                rodalReferenciaVal.push(dotsGraphData[1][i][x]['rodal']['valor']);
                rodalReferenciaNombres.push(dotsGraphData[1][i][x]['rodal']['nombre']);

            }
        }
    }

    var rodal2 = [];
    var rodalReferencia2 = [];

    for(r=0; r<rodalVal.length; r++){
        rodal2 = [{
            'nombre': rodalNombres[r],
            'val': rodalVal[r],
            'color': '#339933'
        }]
    }
    for(rRef=0; rRef<rodalReferenciaVal.length; rRef++){
        rodalReferencia2[rRef] = {
           'nombre': rodalReferenciaNombres[rRef],
            'val': rodalReferenciaVal[rRef]
        }
    }
    pointsData.push(rodal2, rodalReferencia2);
    return pointsData;
};

function setCoordenadas(rodalX, rodalReferenciaX, rodalY, rodalReferenciaY){
    var rXY = [];
    var rRefXY = [];
    var coordenadasRodales = [];

    rXY = [{
        'name': rodalX[0].nombre,
        'x': rodalX[0].val,
        'y': rodalY[0].val
    }]

    for(r=0; r<rodalReferenciaX.length; r++){
        rRefXY[r] = {
            'name': rodalReferenciaY[r].nombre,
            'x': rodalReferenciaX[r].val,
            'y': rodalReferenciaY[r].val
        }
    }

    coordenadasRodales.push(rXY, rRefXY);

    return coordenadasRodales;

}

var graficaEjes = function(datosEjes){

    var dataSize = Object.keys(datosEjes).length;
    var datosDesv = [];

    for (i=0; i<=dataSize; i++){
        if(datosEjes[i] != null){
            datosDesv[i] =
                { "desvNeg" : parseInt((datosEjes[i].valorRodalComp - datosEjes[i].desv).toFixed(2)),
                  "desvPos" : parseInt((datosEjes[i].valorRodalComp + datosEjes[i].desv).toFixed(2)),
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

        tooltip: {
            shared: true
        },

        series: [{
            name: 'Rainfall error',
            type: 'errorbar',
            yAxis: 0,
            data: [[datosDesv[0].desvNeg, datosDesv[0].desvPos], [datosDesv[1].desvNeg, datosDesv[1].desvPos], [datosDesv[2].desvNeg, datosDesv[2].desvPos]],

            tooltip: {
                pointFormat: '(error range: {point.low}-{point.high} mm)<br/>'
            }
        }, {
            name: 'Rodal 1',
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
            }
        },
        {
            name: 'Rodal 2',
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
            }
        }]
    });
};

var graficaCritNat = function(datosCritNat){

    var dataSize = Object.keys(datosCritNat).length;
    var datosDesv = [];

    for (i=0; i<=dataSize; i++){
        if(datosCritNat[i] != null){
            datosDesv[i] =
                { "desvNeg" : parseInt((datosCritNat[i].valorRodalComp - datosCritNat[i].desv).toFixed(2)),
                  "desvPos" : parseInt((datosCritNat[i].valorRodalComp + datosCritNat[i].desv).toFixed(2)),
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
            data: [
                [datosDesv[0].desvNeg, datosDesv[0].desvPos],
                [datosDesv[1].desvNeg, datosDesv[1].desvPos],
                [datosDesv[2].desvNeg, datosDesv[2].desvPos],
                [datosDesv[3].desvNeg, datosDesv[3].desvPos],
                [datosDesv[4].desvNeg, datosDesv[4].desvPos],
                ],

            tooltip: {
                pointFormat: '(error range: {point.low}-{point.high} mm)<br/>'
            }
        }, {
            name: 'Rodal 1',
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
            name: 'Rodal 2',
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

var graficaCritHu = function(datosCritHu){

    var dataSize = Object.keys(datosCritHu).length;
    var datosDesv = [];

    for (i=0; i<=dataSize; i++){
        if(datosCritHu[i] != null){
            datosDesv[i] =
                { "desvNeg" : parseInt((datosCritHu[i].valorRodalComp - datosCritHu[i].desv).toFixed(2)),
                  "desvPos" : parseInt((datosCritHu[i].valorRodalComp + datosCritHu[i].desv).toFixed(2)),
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
            data: [
                [datosDesv[0].desvNeg, datosDesv[0].desvPos],
                [datosDesv[1].desvNeg, datosDesv[1].desvPos],
                ],
            tooltip: {
                pointFormat: '(error range: {point.low}-{point.high} mm)<br/>'
            }
        }, {
            name: 'Rodal 1',
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
            name: 'Rodal 2',
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

var graficaCritIe = function(datosCritIe){

    var dataSize = Object.keys(datosCritIe).length;
    var datosDesv = [];

    for (i=0; i<=dataSize; i++){
        if(datosCritIe[i] != null){
            datosDesv[i] =
                { "desvNeg" : parseInt((datosCritIe[i].valorRodalComp - datosCritIe[i].desv).toFixed(2)),
                  "desvPos" : parseInt((datosCritIe[i].valorRodalComp + datosCritIe[i].desv).toFixed(2)),
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
                [datosDesv[0].desvNeg, datosDesv[0].desvPos],
                [datosDesv[1].desvNeg, datosDesv[1].desvPos],
                [datosDesv[2].desvNeg, datosDesv[2].desvPos],
                [datosDesv[3].desvNeg, datosDesv[3].desvPos],],
            tooltip: {
                pointFormat: '(error range: {point.low}-{point.high} mm)<br/>'
            }
        }, {
            name: 'Rodal 1',
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
            name: 'Rodal 2',
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

var graficaScatter = function(rodalXY, rodalReferenciaXY, grafico){
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
        name: rodalXY[0].name,
        color: 'rgba(223, 83, 83, .5)',
        data: rodalXY,
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
        data: rodalReferenciaXY,
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

var graficaBarras1 = function(valoresBarrasEjes){
    var rodNombres = [];
    var rodValores = [];
    var rodVal = [];

    for(t=0; t<valoresBarrasEjes.length; t++){
        for(x=0; x<valoresBarrasEjes[t].length; x++){
            rodValores.push(valoresBarrasEjes[t][x]);
        }
    }

    var ord = rodValores.sort(function (a, b){
        return (b.val - a.val)
    })
    console.log(ord);

    for(t=0; t<rodValores.length; t++){
        //for(x=0; x<rodValores[t].length; x++){
            //rodValores.push(valoresBarrasEjes[t][x]);
            rodNombres.push(rodValores[t].nombre);
            //rodVal.push(rodValores[t].val);

            rodVal[t] = {
                'y': rodValores[t].val,
                'color': rodValores[t].color
            }
        //}
    }

    console.log(rodNombres);
    console.log(rodVal);

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
            valueSuffix: ' millions'
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

var graficaBarras2 = function(){
    Highcharts.chart('graficaBarras2', {
        chart: {
            type: 'bar'
        },
        title: {
            text: ''
        },
        exporting: { enabled: false },
        xAxis: {
            categories: ['Africa', 'America', 'Asia', 'Europe', 'Oceania','Asia', 'Europe', 'Oceania'],
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
            valueSuffix: ' millions'
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
            data: [6, 5, {y:3, color:'#339933'}, 2, 2, 8, 6]
        }]
    });
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

/*$('.scatterSelector').change(function(){

    var ejeSelected = $(this).val();
    var dotsGraphDataSize = Object.keys(dotsGraphData[1]).length;
    var ejeX = null;
    var ejeY = null;

    if($(this).hasClass('grafica1')){
        var ejeX = "ejeXGrafica1";
        var ejeY = "ejeYGrafica1";
    }else if($(this).hasClass('grafica2')){
        var ejeX = "ejeXGrafica2";
        var ejeY = "ejeYGrafica2";
    }else if($(this).hasClass('grafica3')){
        var ejeX = "ejeXGrafica3";
        var ejeY = "ejeYGrafica3";
    }

    var ejeSelected = $(this).attr('id');
    var ejeOptionSelected = $(this).val();

    if(ejeSelected == ejeX){
        rodalX = [];
        rodalReferenciaX = [];
        rodalXNombres = [];
        rodalReferenciaXNombres = [];

        //Rodal inicial
        for (i=0; i<dotsGraphDataSize; i++){
            for (x=0; x<dotsGraphData[0][i].length; x++){
                if(dotsGraphData[0][i][x]['rodal']['eje'] == ejeOptionSelected){
                    rodalX.push(dotsGraphData[0][i][x]['rodal']['valor']);
                    rodalXNombres.push(dotsGraphData[0][i][x]['rodal']['nombre']);

                }
            }
             //Rodal con el que comparamos
            for (x=0; x<dotsGraphData[1][i].length; x++){
                if(dotsGraphData[1][i][x]['rodal']['eje'] == ejeOptionSelected){
                    rodalReferenciaX.push(dotsGraphData[1][i][x]['rodal']['valor']);
                    rodalReferenciaXNombres.push(dotsGraphData[1][i][x]['rodal']['nombre']);
                }
            }
        }


        if(rodalY != null && rodalReferenciaY != null){
            var rodalXY = [];
            var rodalReferenciaXY = [];

            rodalXY = [{
                'name': rodalXNombres,
                'x': rodalX[0],
                'y': rodalY[0]
            }]

            for(r=0; r<rodalReferenciaX.length; r++){
                rodalReferenciaXY[r] = {
                    'name': rodalReferenciaYNombres[r],
                    'x': rodalReferenciaX[r],
                    'y': rodalReferenciaY[r]
                }
            }

            var grafico;
            if($(this).hasClass('grafica1')){
                grafico = 'scatter1';
                graficaScatter(rodalXY, rodalReferenciaXY, grafico);
            }else if($(this).hasClass('grafica2')){
                grafico = 'scatter2';
                graficaScatter(rodalXY, rodalReferenciaXY, grafico);
            }else if($(this).hasClass('grafica3')){
                grafico = 'scatter3';
                graficaScatter(rodalXY, rodalReferenciaXY, grafico);
            }

            rodalX = null;
            rodalReferenciaX = null;
            //rodalY = null;
            //rodalReferenciaY = null;

        }

    }else if(ejeSelected == ejeY){
        rodalY = [];
        rodalReferenciaY = [];
        //rodalYNombres = [];
        //rodalReferenciaYNombres = [];

        //Rodal inicial
        for (i=0; i<dotsGraphDataSize; i++){
            for (x=0; x<dotsGraphData[0][i].length; x++){
                if(dotsGraphData[0][i][x]['rodal']['eje'] == ejeOptionSelected){
                    rodalY.push(dotsGraphData[0][i][x]['rodal']['valor']);
                    rodalYNombres.push(dotsGraphData[0][i][x]['rodal']['nombre']);
                }
            }
        }

        //Rodal de con el que comparamos
        for (i=0; i<dotsGraphDataSize; i++){
            for (x=0; x<dotsGraphData[1][i].length; x++){
                if(dotsGraphData[1][i][x]['rodal']['eje'] == ejeOptionSelected){
                    rodalReferenciaY.push(dotsGraphData[1][i][x]['rodal']['valor']);
                    rodalReferenciaYNombres.push(dotsGraphData[1][i][x]['rodal']['nombre']);
                }
            }
        }

        if(rodalX != null && rodalReferenciaX != null){
            var rodalXY = [];
            var rodalReferenciaXY = [];

            rodalXY = [{
                'name': rodalXNombres,
                'x': rodalX[0],
                'y': rodalY[0]
            }]

            for(r=0; r<rodalReferenciaX.length; r++){
                rodalReferenciaXY[r] = {
                    'name': rodalReferenciaYNombres[r],
                    'x': rodalReferenciaX[r],
                    'y': rodalReferenciaY[r]
                }
            }

            var grafico;
            if($(this).hasClass('grafica1')){
                grafico = 'scatter1';
                graficaScatter(rodalXY, rodalReferenciaXY, grafico);
            }else if($(this).hasClass('grafica2')){
                grafico = 'scatter2';
                graficaScatter(rodalXY, rodalReferenciaXY, grafico);
            }else if($(this).hasClass('grafica3')){
                grafico = 'scatter3';
                graficaScatter(rodalXY, rodalReferenciaXY, grafico);

            }
            //rodalX = null;
            //rodalReferenciaX = null;
            rodalY = null;
            rodalReferenciaY = null;
        }
    }
});*/
