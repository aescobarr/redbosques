

$(document).ready(function() {
        var eje = eje;



    setMapData = function(data, eje){

        //marker_cluster.clearLayers();
        if(markerLayer){
            markerLayer.clearLayers();
        }

        /*###########################Icono/Leyenda##########################################*/

        if(eje == 'hh'){
            legendHH.addTo(mymap);
            mymap.removeControl(legend);

            var html_icon_0 = L.divIcon({className: "iconHH_0", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle iconHH_0"></i>'});
            var html_icon_1 = L.divIcon({className: "iconHH_1", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle iconHH_1"></i>'});
            var html_icon_2 = L.divIcon({className: "iconHH_2", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle iconHH_2"></i>'});
            var html_icon_3 = L.divIcon({className: "iconHH_3", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle iconHH_3"></i>'});
            var html_icon_4 = L.divIcon({className: "iconHH_4", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle iconHH_4"></i>'});
            var html_icon_5 = L.divIcon({className: "iconHH_5", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle iconHH_5"></i>'});
            var html_icon_6 = L.divIcon({className: "iconHH_6", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle iconHH_6"></i>'});
            var html_icon_7 = L.divIcon({className: "iconHH_7", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle iconHH_7"></i>'});
            var html_icon_8 = L.divIcon({className: "iconHH_8", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle iconHH_8"></i>'});
            var html_icon_9 = L.divIcon({className: "iconHH_9", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle iconHH_9"></i>'});
            var html_icon_10 = L.divIcon({className: "iconHH_10", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle iconHH_10"></i>'});
            var html_icon_default = L.divIcon({className: "iconHH_null", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle iconHH_null"></i>'});

        }else{
            legend.addTo(mymap);
            mymap.removeControl(legendHH);

            var html_icon_0 = L.divIcon({className: "icon_0", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_0"></i>'});
            var html_icon_1 = L.divIcon({className: "icon_1", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_1"></i>'});
            var html_icon_2 = L.divIcon({className: "icon_2", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_2"></i>'});
            var html_icon_3 = L.divIcon({className: "icon_3", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_3"></i>'});
            var html_icon_4 = L.divIcon({className: "icon_4", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_4"></i>'});
            var html_icon_5 = L.divIcon({className: "icon_5", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_5"></i>'});
            var html_icon_6 = L.divIcon({className: "icon_6", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_6"></i>'});
            var html_icon_7 = L.divIcon({className: "icon_7", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_7"></i>'});
            var html_icon_8 = L.divIcon({className: "icon_8", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_8"></i>'});
            var html_icon_9 = L.divIcon({className: "icon_9", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_9"></i>'});
            var html_icon_10 = L.divIcon({className: "icon_10", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_10"></i>'});
            var html_icon_default = L.divIcon({className: "icon_null", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_null"></i>'});
        }

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


        var llista_punts = [];

        for(var i = 0; i < data.length; i++){
            var punt = data[i];

            var current_icon;
            if (punt.valor){
                current_icon = taula_icons[punt.valor];
            }else{
                current_icon = html_icon_default;
            }

            var marker = L.marker([punt.y,punt.x], {icon: current_icon}).bindPopup(
            '<b>' + punt.nombre + '</b><br><b>Hábitat: </b>' + punt.habitat_nom + '<br>' +
            '<b>Comunidad Autónoma: </b>' + punt.Comunidad_autonoma + '<br><b>Región biogeográfica: </b>' + punt.regionBiogeo + '<br>' +
            '<a href="/redbosques/comparador/' + punt.id_rodal + '/"><b>Comparar</b></a><br><br>' +
            '<div class="" style="text-align: center;"><table class="table"><tr><th style="text-align: center">Ámbito</th>'+
            '<th style="text-align: center">Valor</th></tr><tr><td>Naturalidad</td><td>'+ punt.valor_nm +'</td></tr><tr>'+
            '<td>Huella humana</td><td>'+ punt.valor_hh +'</td></tr><tr><td>Integridad Espacial</td><td>'+ punt.valor_ie +'</td></tr></table></div>' +
            '<div class="imagenRodal"><img src="'+ punt.imagen +'" alt="'+ punt.nombre +'" width="250" height="150"></div>'
            );

            llista_punts.push(marker);

            /* Tornar a activar els clusters dels punts*/
            //marker_cluster.addLayer(marker);
            //mymap.addLayer(marker_cluster);

        }

        markerLayer = L.layerGroup(llista_punts);
        mymap.addLayer(markerLayer);


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


    var test = $('.selector_clasificacio').val();
    //console.log(test);

    var legendHH = L.control({position: 'bottomright'});

    legendHH.onAdd = function (mymap) {

        var div = L.DomUtil.create('div', 'info legend'),
            puntuacion = [
            {10: '#ff0000'},
            {9: '#ff4000'},
            {8: '#ff8000'},
            {7: '#ffff00'},
            {6: '#f2f200'},
            {5: '#e5ff00'},
            {4: '#caff00'},
            {3: '#adff00'},
            {2: '#8cff00'},
            {1: '#62ff00'},
            {0:'#00ff00'}
            ];

        for (i=0; i<puntuacion.length; i++){
            div.innerHTML += '<p class="leyendaValoracion"><i class="fas fa-circle" style="color:' + Object.values(puntuacion[i]) + '; margin-right: 5px;"></i>' + Object.keys(puntuacion[i]) + '</p>';
        }
        return div;
    };


    /*marker_cluster = L.markerClusterGroup({
            spiderLegPolylineOptions: { weight: 3, color: '#222', opacity: 0.5 },
            spiderfyDistanceMultiplier: 3
    });*/

    if(zoomRodal){
        zoomCoordenadasRodal(zoomRodal);
    }else{
        mymap.setView([40.0000000, -4.0000000], 6);
    }

    //legend.addTo(mymap);
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
                    //mymap.setView([40.0000000, -4.0000000], 6);
                    /*if(data.llista_habitats){
                        //selector_Habitat(data.llista_habitats);
                        //mymap.setView([40.0000000, -4.0000000], 6);
                    }*/

                    //selector_rodal(data.llista_punts);
                    setMapData(data.llista_punts, eje);


                    if(id_rodal){
                        mymap.setView([data.llista_punts[0].y, data.llista_punts[0].x], 13);
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
    //console.log(urlHabitat);
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
                //updateMapData();

                setMapData(data.newRodalesData, codiAmbito);
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
    //console.log(urlSubHabitat);
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
                    selector_rodal(data.newRodalesData2);
                    //updateMapData();
                    setMapData(data.newRodalesData2, codiAmbito);

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

    //console.log(urlRodal);

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
                    //console.log(data.rodalData);
                    //ambitoData();
                    //updateMapData();
                    setMapData(data.rodalData, codiAmbito);
                    if(codiRodal){
                        mymap.setView([data.rodalData[0].y, data.rodalData[0].x], 13);
                    }
                }
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
}



var ambitoData = function(){
    var codiAmbito = getEje();
    urlAmbito = '/redbosques/ambitoData';
    urlAmbito = urlAmbito +'?ca='+codiAmbito;

    console.log(urlAmbito);

    $.ajax({
            url: urlAmbito,
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
    markerLayer.clearLayers();
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
    //habitatData();
    //subHabitatData();
    //rodalData();

    urlCleaner = '/redbosques/dataCleaner';

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


function zoomCoordenadasRodal(zoomRodal){
    //alert("hola zoom");
    console.log(zoomRodal[0].nombre);
    //if(id_rodal){
        mymap.setView([zoomRodal[0].y, zoomRodal[0].x], 13);
    //}

}


