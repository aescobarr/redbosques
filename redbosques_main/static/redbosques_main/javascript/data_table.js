$(document).ready(function() {



});


$('tr.lv1').on("click", function(){

    var classLvl = this.className;
    //console.log(classLvl);

    if(classLvl == "lv1 lv1Nat"){
        $('.lv2Nat').toggle();
    }else if(classLvl == "lv1 lv1Hh"){
        $('.lv2Hh').toggle();
    }else if(classLvl == "lv1 lv1Ie"){
        $('.lv2Ie').toggle();
    }

    /*if(classLvl == "lv1 lv1Nat"){
        $('.lv2Nat, .lv3Nat').toggle();
    }else if(classLvl == "lv1 lv1Hh"){
        $('.lv2Hh, .lv3Hh').toggle();
    }else if(classLvl == "lv1 lv1Ie"){
        $('.lv2Ie, .lv3Ie').toggle();
    }*/

    var validation = $('.lv2Nat').css("display");

    if(($('.lv2Nat').css("display")) == "none"){
        $('.lv3Nat').hide();
    }

    if(($('.lv2Hh').css("display")) == "none"){
        $('.lv3Hh').hide();
    }
});

$('tr.lv2').on("click", function(){

    var classLvl2 = this.className;
    //console.log(classLvl2);

    if(classLvl2 == "lv2 lv2Nat"){
        $('.lv3Nat').toggle();
    }else if(classLvl2 == "lv2 lv2Hh"){
        $('.lv3Hh').toggle();
    }


    /*if(classLvl2 == "lv2 lv2Nat compo"){
        $('.lv3Nat.compo').toggle();
    }else if(classLvl2 == "lv2 lv2Nat compl"){
        $('.lv3Nat.compl').toggle();
    }else if(classLvl2 == "lv2 lv2Nat mad"){
        $('.lv3Nat.mad').toggle();
    }else if(classLvl2 == "lv2 lv2Nat micro"){
        $('.lv3Nat.micro').toggle();
     }else if(classLvl2 == "lv2 lv2Nat din"){
        $('.lv3Nat.din').toggle();
    }else if(classLvl2 == "lv2 lv2Hh ant"){
        $('.lv3Hh.ant').toggle();
    }else if(classLvl2 == "lv2 lv2Hh rec"){
        $('.lv3Hh.rec').toggle();
    }



    */

});

//$('.selector_rodal').on("change", function(){
var rodalRefData = function(){


    url = '/redbosques/valorRef';

    valRod = $('.selector_rodal option:selected').val();
    habSel = $('.habitatSelected').attr('value');


    if(valRod == 'medRod'){
        url = url + '?vr=medRod&habSel='+ habSel;
        console.log(url);
        $('#selector_ComAut option:first').prop('selected', 'selected');
        $('#selector_RegBio option:first').prop('selected', 'selected');

    }else if(valRod != 'medRod' ){
        if (valRod == 'None'){
            $('.valGraf').html('---');
            $('.valGraf').css("background-color", "#FFFFFF");
        }else{
            url = url + '?vr='+valRod;

        }
    }

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
            recorreArbre('', rodalReferencia);
            recorreRodal('', valores_rodal_jason);
            calcDiferencia();

            $('.grafico div').html('');
            dataGraph(valores_rodal_jason, rodalReferencia);
            //crearGraficos(testJson);
        },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
};






var recorreArbre = function(nom_pare, element){
      jQuery.each(element, function(i, actual) {
        if(i === 'valor' || i === 'valor_desv'){
          return;
        }else{
          if(nom_pare === ''){
            nom_complet = i;
          }else{
            nom_complet = nom_pare + "_" + i;
          }

        if (isNaN(element[i].valor)){
            //$('#' + nom_complet).html("---");
            $('#' + nom_complet).html('---');
            element[i].valor = (null);
        }else{
            $('#' + nom_complet).html(element[i].valor);

        }
          rodRef[nom_complet] = element[i].valor;
          recorreArbre(nom_complet, actual);
        }
      });

};


var recorreRodal = function(nom_pare, element){
jQuery.each(element, function(i, actual) {
        if(i === 'valor'){
          return;
        }else{
          if(nom_pare === ''){
            nom_complet = i;
          }else{
            nom_complet = nom_pare + "_" + i;
          }

          if (isNaN(element[i].valor)){
                //element[i].valor = ("---");
                element[i].valor = ('null');
          }
            rodal[nom_complet] = element[i].valor;
            recorreRodal(nom_complet, actual);
        }
      });

};


function calcDiferencia(){
    resComp = [];
    var test = rodal.naturalidad - rodRef.naturalidad;
    for(var key in rodal) {
        var value = rodal[key];
        var value2 = rodRef[key];

        if(isNaN(value) || isNaN(value2)){
            resta = null;
            $('#' + key+'_dif').html("---");
            $('#' + key+'_dif').css("background-color", "#CDCCC8");
        }else{
            resta =  value - value2;
            $('#' + key+'_dif').html(resta);

            if(resta<0){
                $('#' + key+'_dif').css("background-color", "#EF3340");
            }else if(resta >= 0){
                $('#' + key+'_dif').css("background-color", "#9ac635");
            }
        }
        var elem = {};
        elem[key+'_dif'] = resta;
        resComp.push(elem);
    }
}

$('.val-graf.valores').on("click", function(){
     $('td.graf, th.graf').show();
     $('td.grafico').hide();
});

$('.val-graf.grafica').on("click", function(){
    $('td.graf, th.graf').hide();
    $('td.grafico').show();
});



var setFiltros = function(){

        valIdRodal = $('p.rodalSelected').attr('value');
        console.log(valIdRodal);
        url = '/redbosques/setFiltrosRodal?idR=' + valIdRodal;
        valComAut = $('.selector_ComAut option:selected').val();
        valRegBio = $('.selector_RegBio option:selected').val();

        if(valRegBio){
            url = url + '&rb='+valRegBio;
        }

        if(valComAut){
            url = url + '&ca='+valComAut;
        }
        console.log(url);
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

                listaRodales = data.listaRodales;
                $('.valGraf').html('---');
                $('.valGraf').css("background-color", "#FFFFFF");
                $('.selector_rodal .rodal').remove();
                listaRodales.forEach(rodal => {
                    console.log(rodal);
                    $('.selector_rodal').append('<option class="rodal" value="'+ rodal.id_rodal +'">'+ rodal.nombre +'</option>');
                })
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
}



var dataGraph = function(valoresRodal, valoresRodalComp){
    var testJson = {
        "0": { "ref": "naturalidad",
                "valorRodal": valoresRodal.naturalidad.valor,
                "valorRodalComp": valoresRodalComp.naturalidad.valor,
                "desv": valoresRodalComp.naturalidad.valor_desv },
        "1": { "ref": "composicion",
                "valorRodal": valoresRodal.naturalidad.composicion.valor,
                "valorRodalComp": valoresRodalComp.naturalidad.composicion.valor,
                "desv": valoresRodalComp.naturalidad.composicion.valor_desv },
        "2": { "ref": "especies_arboreas",
                "valorRodal": valoresRodal.naturalidad.composicion.especies_arboreas.valor,
                "valorRodalComp": valoresRodalComp.naturalidad.composicion.especies_arboreas.valor,
                "desv": valoresRodalComp.naturalidad.composicion.especies_arboreas.valor_desv },
        "3": { "ref": "complejidad",
                "valorRodal": valoresRodal.naturalidad.complejidad.valor,
                "valorRodalComp": valoresRodalComp.naturalidad.complejidad.valor,
                "desv": valoresRodalComp.naturalidad.complejidad.valor_desv },
        "4": { "ref": "area_basimetrica",
                "valorRodal": valoresRodal.naturalidad.complejidad.area_basimetrica.valor,
                "valorRodalComp": valoresRodalComp.naturalidad.complejidad.area_basimetrica.valor,
                "desv": valoresRodalComp.naturalidad.complejidad.area_basimetrica.valor_desv },
        "5": { "ref": "estratificacion_vertical",
                "valorRodal": valoresRodal.naturalidad.complejidad.estratificacion_vertical.valor,
                "valorRodalComp": valoresRodalComp.naturalidad.complejidad.estratificacion_vertical.valor,
                "desv": valoresRodalComp.naturalidad.complejidad.estratificacion_vertical.valor_desv },
        "6": { "ref": "diversidad_estructural",
                "valorRodal": valoresRodal.naturalidad.complejidad.diversidad_estructural.valor,
                "valorRodalComp": valoresRodalComp.naturalidad.complejidad.diversidad_estructural.valor,
                "desv": valoresRodalComp.naturalidad.complejidad.diversidad_estructural.valor_desv },
        "7": { "ref": "senectud",
                "valorRodal": valoresRodal.naturalidad.senectud.valor,
                "valorRodalComp": valoresRodalComp.naturalidad.senectud.valor,
                "desv": valoresRodalComp.naturalidad.senectud.valor_desv },
        "8": { "ref": "arb_tam_excep",
                "valorRodal": valoresRodal.naturalidad.senectud.arb_tam_excep.valor,
                "valorRodalComp": valoresRodalComp.naturalidad.senectud.arb_tam_excep.valor,
                "desv": valoresRodalComp.naturalidad.senectud.arb_tam_excep.valor_desv },
        "9": { "ref": "abund_mad_muerta",
                "valorRodal": valoresRodal.naturalidad.senectud.abund_mad_muerta.valor,
                "valorRodalComp": valoresRodalComp.naturalidad.senectud.abund_mad_muerta.valor,
                "desv": valoresRodalComp.naturalidad.senectud.abund_mad_muerta.valor_desv },
        "10": { "ref": "prop_madera_muerta",
                "valorRodal": valoresRodal.naturalidad.senectud.prop_madera_muerta.valor,
                "valorRodalComp": valoresRodalComp.naturalidad.senectud.prop_madera_muerta.valor,
                "desv": valoresRodalComp.naturalidad.senectud.prop_madera_muerta.valor_desv },
        "11": { "ref": "micro_habitats",
                "valorRodal": valoresRodal.naturalidad.micro_habitats.valor,
                "valorRodalComp": valoresRodalComp.naturalidad.micro_habitats.valor,
                "desv": valoresRodalComp.naturalidad.micro_habitats.valor_desv },
        "12": { "ref": "mh_pies_vivos",
                "valorRodal": valoresRodal.naturalidad.micro_habitats.mh_pies_vivos.valor,
                "valorRodalComp": valoresRodalComp.naturalidad.micro_habitats.mh_pies_vivos.valor,
                "desv": valoresRodalComp.naturalidad.micro_habitats.mh_pies_vivos.valor_desv },
        "13": { "ref": "dinamica",
                "valorRodal": valoresRodal.naturalidad.dinamica.valor,
                "valorRodalComp": valoresRodalComp.naturalidad.dinamica.valor,
                "desv": valoresRodalComp.naturalidad.dinamica.valor_desv },
        "14": { "ref": "ciclo_silvogen",
                "valorRodal": valoresRodal.naturalidad.dinamica.ciclo_silvogen.valor,
                "valorRodalComp": valoresRodalComp.naturalidad.dinamica.ciclo_silvogen.valor,
                "desv": valoresRodalComp.naturalidad.dinamica.ciclo_silvogen.valor_desv },

        "15": { "ref": "huellaHumana",
                "valorRodal": valoresRodal.huellaHumana.valor,
                "valorRodalComp": valoresRodalComp.huellaHumana.valor,
                "desv": valoresRodalComp.huellaHumana.valor_desv },
        "16": { "ref": "antigua",
                "valorRodal": valoresRodal.huellaHumana.antigua.valor,
                "valorRodalComp": valoresRodalComp.huellaHumana.antigua.valor,
                "desv": valoresRodalComp.huellaHumana.antigua.valor_desv },
        "17": { "ref": "cont_temp",
                "valorRodal": valoresRodal.huellaHumana.antigua.cont_temp.valor,
                "valorRodalComp": valoresRodalComp.huellaHumana.antigua.cont_temp.valor,
                "desv": valoresRodalComp.huellaHumana.antigua.cont_temp.valor_desv },
        "18": { "ref": "usos_agropast",
                "valorRodal": valoresRodal.huellaHumana.antigua.usos_agropast.valor,
                "valorRodalComp": valoresRodalComp.huellaHumana.antigua.usos_agropast.valor,
                "desv": valoresRodalComp.huellaHumana.antigua.usos_agropast.valor_desv },
        "19": { "ref": "ant_usos_forestales",
                "valorRodal": valoresRodal.huellaHumana.antigua.usos_forestales.valor,
                "valorRodalComp": valoresRodalComp.huellaHumana.antigua.usos_forestales.valor,
                "desv": valoresRodalComp.huellaHumana.antigua.usos_forestales.valor_desv },
        "20": { "ref": "reciente",
                "valorRodal": valoresRodal.huellaHumana.reciente.valor,
                "valorRodalComp": valoresRodalComp.huellaHumana.reciente.valor,
                "desv": valoresRodalComp.huellaHumana.reciente.valor_desv },
        "21": { "ref": "rec_usos_forestales",
                "valorRodal": valoresRodal.huellaHumana.reciente.usos_forestales.valor,
                "valorRodalComp": valoresRodalComp.huellaHumana.reciente.usos_forestales.valor,
                "desv": valoresRodalComp.huellaHumana.reciente.usos_forestales.valor_desv },
        "22": { "ref": "especies_inv",
                "valorRodal": valoresRodal.huellaHumana.reciente.especies_inv.valor,
                "valorRodalComp": valoresRodalComp.huellaHumana.reciente.especies_inv.valor,
                "desv": valoresRodalComp.huellaHumana.reciente.especies_inv.valor_desv },
        "23": { "ref": "causa_fragment",
                "valorRodal": valoresRodal.huellaHumana.reciente.causa_fragment.valor,
                "valorRodalComp": valoresRodalComp.huellaHumana.reciente.causa_fragment.valor,
                "desv": valoresRodalComp.huellaHumana.reciente.causa_fragment.valor_desv },
        "24": { "ref": "actv_cineget",
                "valorRodal": valoresRodal.huellaHumana.reciente.actv_cineget.valor,
                "valorRodalComp": valoresRodalComp.huellaHumana.reciente.actv_cineget.valor,
                "desv": valoresRodalComp.huellaHumana.reciente.actv_cineget.valor_desv },
        "25": { "ref": "herv_rom",
                "valorRodal": valoresRodal.huellaHumana.reciente.herv_rom.valor,
                "valorRodalComp": valoresRodalComp.huellaHumana.reciente.herv_rom.valor,
                "desv": valoresRodalComp.huellaHumana.reciente.herv_rom.valor_desv },
        "26": { "ref": "frecuent",
                "valorRodal": valoresRodal.huellaHumana.reciente.frecuent.valor,
                "valorRodalComp": valoresRodalComp.huellaHumana.reciente.frecuent.valor,
                "desv": valoresRodalComp.huellaHumana.reciente.frecuent.valor_desv },
        "27": { "ref": "durab_usos",
                "valorRodal": valoresRodal.huellaHumana.reciente.durab_usos.valor,
                "valorRodalComp": valoresRodalComp.huellaHumana.reciente.durab_usos.valor,
                "desv": valoresRodalComp.huellaHumana.reciente.durab_usos.valor_desv },

        "28": { "ref": "integridadEspacial",
                "valorRodal": valoresRodal.integridadEspacial.valor,
                "valorRodalComp": valoresRodalComp.integridadEspacial.valor,
                "desv": valoresRodalComp.integridadEspacial.valor_desv },
        "29": { "ref": "tamano",
                "valorRodal": valoresRodal.integridadEspacial.tamano.valor,
                "valorRodalComp": valoresRodalComp.integridadEspacial.tamano.valor,
                "desv": valoresRodalComp.integridadEspacial.tamano.valor_desv },
        "30": { "ref": "cont_forest",
                "valorRodal": valoresRodal.integridadEspacial.cont_forest.valor,
                "valorRodalComp": valoresRodalComp.integridadEspacial.cont_forest.valor,
                "desv": valoresRodalComp.integridadEspacial.cont_forest.valor_desv },
        "31": { "ref": "efect_borde",
                "valorRodal": valoresRodal.integridadEspacial.efect_borde.valor,
                "valorRodalComp": valoresRodalComp.integridadEspacial.efect_borde.valor,
                "desv": valoresRodalComp.integridadEspacial.efect_borde.valor_desv },
        "32": { "ref": "conect",
                "valorRodal": valoresRodal.integridadEspacial.conect.valor,
                "valorRodalComp": valoresRodalComp.integridadEspacial.conect.valor,
                "desv": valoresRodalComp.integridadEspacial.conect.valor_desv },
        /*"33": { "ref": "composicion",
                "valorRodal": valoresRodal.composicion.valor,
                "valorRodalComp": valoresRodalComp.composicion.valor,
                "desv": valoresRodalComp.composicion.valor_desv },*/

    }
    crearGraficos(testJson);
}

/*var recorrerDataGraph = function(nom_pare, element, element2){
      jQuery.each(element, function(i, actual) {
        if(i === 'valor' || i === 'valor_desv'){
          return;
        }else{
            nom_complet = i;
            //console.log(nom_complet +' '+ element[i].valor +' '+ element[i].valor_desv);
            //console.log(i);
            recorrerDataGraph(nom_complet, actual);
        }

      });

      jQuery.each(element2, function(z, actual) {
        if(z === 'valor' || z === 'valor_desv'){
          return;
        }else{
          nom_complet = z;

          console.log(element2[z].valor);
          recorrerDataGraph(nom_complet, actual);
        }

      });
};
*/


var createMinorTick = function(svgContainer, x_value, i){
    var tick = svgContainer.append("line").attr("x1", x_value + 10).attr("y1", 5).attr("x2", x_value + 10).attr("y2", 15).attr("stroke-width", 1.5).attr("stroke", "#262626");
    var textInfo = svgContainer.append("text").attr("x", x_value + 10).attr("y", 35).attr("font-size", "12px").attr("text-anchor", "middle").text(i);
};


var crearPuntos = function(svgContainer, ref, valorRodal, valorRodalComp, desv){
    var colorCircle = [' ','black', '#9ac635'];

    var div = d3.select("body").append("div").attr("class", "tooltip").style("opacity", 0);

    valorRodal = valorRodal*50;
    valorRodalComp = valorRodalComp*50;
    desv = desv*50;

    var circle = svgContainer.append("circle").attr("cx", valorRodal + 10).attr("cy", 10).attr("r", 8).style("fill", colorCircle[1]).on("mouseover", function(d) {
            div.transition()
                .duration(200)
                .style("opacity", 2);
            div .html("Valor: " + valorRodal/50)
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY ) + "px")
                .style("background-color", "black")
                .style("position", "absolute")
                .style("width", "100px")
                .style("height", "20px")
                .style("border-radius", "5px")
                .style("text-align", "center")
                .style("padding", "1px").style("font-size", "14px").style("pointer-event", "none").style("font-family", "Open Sans, Arial, sans-serif")
                .style("color", "white");
            })
        .on("mouseout", function(d) {
            div.transition()
                .duration(500)
                .style("opacity", 0);

    });

    var circle1 = svgContainer.append("circle").attr("cx", valorRodalComp + 10).attr("cy", 10).attr("r", 6).style("fill", colorCircle[2]).on("mouseover", function(d) {
            div.transition()
                .duration(200)
                .style("opacity", 2);
            div .html("Valor: " + valorRodalComp/50 + "<br>" + "Desv.: " + (desv/50).toFixed(2))
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY) + "px")
                .style("background-color", "#9ac635")
                .style("position", "absolute")
                .style("width", "120px")
                .style("height", "45px")
                .style("border-radius", "5px")
                .style("text-align", "center")
                .style("padding", "3px").style("font-size", "14px").style("pointer-event", "none").style("font-family", "Open Sans, Arial, sans-serif")
                .style("color", "black");;
            })
        .on("mouseout", function(d) {
            div.transition()
                .duration(500)
                .style("opacity", 0);

    });

    var leftDesv = svgContainer.append("line").attr("x1", valorRodalComp + 10).attr("y1", 10).attr("x2", (valorRodalComp-desv) + 10).attr("y2", 10).attr("stroke-width", 1.5).attr("stroke", colorCircle[2]);
    var leftDesvTick = svgContainer.append("line").attr("x1", (valorRodalComp-desv) + 10).attr("y1", 5).attr("x2", (valorRodalComp-desv) + 10).attr("y2", 15).attr("stroke-width", 1.5).attr("stroke", colorCircle[2]);
    var rightDesv = svgContainer.append("line").attr("x1", (valorRodalComp+desv) + 10).attr("y1", 10).attr("x2", valorRodalComp + 10).attr("y2", 10).attr("stroke-width", 1.5).attr("stroke", colorCircle[2]);
    var rightDesvTick = svgContainer.append("line").attr("x1", (valorRodalComp+desv) + 10).attr("y1", 5).attr("x2", (valorRodalComp+desv) + 10).attr("y2", 15).attr("stroke-width", 1.5).attr("stroke", colorCircle[2]);
};


var crearGraficos = function(testJson){

    var sizeTestJson = Object.keys(testJson).length;

    for (x=0; x<sizeTestJson; x++){
        var svgContainer = d3.select("."+testJson[x].ref).append("svg").attr("width", 520).attr("height", 35).attr("top", 15).attr("left", 50);

        var axis = svgContainer.append("line").attr("x1", 0).attr("y1", 10).attr("x2", 520).attr("y2", 10).attr("stroke-width", 1.5).attr("stroke", "#262626");
        var leftTick = svgContainer.append("line").attr("x1", 10).attr("y1", 0).attr("x2", 10).attr("y2", 20).attr("stroke-width", 2.5).attr("stroke", "#262626");
        var rightTick = svgContainer.append("line").attr("x1", 510).attr("y1", 0).attr("x2", 510).attr("y2", 20).attr("stroke-width", 2.5).attr("stroke", "#262626");
        var centerTick = svgContainer.append("line").attr("x1", 260).attr("y1", 0).attr("x2", 260).attr("y2", 20).attr("stroke-width", 2).attr("stroke", "#262626");

        for(var i = 0; i <= 10; i++){
            var minorTick = createMinorTick(svgContainer,i*50, i);
        }



        if(isNaN(testJson[x].desv) || testJson[x].valorRodal == null){
            testJson[x].desv = 0;

        }

        if(isNaN(testJson[x].valorRodal) || testJson[x].valorRodal == null ){
            testJson[x].valorRodal = 100;
        }

        if(isNaN(testJson[x].valorRodalComp) || testJson[x].valorRodalComp == null ){
            testJson[x].valorRodalComp = 100;
        }


        console.log(testJson[x].valorRodal +' - '+ testJson[x].valorRodalComp + ' - ' + testJson[x].desv);
        crearPuntos(svgContainer, testJson[x].ref, testJson[x].valorRodal, testJson[x].valorRodalComp, testJson[x].desv);
    }

}
