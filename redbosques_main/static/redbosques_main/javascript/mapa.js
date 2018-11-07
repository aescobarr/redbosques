

$(document).ready(function() {
    //console.log(URL_BASE);
    //console.log(URL_BASE);


    setMapData = function(data){
        marker_cluster.clearLayers();
        //console.log(data);
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

            /*var marker = L.marker([punt.y,punt.x], {icon: current_icon}).bindPopup(
            '<b>Nombre habitad: </b>' + punt.habitat_nom + '<br><b>Localización: </b>' + punt.nombre + '<br>' +
            '<b>Comunidad Autónoma: </b>' + punt.Comunidad_autonoma + '<br>' +
            '<a href="/redbosques/comparador/' + punt.id_rodal + '/"><b>Ver ficha</b></a><br>' +
            '<div class="imagenRodal"><img href="'+ punt.imagen +'" alt="'+ punt.nombre +'" width="250" height="150"></div>'
            );*/

            console.log(punt.imagen);

            var marker = L.marker([punt.y,punt.x], {icon: current_icon}).bindPopup(
            '<b>' + punt.nombre + '</b><br><b>Hábitat: </b>' + punt.habitat_nom + '<br>' +
            '<b>Comunidad Autónoma: </b>' + punt.Comunidad_autonoma + '<br>' +
            '<a href="/redbosques/comparador/' + punt.id_rodal + '/"><b>Comparar</b></a><br><br>' +
            '<div class="" style="text-align: center;"><table class="table"><tr><th style="text-align: center">Ámbito</th>'+
            '<th style="text-align: center">Valor</th></tr><tr><td>Naturalidad</td><td>'+ punt.valor_nm +'</td></tr><tr>'+
            '<td>Huella humana</td><td>'+ punt.valor_hh +'</td></tr><tr><td>Integridad Espacial</td><td>'+ punt.valor_ie +'</td></tr></table></div>' +
            '<div class="imagenRodal"><img src="'+ punt.imagen +'" alt="'+ punt.nombre +'" width="250" height="150"></div>'
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


    var bing = L.tileLayer.bing('AisLQm3JkrOKysYfF9FiIkwkH-kIryIOeJcEs4JV-Qb9fgdBZk3tM4NmTe-e94Zr');

    var baseLayers = {
		"Bing maps": bing,
		"Open street map": base
	};


    mymap = L.map('mapid', {
            center: [40.0000000, -4.0000000],
            zoom: 6,
            layers: [base,bing]
    });

    L.control.layers(baseLayers).addTo(mymap);

    var legend = L.control({position: 'bottomright'});

    legend.onAdd = function (mymap) {

        var div = L.DomUtil.create('div', 'info legend'),
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
            div.innerHTML += '<p class="leyendaValoracion"><i class="fas fa-circle" style="color:' + Object.values(puntuacion[i]) + '; margin-right: 5px;"></i>' + Object.keys(puntuacion[i]) + '</p>';
        }
        return div;
    };

    marker_cluster = L.markerClusterGroup({
            spiderLegPolylineOptions: { weight: 1.5, color: '#222', opacity: 0.5 },
            spiderfyDistanceMultiplier: 3
    });


    legend.addTo(mymap);
    updateMapData();
});

/*################Getters selectores#######################*/


var getEje = function(){
    var eje_sel = $('.selector_clasificacio').val();
    return eje_sel;
}

var getCodiRodal = function(){
    codi_rodal = $('.selector_rodal').val();

    if(codi_rodal == ''){
        return null;
    }
    return codi_rodal;
}

var getHabitat = function(){
    var tipo_habitat = $(".tipo_habitat").val();

    if(tipo_habitat == ''){
        return null;
    }else{
        //$('.selector_rodal').val('');
        return tipo_habitat;
    }
}


var getSubHabitat = function(){
    id_tipo_habitat_sel = $('.tipo_habitat_sel').val();

    if(id_tipo_habitat_sel == ''){
        return null;
    }else{

        return id_tipo_habitat_sel;
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

        url = '/redbosques/datos_mapa';
        var eje = getEje();
        var id_rodal = getCodiRodal();
        var codigo_habitat = getHabitat();
        var codigo_subHabitat = getSubHabitat();
        var valoracion = getValoracion();


        url = url+'?e='+eje;

        /*if(id_rodal){
            id_tipo_habitat_sel = null;
            url = url + '&cr=' + id_rodal;
        }else{
            if(codigo_habitat){
                url = url + '&h=' + codigo_habitat;
                    if(codigo_subHabitat){
                        url = url + '&ch=' + codigo_subHabitat;
                        if(id_rodal){
                            id_tipo_habitat_sel = null;
                            url = url + '&cr=' + id_rodal;
                        }
                    }

            }
        }*/

        if(id_rodal){
            url = url + '&cr=' + id_rodal;
        }else{
            if(codigo_habitat){
                url = url + '&h=' + codigo_habitat;
            }
            if(codigo_subHabitat){
                url = url + '&csh=' + codigo_subHabitat;
            }
            if(id_rodal){
                url = url + '&cr=' + id_rodal;
            }
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
                if(data){
                    if(data.llista_habitats){
                        //selector_Habitat(data.llista_habitats);
                        mymap.setView([40.0000000, -4.0000000], 6);
                    }

                    //selector_rodal(data.llista_punts);
                    setMapData(data.llista_punts);


                    if(id_rodal){
                        mymap.setView([data.llista_punts[0].y, data.llista_punts[0].x], 10);
                    }else{
                        mymap.setView([40.0000000, -4.0000000], 6);
                    }
                }
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
}



var habitatData = function(){

    var codiHabitat = getHabitat();
    var codiAmbito = getEje();
    urlHabitat = '/redbosques/habitatData';
    urlHabitat = urlHabitat+'?ch='+codiHabitat + '&ca=' + codiAmbito;
    console.log(urlHabitat);
    $('.tipo_habitat_sel').prop('selectedIndex',0);




    $.ajax({
            url: urlHabitat,
            method: "GET",
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },

            success: function( data, textStatus, jqXHR ) {
                //console.log(data.newRodalesData);
                selector_subHabitat(data.newSubHabitatData);
                selector_rodal(data.newRodalesData);
                updateMapData();
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
}


var subHabitatData = function(){

    var codiSubHabitat = getSubHabitat();
    var codiAmbito = getEje();
    urlSubHabitat = '/redbosques/subHabitatData';
    urlSubHabitat = urlSubHabitat+'?csh='+codiSubHabitat+ '&ca=' + codiAmbito;
    console.log(urlSubHabitat);
    //$('.tipo_habitat_sel').prop('selectedIndex',0);
    $('.selector_rodal').prop('selectedIndex',0);

    $.ajax({
            url: urlSubHabitat,
            method: "GET",
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },

            success: function( data, textStatus, jqXHR ) {
                if(data){
                    console.log(data.newRodalesData2);
                    selector_rodal(data.newRodalesData2);
                    updateMapData();

                }
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
}


var rodalData = function(){
    var codiRodal = getCodiRodal();
    var codiAmbito = getEje();
    urlRodal = '/redbosques/rodalData';
    urlRodal = urlRodal+'?cr='+codiRodal+'&ca='+codiAmbito;
    console.log(urlRodal);

    $.ajax({
            url: urlRodal,
            method: "GET",
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },

            success: function( data, textStatus, jqXHR ) {
                if(data){
                    console.log(data.rodalData);
                    updateMapData();
                }
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
}


function selector_Habitat(data){
    $(".tipo_habitat").empty();
        $(".tipo_habitat").append('<option value="" selected="selected">------</option>');
        for(i=0; i<data.length; i++){
            $(".tipo_habitat").append('<option value=' + data[i].cod + ' class="habitat_seleccionada">' + data[i].nombre + '</option>');
        }

        if(id_tipo_habitat){
            $(".tipo_habitat").val(id_tipo_habitat);
        }
}

function selector_subHabitat(data){
    $(".tipo_habitat_sel").empty();
        $(".tipo_habitat_sel").append('<option value="" selected="selected">------</option>');
        for(i=0; i<data.length; i++){
            $(".tipo_habitat_sel").append('<option value=' + data[i].cod + ' class="subHabitat_seleccionada">' + data[i].nombre + '</option>');
        }

        if(id_tipo_habitat_sel){
            $(".tipo_habitat_sel").val(id_tipo_habitat_sel);
        }
}


function selector_rodal(data){
    $(".selector_rodal").empty();

        $(".selector_rodal").append('<option value="" class="rodal">------</option>');
        for(i=0; i<data.length; i++){
            $(".selector_rodal").append('<option value=' + data[i].id_rodal + ' class="rodal">' + data[i].nombre + '</option>');
        }

        if(codi_rodal){
            $(".selector_rodal").val(codi_rodal);
        }
}



var limpiarFiltros = function(){
    marker_cluster.clearLayers();
    //$('.tipo_habitat_sel').empty();
    //$('input[type="checkbox"]').prop('checked', false);


    //$('.selector_clasificacio').prop('selectedIndex',0);
    //$('.selector_rodal').prop('selectedIndex',0);

    $('.tipo_habitat').prop('selectedIndex',0);
    $('.tipo_habitat_sel').prop('selectedIndex',0);
    $('.selector_rodal').prop('selectedIndex',0);

    //Per que tornin a sortir tots els registres al mapa
    mymap.setView([40.0000000, -4.0000000], 6);
    updateMapData();

    urlCleaner = '/redbosques/dataCleaner';

    //console.log(urlCleaner);
    $.ajax({
            url: urlCleaner,
            method: "GET",
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },

            success: function( data, textStatus, jqXHR ) {
                if(data){

                    /*console.log(data);
                    console.log(data.habitatData);
                    console.log(data.subHabitatData);
                    console.log(data.rodalesData);*/


                    selector_Habitat(data.habitatData);
                    selector_subHabitat(data.subHabitatData);
                    selector_rodal(data.rodalesData);
                }
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
}


