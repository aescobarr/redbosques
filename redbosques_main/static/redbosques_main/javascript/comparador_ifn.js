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
    //console.log(idHabitat);
    //console.log(idComAut);
    //console.log(idRegBiogeo);
    //console.log(valRod);

    //console.log(valComAut_Comp);
    //console.log(valRegBio_Comp);



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

        console.log(url);

        if(valRod == "null"){
            resetUITable();
        }else{
            resetUITable();
            $('.graphsTree').addClass("asyncload-big");

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
                    console.log(test);
                    console.log(valMet);

                    graficaTEST(test);
                    graficaValoresMetricos(valMet);


                    $('.graphsTree').removeClass("asyncload-big");
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
    console.log(test);
    for(i=0; i<test.length; i++){
        ind = test[i][Object.keys(test[i])[0]]['ind'];
        parcelas = test[i][Object.keys(test[i])[0]]['ifn'];
        rodal = test[i][Object.keys(test[i])[0]]['rod'];

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

        /*nombre = [["0", 0],
                ["1", test[i].ifn['1.0']],
                ["2", test[i].ifn['2.0']],
                ["3", test[i].ifn['3.0']],
                ["4", test[i].ifn['4.0']],
                ["5", test[i].ifn['5.0']],
                ["6", test[i].ifn['6.0']],
                ["7", test[i].ifn['7.0']],
                ["8", test[i].ifn['8.0']],
                ["9", test[i].ifn['9.0']],
                ["10", test[i].ifn['10.0']]
        ];*/

        grafconst(ind, nombre, rodal);
    }
}

/*var graficaValoresMetricos = function(valMet){
    for(i=0; i<valMet.length; i++){

        console.log(valMet);

        ind = valMet[i]['ind'];
        interv = valMet[i]['interv'];
        valores = valMet[i]['valores'];

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


    grafconstvalmet(ind, valores);

    }


}*/

var grafconst = function(ind, parcelas, rodal){

    indGrafica = 'grafica_' + ind;

    Highcharts.chart(indGrafica, {
        chart: {
            type: 'column',
            height: 150,
        },
        exporting: { enabled: false },
        title: {
            text: ' '
        },
        xAxis: {
            title: {
                text: 'Puntuación'
            },
            type: 'category',
            labels: {
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif'
                }
            },
            plotLines: [{
                color: '#339933',
                width: 2,
                value: Object.keys(rodal),
                zIndex: 5,
                events: {
                    click: function () {
                        //alert("HOLA");
                    },
                    mouseover: function () {
                        //alert("in");
                    },
                    mouseout: function () {
                        //alert("out");
                    }
                }
            }]
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Cantidad'
            }
        },
        plotOptions: {
           series: {
             groupPadding: 0,
             pointPadding: 0.1,
             borderWidth: 0
           }
        },
        legend: {
            enabled: false
        },
        tooltip: {
            pointFormat: 'Número de parcelas: <b>{point.y}</b>'
        },
        series: [{
            name: ' ',
            data: parcelas,
            color: '#FF6600'
        }]
    });

}


var graficaValoresMetricos = function(valMet){
    for(i=0; i<valMet.length; i++){
        indGrafica = 'grafica_' + valMet[i]['ind'] + '_valMet';
        valores = valMet[i]['valores'];

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

        Highcharts.chart(indGrafica, {
            chart: {
                type: 'column',
                height: 150,
            },
            exporting: { enabled: false },
            title: {
                text: ' '
            },
            xAxis: {
                title: {
                    text: 'Puntuación'
                },
                type: 'category',
                labels: {
                    style: {
                        fontSize: '13px',
                        fontFamily: 'Verdana, sans-serif'
                    }
                },
                plotLines: [{
                    color: '#339933',
                    width: 2,
                    //value: Object.keys(rodal),
                    value: 5,
                    zIndex: 5,
                    events: {
                        click: function () {
                            //alert("HOLA");
                        },
                        mouseover: function () {
                            //alert("in");
                        },
                        mouseout: function () {
                            //alert("out");
                        }
                    }
                }]
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Cantidad'
                }
            },
            plotOptions: {
               series: {
                 groupPadding: 0,
                 pointPadding: 0.1,
                 borderWidth: 0
               }
            },
            legend: {
                enabled: false
            },
            /*tooltip: {
                pointFormat: 'Número de parcelas: <b>{point.y}</b>'
            },*/
            series: [{
                name: ' ',
                data: valores,
                color: '#FF6600'
            }]
        });
    }
}


function rodalData(valRod, valComAut_Comp, valRegBio_Comp){
    //var rodPrincip = valRod;
    var idHabitat = $('#habitat').val();

    var idComAut = $('#selector_ComAut').val();
    var idRegBiogeo = $('#selector_RegBio').val();

    load_rodal_ref(idHabitat, idComAut, idRegBiogeo, valRod);
}

