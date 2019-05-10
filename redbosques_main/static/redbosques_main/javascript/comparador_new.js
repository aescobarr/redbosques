$(document).ready(function(){


});

function load_rodal_ref(idHabitat, idComAut, idRegBiogeo, valRod, rodPrincip){
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
    if(rodPrincip != "null"){
        params.push('rodPrincip='+escape(rodPrincip));
    }

    //params.push('rodRef='+escape(rodRef));

    url = url + "?" + params.join('&');

    if(valRod == "null"){
        resetUITable();
    }else{
        resetUITable();
        $('.data-table').addClass("asyncload-big");
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
                //recorreRodal('', rodalSelData);
                if(rodalSelData){
                    if(rodalReferencia != null){
                        calcDiferencia();
                        $('.grafico div').html('');
                        dataGraph(rodalSelData, rodalReferencia);
                    }else{
                        $('.grafico div').html('');
                        $('td.diff-col').html('---');
                        $('td.col-diff').html('---');
                        $('td.col-diff').css("background-color", "#FFFFFF");
                        $('td.diff-col').css("background-color", "#FFFFFF");
                        $('.valGraf').html('---');
                        $('.valGraf').css("background-color", "#FFFFFF");
                    }
                }
                if (valRod == "null"){
                    $('td.diff-col').html('---');
                    $('td.col-diff').html('---');
                }
                $('.data-table').removeClass("asyncload-big");
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
                $('.data-table').removeClass("asyncload-big");
            }
        });
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

function rodalData(valorRodal){
    if(valorRodal == 'null'){
        //clear taula
        $('.bgColorRod').html('');
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
            success: function( data, textStatus, jqXHR ) {
                rodalSelData = data.rodal;
                recorreRodal('', rodalSelData);
                if(rodalReferencia){
                    calcDiferencia();
                    $('.grafico div').html('');
                    dataGraph(rodalSelData, rodalReferencia);
                }
                $('.data-table').removeClass("asyncload-big");
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
                $('.data-table').removeClass("asyncload-big");
            }
        });
    }
};