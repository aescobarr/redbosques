$(document).ready(function(){

});


var rodalName = [];
var rodalNameRef = [];

function dataSelected(valorRodal, valRodComp){

}


var blockSelectores = function(){
    $('.scatterSelector').attr('disabled', 'disabled');
    $('.barChartselector').attr('disabled', 'disabled');
}

var unblockSelectores = function(){
    $('.scatterSelector').removeAttr('disabled');
    $('.barChartselector').removeAttr('disabled');
}


function load_rodal_ref(valRod, valComAut_Comp, valRegBio_Comp, idHabitat, idComAut, idRegBiogeo){

    if(valRod != "null"){
        url = _rodal_IFN;
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

        if(valComAut_Comp != "null"){
            params.push('comAutComp='+escape(valComAut_Comp));
        }

        if(valRod != "null"){
            params.push('vr='+escape(valRod));
        }

        if(valRegBio_Comp != "null"){
            params.push('regBiogeoComp='+escape(valRegBio_Comp));
        }

        url = url + "?" + params.join('&');

        if(valRod == "null"){
            resetUITable();
        }else{
            resetUITable();
            //$('.graphsTree').addClass("asyncload-big");
            $('.ifnGraphCont').css("height", "315px");
            $('.spinner').addClass("asyncload-big");
            /*if(valRod == rodPrincip){
                alert("La selección de rodales no es correcta");
                $("#selector_rodales_comp").val('null');
                $('.data-table').removeClass("asyncload-big");
            }else{*/
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
                    test = data.data;
                    valMet = data.valoresMetricos;
                    nombreRodal = data.nombreRodal;



                    graficaTEST(test, nombreRodal);

                    for(i=0; i<valMet.length; i++){
                        graficaValoresMetricos(valMet[i]);
                    }

                    //$('.graphsTree').removeClass("asyncload-big");
                    $('.spinner').removeClass("asyncload-big");
                },
                error: function(jqXHR, textStatus, errorThrown){
                    console.log(errorThrown);
                    $('.graphsTree').removeClass("asyncload-big");
                }
            });
        }
    }
};


function resetUITable(){
        $('td.diff-col').html('---');
        $('td.col-diff').html('---');
        $('.valGraf').html('---');
        $('.valGraf').css("background-color", "#FFFFFF");
        $('.divGraf').empty();
        $('.col-diff').removeAttr("style");
        $('.diff-col').removeAttr("style");
}

var graficaTEST = function(test){
    for(i=0; i<test.length; i++){
        ind = test[i][Object.keys(test[i])[0]]['ind'];
        parcelas = test[i][Object.keys(test[i])[0]]['ifn'];
        r = parseFloat(Object.keys(test[i][Object.keys(test[i])[0]]['rod']));
        textCord = test[i][Object.keys(test[i])[0]]['cordText'];

        rodal = [r, 0];

        if (!parcelas['0.0']){ parcelas['0.0'] = 0; }
        if (!parcelas['1.0']){ parcelas['1.0'] = 0; }
        if (!parcelas['2.0']){ parcelas['2.0'] = 0; }
        if (!parcelas['3.0']){ parcelas['3.0'] = 0; }
        if (!parcelas['4.0']){ parcelas['4.0'] = 0; }
        if (!parcelas['5.0']){ parcelas['5.0'] = 0; }
        if (!parcelas['6.0']){ parcelas['6.0'] = 0; }
        if (!parcelas['7.0']){ parcelas['7.0'] = 0; }
        if (!parcelas['8.0']){ parcelas['8.0'] = 0; }
        if (!parcelas['9.0']){ parcelas['9.0'] = 0; }
        if (!parcelas['10.0']){ parcelas['10.0'] = 0; }

        nombre = [["0", parcelas['0.0']],
                ["1", parcelas['1.0']],
                ["2", parcelas['2.0']],
                ["3", parcelas['3.0']],
                ["4", parcelas['4.0']],
                ["5", parcelas['5.0']],
                ["6", parcelas['6.0']],
                ["7", parcelas['7.0']],
                ["8", parcelas['8.0']],
                ["9", parcelas['9.0']],
                ["10", parcelas['10.0']]
        ];
        grafconst(ind, nombre, rodal, textCord);
    }
}

var grafconst = function(ind, parcelas, rodal, textCord){

    indGrafica = 'grafica_' + ind;

    Highcharts.chart(indGrafica, {
        chart: {
            type: 'column',
            height: 250,

        },
        exporting: { enabled: false },
        title: { text: ' ' },
        xAxis: [{

            title: { text: textCord },
            type: 'category',
            labels: {
                style: {
                    fontSize: '10px',
                    fontFamily: 'Verdana, sans-serif'
                }
            },
        },{
            title: { text: textCord + ' del rodal' },
            alignTicks: true,
            opposite: true,
            tickAmount: 11,
            /*tickInterval: 1*/
            min: 0,
            max: 10

        }],

        yAxis: [{
            title: { text: 'nº de parcelas' },
            min: 0
        },{
            title: { text: ' ' },
            opposite: true,
            min: 0,
            max: 10,
            reversed: true,
            visible: false
        }
        ],
        /*plotOptions: {
           series: {
             groupPadding: 0,
             pointPadding: 0.1,
             borderWidth: 0,
             minPointLength: 3
           }
        },*/
        legend: {
            enabled: false
        },
        tooltip: {
            pointFormat: 'Número de parcelas: <b>{point.y}</b>'
        },
        series: [{
            name: ' ',
            data: parcelas,
            color: '#FF6600',
            groupPadding: 0,
            pointPadding: 0.1,
            borderWidth: 0,
            minPointLength: 3,
            tooltip: {
                useHTML: true,
                headerFormat: '<span>Nº de parcelas: <b>{point.y}</b></span><br>',
                pointFormat: '<span>Valor: <b>{point.x}</b></span>'
            }
        },{
            name: ' ',
            type: 'scatter',
            data: [rodal],
            xAxis: 1,
            yAxis: 1,
            zIndex: -1,
            marker: {
                radius: 6,
                fillColor: 'green'
            },
            tooltip: {
                useHTML: true,
                headerFormat: '<span style="font-weight: bold; color: #339933">'+ nombreRodal +'</span><br>',
                pointFormat: '<span>Valor: <b>{point.x}</b></span>'
            }

        }]
    });

}


var graficaValoresMetricos = function(valMetInd){
    var valMetInd = valMetInd;
    //for(i=0; i<valMet.length; i++){
    indGrafica = 'grafica_' + valMetInd['ind'] + '_valMet';

    valores = valMetInd['valores'];
    r = parseFloat(Object.keys(valMetInd['rodalValue'])[0]);
    //r = parseInt(Object.keys(valMetInd['rodalValue'])[0]);
    textCord = valMetInd["cordText"];
    rodal = [r, 0];

    if (!valores['0.0']){ valores['0.0'] = 0; }
    if (!valores['1.0']){ valores['1.0'] = 0; }
    if (!valores['2.0']){ valores['2.0'] = 0; }
    if (!valores['3.0']){ valores['3.0'] = 0; }
    if (!valores['4.0']){ valores['4.0'] = 0; }
    if (!valores['5.0']){ valores['5.0'] = 0; }
    if (!valores['6.0']){ valores['6.0'] = 0; }
    if (!valores['7.0']){ valores['7.0'] = 0; }
    if (!valores['8.0']){ valores['8.0'] = 0; }
    if (!valores['9.0']){ valores['9.0'] = 0; }
    if (!valores['10.0']){ valores['10.0'] = 0; }

    nombre = [["0", valores['0.0']],
            ["1", valores['1.0']],
            ["2", valores['2.0']],
            ["3", valores['3.0']],
            ["4", valores['4.0']],
            ["5", valores['5.0']],
            ["6", valores['6.0']],
            ["7", valores['7.0']],
            ["8", valores['8.0']],
            ["9", valores['9.0']],
            ["10", valores['10.0']]
    ];

    var tickintervals = Number((valMetInd['interv'][0]['interv'][0][1] - valMetInd['interv'][0]['interv'][0][0])/2).toFixed(1);
    var tickintervalsRodal = parseFloat(tickintervals);
    //console.log(tickintervalsRodal);
    var valMinEje = valMetInd['intervEje'][0][0];
    var valMaxEje = valMetInd['intervEje'][10][0];
    //console.log(valMinEje);
    //console.log(valMaxEje);


        Highcharts.chart(indGrafica, {
            chart: {
            type: 'column',
            height: 250,

        },
            title: {text: ''},
            exporting: { enabled: false },
            legend: {enabled: false},

        /* *********************************** EJE X *********************************** */
            xAxis: [{
                title: { text: textCord },
                id: 'ifn_x',
                type: 'column',
                categories: valMetInd['intervEje'],
                min: 0,
                max: 10,
            },{
              id: 'rodal_x',
              title: { text: textCord + ' del rodal' },
              type: 'scatter',
              //categories: [[0.2],[0.7],[1.2],[1.6],[2.1],[2.5],[3],[3.5],[3.9],[4.4],[4.8]],
              pointStart: valMinEje,
              //pointInterval: 1,
              opposite: true,
              min: 0,
              max: valMaxEje,
              allowDecimals: true
            }],
/* *********************************** EJE Y *********************************** */
        yAxis: [{
          	id: 'ifn_y',
            title: { text: 'nº de parcelas'}
        }, {
          	id: 'rodal_y',
          	title: {text: ' '},
            opposite: true,
            reversed: true,
            visible: false
        }],
/* *********************************** DATOS *********************************** */
        series: [{
            name: ' ',
            type: 'column',
            xAxis: 'ifn_x',
            yAxis: 'ifn_y',
            data: valores,
            color: '#FF6600',
            groupPadding: 0,
            pointPadding: 0.1,
            borderWidth: 0,
            minPointLength: 3,
            tooltip: {
                useHTML: true,
                headerFormat: '<span>Nº de parcelas: <b>{point.y}</b></span><br>',
                pointFormat: '<span>Valor: <b>{point.x}</b></span>'
            }
        },{
            name: ' ',
            type: 'scatter',
            xAxis: 'rodal_x',
            yAxis: 'rodal_y',
            data: [rodal],
            marker: {
                radius: 6,
                fillColor: 'green'
            },
            tooltip: {
                useHTML: true,
                headerFormat: '<span style="font-weight: bold; color: #339933">'+ nombreRodal +'</span><br>',
                pointFormat: '<span>Valor: <b>{point.x}</b></span>'
            }
        }]
    });
};



function rodalData(valRod, valComAut_Comp, valRegBio_Comp){
    //var rodPrincip = valRod;
    var idHabitat = $('#habitat').val();

    var idComAut = $('#selector_ComAut').val();
    var idRegBiogeo = $('#selector_RegBio').val();

    load_rodal_ref(idHabitat, idComAut, idRegBiogeo, valRod);
}


$('.lv1').on("click", function(){

    var classLvl = this.className;

    if(classLvl == "lv1 lv1Nat"){
        $('.lv2Nat').toggle();
    }

    var validation = $('.lv2Nat').css("display");

    if(($('.lv2Nat').css("display")) == "none"){
        $('.lv3Nat').hide();
    }

});

$('.lv2').on("click", function(){
    var classLvl2 = this.className;

    if(classLvl2 == "lv2 lv2Nat"){
        $('.lv3Nat').toggle();
    }
});

$('.showAll').on("click", function(){
    $('.lv2Nat').toggle();

    var validation = $('.lv2Nat').css("display");

    if(($('.lv2Nat').css("display")) == "none"){
        $('.lv3Nat').hide();
    }
});

$('.hideAll').on("click", function(){
    $('.lv2Nat').hide();
});


/*$(".popupInfo").click(function(){

    $("#instruc").dialog({
      modal: true,
      buttons: {
        Cerrar: function() {
          $( this ).dialog( "close" );
        }
      },
      draggable: false,
      classes: {
            "ui-dialog": "popupInstrucciones"
      }
    });

});*/
