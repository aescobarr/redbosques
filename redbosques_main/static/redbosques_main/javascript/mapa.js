

$(document).ready(function() {

    setMapData = function(data){
        marker_cluster.clearLayers();

        /*###########################Icono##########################################*/

        var html_icon_0 = L.divIcon({className: "icon_0", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-tree icon_0 fa-2x"></i>'});
        var html_icon_1 = L.divIcon({className: "icon_1", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-tree icon_1 fa-2x"></i>'});
        var html_icon_2 = L.divIcon({className: "icon_2", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-tree icon_2 fa-2x"></i>'});
        var html_icon_3 = L.divIcon({className: "icon_3", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-tree icon_3 fa-2x"></i>'});
        var html_icon_4 = L.divIcon({className: "icon_4", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-tree icon_4 fa-2x"></i>'});
        var html_icon_5 = L.divIcon({className: "icon_5", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-tree icon_5 fa-2x"></i>'});
        var html_icon_6 = L.divIcon({className: "icon_6", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-tree icon_6 fa-2x"></i>'});
        var html_icon_7 = L.divIcon({className: "icon_7", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-tree icon_7 fa-2x"></i>'});
        var html_icon_8 = L.divIcon({className: "icon_8", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-tree icon_8 fa-2x"></i>'});
        var html_icon_9 = L.divIcon({className: "icon_9", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-tree icon_9 fa-2x"></i>'});
        var html_icon_10 = L.divIcon({className: "icon_10", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-tree icon_10 fa-2x"></i>'});
        var html_icon_default = L.divIcon({className: "icon_null", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-tree icon_null fa-2x"></i>'});

        //var html_icon_default = L.divIcon({className: "marker icon_null", iconAnchor: [0, 24], labelAnchor: [-6, 0], popupAnchor: [0, -36], html: '<span style="marker_style"></span>'});

        var taula_icons = {
            0: html_icon_0,
            1: html_icon_1,
            2: html_icon_2,
            3: html_icon_3,
            4: html_icon_4,
            5: html_icon_5,
            6: html_icon_6,
            7: html_icon_7,
            8: html_icon_8,
            9: html_icon_9,
            10: html_icon_10
        };

        /*#####################################################################################*/


        for(var i = 0; i < data.length; i++){
            var punt = data[i];

            var current_icon;
            if (punt.valor){
                current_icon = taula_icons[punt.valor];
            }else{
                current_icon = html_icon_default;
            }

            var marker = L.marker([punt.y,punt.x], {icon: current_icon}).bindPopup(
            '<b>Nombre habitad: </b>' + punt.habitat_nom + '<br><b>Localización: </b>' + punt.nombre + '<br><b>Comunidad Autónoma: </b>' + punt.Comunidad_autonoma +    '<br><a href="http://127.0.0.1:8000/redbosques/comparador/' + punt.id_rodal + '/"><b>Ver ficha</b></a>'
            );

             //url = 'http://127.0.0.1:8000/redbosques/datos_mapa';

            marker_cluster.addLayer(marker);
            mymap.addLayer(marker_cluster);
        }

       if (testData){
            testData.markerClusterGroup();
       }
    }

    var base = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
            maxZoom: 18,
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
                '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
                'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            id: 'mapbox.streets'
    });

    mymap = L.map('mapid', {
            center: [40.0000000, -4.0000000],
            zoom: 6,
            layers: [base],
    });

    marker_cluster = L.markerClusterGroup({
            spiderLegPolylineOptions: { weight: 1.5, color: '#222', opacity: 0.5 },
            spiderfyDistanceMultiplier: 3
    });

    //setMapData(data);
    updateMapData();
    selector_valoracion();

    //$('.tipo_habitad').append('<option class="tipo_bosque" value="empty" selected="selected"></option>');
    //$('.selector_rodal').append('<option class="rodal" value="null" selected="Selected">Selecciona un rodal</option>');

});

/*################Getters selectores#######################*/


var getEje = function(){
    var eje_sel = $('.selector_clasificacio').val();
    return eje_sel;
}

var getCodiRodal = function(){
    var codi_rodal = $('.selector_rodal').val();

    if(codi_rodal == ''){
        return null;
    }
    return codi_rodal;
}

var getTipoHabitat = function(){
    var tipo_habitat = $(".tipo_habitad").val();

    if(tipo_habitat == ''){
        return null;
    }else{
        //$('.selector_rodal').val('');
        return tipo_habitat;
    }
}


var getHabitatSel = function(){
    id_tipo_habitad_sel = $('.tipo_habitad_sel').val();
    //console.log(id_tipo_habitad_sel);

    if(id_tipo_habitad_sel == ''){
        return null;
    }else{

        return id_tipo_habitad_sel;
    }
}


var getValoracion = function (){
    //var valoresValoracion = $.each($('.val_button:checkbox:checked').val());

    var valores = [];
    $.each($('.val_button:checkbox:checked'), function(){
        valores.push($(this).val());
    });
    if(valores){
        return valores;
    }else{
        return null;
    }
}
/*#########################################################*/


var updateMapData = function(){

        url = 'http://127.0.0.1:8000/redbosques/datos_mapa';
        var eje = getEje();
        var id_rodal = getCodiRodal();
        var codigo_habitat = getTipoHabitat();
        var habitat_sel = getHabitatSel();
        var valoracion = getValoracion();


        url = url+'?e='+eje;

        if(id_rodal){
            id_tipo_habitad_sel = null;
            url = url + '&cr=' + id_rodal;
        }else{
            if(codigo_habitat){
                url = url + '&h=' + codigo_habitat;
                    if(habitat_sel){
                        url = url + '&ch=' + habitat_sel;
                    }
            }

            if(valoracion.length != 0){

                for (var i = 0; i < valoracion.length; i++){
                    url = url + '&val_valor=' + valoracion[i];
                }
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
                if(data){
                    if(data.llista_habitats){
                        //console.log(data.llista_habitats);
                        selector_Habitad(data.llista_habitats);
                    }
                    console.log(data.llista_punts);
                    setMapData(data.llista_punts);

                }
                //setMapData(data);

            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
}


function selector_Habitad(data){
    $(".tipo_habitad_sel").empty();
    //if(data){
        $(".tipo_habitad_sel").append('<option value="" class="tipo_habitad_seleccionada">------</option>');
        for(i=0; i<data.length; i++){
            $(".tipo_habitad_sel").append('<option value=' + data[i].cod + ' class="tipo_habitad_seleccionada">' + data[i].nombre + '</option>');
        }

        if(id_tipo_habitad_sel){
            //$(".tipo_habitad_sel option[value='+ id_tipo_habitad_sel +']").attr("selected",true);
            $(".tipo_habitad_sel").val(id_tipo_habitad_sel);
        }
    //}

}


function selector_valoracion(){
    puntuacion = [
        {0: '#7030a0'},
        {1: '#b719a0'},
        {2: '#b719a0'},
        {3: '#ff3300'},
        {4: '#ff9900'},
        {5: '#ffff00'},
        {6: '#99cc00'},
        {7: '#669900'},
        {8: '#003300'},
        {9: '#0033cc'},
        {10:'#000066'}
    ];

    for (i=0; i<puntuacion.length; i++){
        /*$(".selector_valoracion").append(
        '<span>'+ Object.keys(puntuacion[i]) + '</span><label class="dot" style="background-color:' + Object.values(puntuacion[i]) + '"><input class="valoracion_button" type="radio" name="selector_valoracion" id="' + Object.values(puntuacion[i]) + '" value="option1"></label><br>');*/

        $(".selector_valoracion").append(
        '<input class="val_button" type="checkbox" onclick="updateMapData()" name="selector_val" id="' + Object.values(puntuacion[i]) + '" value="' + Object.keys(puntuacion[i]) + '"><p class="leyendaValoracion"><i class="fas fa-circle" style="color:' + Object.values(puntuacion[i]) + '; margin-right: 5px;"></i>' + Object.keys(puntuacion[i]) + '</p>');
    }
}



var changeFilter = function(){

    var valorFiltro = $(".selectorFiltro").val();
    var txtButton = $(".selectorFiltro").html();

    if((valorFiltro == 0) && (txtButton == "Valoración Humana")){
        $(".selectorFiltro").val(1);
        $(".selectorFiltro").html("Rodal");
        $(".seleccio_rodal").hide();
        $(".seleccio_habitat").show();
        //updateMapData();
        limpiarFiltros();
    }else{
        $(".selectorFiltro").val(0);
        $(".selectorFiltro").html("Valoración Humana");
        $(".seleccio_habitat").hide();
        $(".seleccio_rodal").show();
        //updateMapData();
        limpiarFiltros();
    }
}

var limpiarFiltros = function(){
    marker_cluster.clearLayers();
    $('.tipo_habitad_sel').empty();
    $('input[type="checkbox"]').prop('checked', false);


    $('.selector_clasificacio').prop('selectedIndex',0);
    $('.selector_rodal').prop('selectedIndex',0);
    $('.tipo_habitad').prop('selectedIndex',0);
    $('.tipo_habitad_sel').prop('selectedIndex',0);
    //Per que tornin a sortir tots els registres al mapa
    //updateMapData();
}

/*
$('.tipo_bosque').on("click", function(){
    var codigo = $(".tipo_habitad").val();
    marker_cluster.clearLayers();

    $.ajax({
        url: 'http://127.0.0.1:8000/redbosques/datos_habitat?h=' + codigo,
        //url: url+'?h='+codigo,
        method: "GET",
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                var csrftoken = getCookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },

        success: function( data, textStatus, jqXHR ) {
            selector_Habitad(data.llista_habitats);
            setMapData(data.llista_punts_ini)
            //console.log(data.llista_punts_ini);
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        }
    });
});
*/

/*
$('.rodal').on("click", function(){

    marker_cluster.clearLayers();

    var id_rodal = $(".selector_rodal").val();

    $.ajax({
        url: 'http://127.0.0.1:8000/redbosques/datos_mapa?cr=' + id_rodal,
        //url: url+'?h='+codigo,
        method: "GET",
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                var csrftoken = getCookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },

        success: function( data, textStatus, jqXHR ) {
            setMapData(data);
            //console.log(data);
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        }
    });
});
*/


/*
$('.tipo_habitad_sel').on("click", function(){
    marker_cluster.clearLayers();
    var id_tipo_habitad_sel = $('.tipo_habitad_sel').val();
    var val_valoracion = $("input:checked").val();

    if (val_valoracion == undefined){
        url_data = 'http://127.0.0.1:8000/redbosques/datos_mapa?ch=' + id_tipo_habitad_sel;
    }else{
        url_data = 'http://127.0.0.1:8000/redbosques/datos_mapa?ch=' + id_tipo_habitad_sel + '&val_valor=' + val_valoracion;
    }

    console.log(url_data);

    $.ajax({
        //url: 'http://127.0.0.1:8000/redbosques/datos_mapa?ch=' + id_tipo_habitad_sel,
        url: url_data,
        method: "GET",
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                var csrftoken = getCookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },

        success: function( data, textStatus, jqXHR ) {
            setMapData(data);
            //console.log(data);
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        }
    });
});
*/



/*$(".selector_valoracion").change(function(){

    //alert($("input:checked").val());
    marker_cluster.clearLayers();
    var val_valoracion = $("input:checked").val();
    var id_tipo_habitad_sel = $('.tipo_habitad_sel').val();

    //console.log(id_tipo_habitad_sel); // Puede ser null
    //console.log(val_valoracion); // Puede ser undefined

    if (id_tipo_habitad_sel == null){
        url_data = 'http://127.0.0.1:8000/redbosques/datos_mapa?val_valor=' + val_valoracion;
    }else{
        url_data = 'http://127.0.0.1:8000/redbosques/datos_mapa?ch=' + id_tipo_habitad_sel + '&val_valor=' + val_valoracion;
    }

    console.log(url_data);

    $.ajax({
        //url: 'http://127.0.0.1:8000/redbosques/datos_mapa?val_valor=' + val_valoracion,
        url: url_data,
        method: "GET",
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                var csrftoken = getCookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },

        success: function( data, textStatus, jqXHR ) {
            setMapData(data);
            //console.log(url);
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        }
    });
});
*/




