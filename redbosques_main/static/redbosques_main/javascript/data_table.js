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


    url = 'http://127.0.0.1:8000/redbosques/valorRef';

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
            $('.naturalidad').html(rodalReferencia.naturalidad.valor);
            recorreArbre('', rodalReferencia);
            recorreRodal('', valores_rodal_jason);
            calcDiferencia();
        },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
};






var recorreArbre = function(nom_pare, element){
      jQuery.each(element, function(i, actual) {
        if(i === 'valor'){
          return;
        }else{
          if(nom_pare === ''){
            nom_complet = i;
          }else{
            nom_complet = nom_pare + "_" + i;
          }

          //console.log("Nom de l'element: " + nom_complet);
          //console.log("Valor de l'element: " + element[i].valor);


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
    //console.log("rodal:" + rodal.naturalidad);
    //console.log("rodal referencia:" + rodRef.naturalidad);
    resComp = [];


    var test = rodal.naturalidad - rodRef.naturalidad;

    //console.log(test);

    for(var key in rodal) {
        var value = rodal[key];
        var value2 = rodRef[key];

        //console.log(key +':'+ value);
        //console.log(key +':'+ value2);
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

        /*console.log(key +':'+ value);
        console.log(key +':'+ value2);*/
        //resta =  value - value2;
        //console.log("resta: " + resta);

        var elem = {};
        elem[key+'_dif'] = resta;

        //$('#' + key+'_dif').html(resta);
        resComp.push(elem);
    }
    //console.log(resComp);
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

        /*var pathArray = window.location.pathname.split('/');
        console.log(pathArray[3]);*/

        //url = 'http://127.0.0.1:8000/redbosques/comparador/'+ pathArray[3]+'/';

        valIdRodal = $('p.rodalSelected').attr('value');
        console.log(valIdRodal);


        url = 'http://127.0.0.1:8000/redbosques/setFiltrosRodal?idR=' + valIdRodal;


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