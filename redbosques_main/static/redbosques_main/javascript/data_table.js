$(document).ready(function() {
});

$('tr.lv1').on("click", function(){

    var classLvl = this.className;

    if(classLvl == "lv1 lv1Nat"){
        $('.lv2Nat').toggle();
    }else if(classLvl == "lv1 lv1Hh"){
        $('.lv2Hh').toggle();
    }else if(classLvl == "lv1 lv1Ie"){
        $('.lv2Ie').toggle();
    }

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

    if(classLvl2 == "lv2 lv2Nat"){
        $('.lv3Nat').toggle();
    }else if(classLvl2 == "lv2 lv2Hh"){
        $('.lv3Hh').toggle();
    }
});

$('.showAll').on("click", function(){
    $('.lv2Nat').toggle();
    $('.lv2Hh').toggle();
    $('.lv2Ie').toggle();
    var validation = $('.lv2Nat').css("display");

    if(($('.lv2Nat').css("display")) == "none"){
        $('.lv3Nat').hide();
    }

    if(($('.lv2Hh').css("display")) == "none"){
        $('.lv3Hh').hide();
    }
});

$('.hideAll').on("click", function(){
    $('.lv2Nat').hide();
    $('.lv2Hh').hide();
    $('.lv2Ie').hide();
});

/* Recorre l'arbre de dades del rodal a comparar */
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
            $('#' + nom_complet).html('---');
            element[i].valor = (null);
        }else{
            var thirdColumnComp = $('#' + nom_complet).parent(".lv3").length;
            if (thirdColumnComp == 1){
                $('#' + nom_complet).html(element[i].valor);
            }else{
                $('#' + nom_complet).html((element[i].valor).toFixed(1));
            }
        }
          rodRef[nom_complet] = element[i].valor;
          recorreArbre(nom_complet, actual);
        }
      });

};

/* Recorre l'arbre de dades del rodal */
var recorreRodal = function(nom_pare, element){
jQuery.each(element, function(i, actual) {
        if(i === 'valor'){
          return;
        }else{
          if(nom_pare === ''){
            nom_complet = "_" + i;
          }else{
            nom_complet = nom_pare + "_" + i;
          }

          if (isNaN(element[i].valor)){
            $('#' + nom_complet).html('---');
            element[i].valor = ('null');
          }else{
            var thirdColumn = $('#' + nom_complet).parent(".lv3").length;

            if (thirdColumn == 1){
                $('#' + nom_complet).html(element[i].valor);
            }else{
                $('#' + nom_complet).html((element[i].valor).toFixed(1));
            }

          }
            rodal[nom_complet] = element[i].valor;
            recorreRodal(nom_complet, actual);
        }
      });

};


function calcDiferencia(){
    resComp = [];
    var test = rodal.naturalidad - rodRef.naturalidad;


    for(var key in rodRef) {
        var value = rodal["_"+key];
        var value2 = rodRef[key];




        if(isNaN(value) || isNaN(value2)){
            resta = null;
            $('#' + key+'_dif').html("---");
            $('#' + key+'_dif').css("background-color", "#CDCCC8");

        }else{
            resta =  value - value2;
            var resta_str = resta.toFixed(2);
            $('#' + key+'_dif').html(resta_str);

            if (key.split("_")[0] == "huellaHumana"){
                if(resta<0){
                    $('#' + key+'_dif').css("background-color", "#9ac635");
                }else if(resta >= 0){
                    $('#' + key+'_dif').css("background-color", "#EF3340");
                }
            }else{
                if(resta<0){
                    $('#' + key+'_dif').css("background-color", "#EF3340");
                }else if(resta >= 0){
                    $('#' + key+'_dif').css("background-color", "#9ac635");
                }
            }


        }
        var elem = {};
        elem[key+'_dif'] = resta;
        resComp.push(elem);

    }
}

$('.val-graf.valores').on("click", function(){
    if($('.tabla-datos').attr('style','display: none')){
        $('.tabla-datos').attr('style','display: block')
    }
     $('td.graf, th.graf').show();
     $('td.grafico, th.aux').hide();
     $('.tabla-datos-metrica').hide();
     $('.comp-graficas').hide();
});

$('.val-graf.grafica').on("click", function(){
    if($('.tabla-datos').attr('style','display: none')){
        $('.tabla-datos').attr('style','display: block')
    }
    $('td.graf, th.graf').hide();
    $('td.grafico, th.aux').show();
    $('.tabla-datos-metrica').hide();
    $('.comp-graficas').hide();
});

$('.val-metr.metrica').on("click", function(){
    $('.tabla-datos').hide();
    $('.comp-graficas').hide();
    $('.tabla-datos-metrica').show();
});

$('.graf.graficas').on("click", function(){
    $('.tabla-datos').hide();
    $('.tabla-datos-metrica').hide();
    $('.comp-graficas').show();
});

var createMinorTick = function(svgContainer, x_value, i){
    var tick = svgContainer.append("line").attr("x1", x_value + 10).attr("y1", 5).attr("x2", x_value + 10).attr("y2", 15).attr("stroke-width", 1.5).attr("stroke", "#8c8c8c");
    var textInfo = svgContainer.append("text").attr("x", x_value + 10).attr("y", 35).attr("font-size", "10px").attr("text-anchor", "middle").text(i);
};

var crearPuntos = function(svgContainer, ref, valorRodal, valorRodalComp, desv){
    var colorCircle = [' ','#339933', '#FF6600'];

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
                .style("background-color", "#339933")
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
                .style("background-color", "#FF6600")
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

        var axis = svgContainer.append("line").attr("x1", 0).attr("y1", 10).attr("x2", 520).attr("y2", 10).attr("stroke-width", 1.5).attr("stroke", "#8c8c8c");
        var leftTick = svgContainer.append("line").attr("x1", 10).attr("y1", 4).attr("x2", 10).attr("y2", 18).attr("stroke-width", 2.5).attr("stroke", "#8c8c8c");
        var rightTick = svgContainer.append("line").attr("x1", 510).attr("y1", 4).attr("x2", 510).attr("y2", 18 ).attr("stroke-width", 2.5).attr("stroke", "#8c8c8c");
        var centerTick = svgContainer.append("line").attr("x1", 260).attr("y1", 4).attr("x2", 260).attr("y2", 18).attr("stroke-width", 2).attr("stroke", "#8c8c8c");

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
        crearPuntos(svgContainer, testJson[x].ref, testJson[x].valorRodal, testJson[x].valorRodalComp, testJson[x].desv);
    }
}