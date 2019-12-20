$(document).ready(function() {
    var eje = eje;


    redirectFaseMap();


    setMapData = function(data, eje){

        //marker_cluster.clearLayers();
        if(markerLayer){
            markerLayer.clearLayers();
        }

        //###########################Icono/Leyenda##########################################

        if(eje == 'hh'){
            legendHH.addTo(mymap);
            mymap.removeControl(legend);

            var html_icon_0 = L.divIcon({className: "iconHH_0", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle iconHH_0"></i>'});
            var html_icon_1 = L.divIcon({className: "iconHH_1", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle iconHH_1"></i>'});
            var html_icon_2 = L.divIcon({className: "iconHH_2", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle iconHH_2"></i>'});
            var html_icon_3 = L.divIcon({className: "iconHH_3", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle iconHH_3"></i>'});
            var html_icon_4 = L.divIcon({className: "iconHH_4", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle iconHH_4"></i>'});
            var html_icon_5 = L.divIcon({className: "iconHH_5", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle iconHH_5"></i>'});
            var html_icon_6 = L.divIcon({className: "iconHH_6", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle iconHH_6"></i>'});
            var html_icon_7 = L.divIcon({className: "iconHH_7", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle iconHH_7"></i>'});
            var html_icon_8 = L.divIcon({className: "iconHH_8", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle iconHH_8"></i>'});
            var html_icon_9 = L.divIcon({className: "iconHH_9", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle iconHH_9"></i>'});
            var html_icon_10 = L.divIcon({className: "iconHH_10", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle iconHH_10"></i>'});
            var html_icon_default = L.divIcon({className: "iconHH_null", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle iconHH_null"></i>'});

        }else{
            legend.addTo(mymap);
            mymap.removeControl(legendHH);

            var html_icon_0 = L.divIcon({className: "icon_0", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_0"></i>'});
            var html_icon_1 = L.divIcon({className: "icon_1", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_1"></i>'});
            var html_icon_2 = L.divIcon({className: "icon_2", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_2"></i>'});
            var html_icon_3 = L.divIcon({className: "icon_3", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_3"></i>'});
            var html_icon_4 = L.divIcon({className: "icon_4", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_4"></i>'});
            var html_icon_5 = L.divIcon({className: "icon_5", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_5"></i>'});
            var html_icon_6 = L.divIcon({className: "icon_6", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_6"></i>'});
            var html_icon_7 = L.divIcon({className: "icon_7", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_7"></i>'});
            var html_icon_8 = L.divIcon({className: "icon_8", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_8"></i>'});
            var html_icon_9 = L.divIcon({className: "icon_9", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_9"></i>'});
            var html_icon_10 = L.divIcon({className: "icon_10", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_10"></i>'});
            var html_icon_default = L.divIcon({className: "icon_null", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_null"></i>'});
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

        //#####################################################################################


        var llista_punts = [];



        for(var i = 0; i < data.length; i++){
            var punt = data[i];

            var current_icon;
            if (punt.valor){
                if(punt.valor > 10 || punt.valor < 0){
                    current_icon = html_icon_default;
                }else{
                    current_icon = taula_icons[(punt.valor).toFixed(0)];
                }

            }else{
                current_icon = html_icon_default;
            }



            if (usuarioAut){

                if (punt.imagen == null){
                    var marker = L.marker([punt.y,punt.x], {icon: current_icon}).bindPopup(
                    '<b>' + punt.nombre + '</b><br><b>Hábitat: </b>' + punt.habitat_nom + '<br>' + '<b>Tipo de Bosque: </b>' + punt.tipobosque_nombre +
                    '<br><b>Comunidad Autónoma: </b>' + punt.Comunidad_autonoma + '<br><b>Región biogeográfica: </b>' + punt.regionBiogeo + '<br>' +
                    '<a href="/redbosques/fichaRodal/' + punt.id_rodal + '/"><b>Ficha </b></a>&nbsp;<b> Comparar con: </b><a href="/redbosques/comparador_new/' + punt.id_rodal + '/">Rodales</a> / ' +
                    '<a href="/redbosques/comparador_ifn/' + punt.id_rodal + '/">IFN</a><br><br>' +
                    '<div class="popup-table" style="text-align: center; width: 250px;"><table class="table"><tr><th>Ámbito</th>'+
                    '<th style="text-align: center;">Valor</th></tr><tr><td style="text-align: left;">Madurez</td><td>'+ punt.valor_nm +'</td></tr><tr>'+
                    '<td style="text-align: left;">Huella humana</td><td>'+ punt.valor_hh +'</td></tr><tr><td style="text-align: left;">Integridad Espacial</td><td>'+ punt.valor_ie +'</td></tr></table></div>' +
                    '<div class="imagenRodal"><img src="/static/redbosques_main/css/logo.png" alt="'+ punt.nombre +'" height="100"></div>'
                    );
                }else{
                    var marker = L.marker([punt.y,punt.x], {icon: current_icon}).bindPopup(
                    '<b>' + punt.nombre + '</b><br><b>Hábitat: </b>' + punt.habitat_nom + '<br>' + '<b>Tipo de Bosque: </b>' + punt.tipobosque_nombre +
                    '<br><b>Comunidad Autónoma: </b>' + punt.Comunidad_autonoma + '<br><b>Región biogeográfica: </b>' + punt.regionBiogeo + '<br>' +
                    '<a href="/redbosques/fichaRodal/' + punt.id_rodal + '/"><b>Ficha </b></a>&nbsp;<b> Comparar con: </b><a href="/redbosques/comparador_new/' + punt.id_rodal + '/">Rodales</a> / ' +
                    '<a href="/redbosques/comparador_ifn/' + punt.id_rodal + '/">IFN</a><br><br>' +
                    '<div class="popup-table" style="text-align: center; width: 250px;"><table class="table"><tr><th>Ámbito</th>'+
                    '<th style="text-align: center;">Valor</th></tr><tr><td style="text-align: left;">Madurez</td><td>'+ punt.valor_nm +'</td></tr><tr>'+
                    '<td style="text-align: left;">Huella humana</td><td>'+ punt.valor_hh +'</td></tr><tr><td style="text-align: left;">Integridad Espacial</td><td>'+ punt.valor_ie +'</td></tr></table></div>' +
                    '<div class="imagenRodal"><img src="/media/'+ punt.imagen +'" alt="'+ punt.nombre +'" width="250" height="150"></div>'
                    );
                }
            }else{

                if (punt.imagen == null){
                    var marker = L.marker([punt.y,punt.x], {icon: current_icon}).bindPopup(
                    '<b>' + punt.nombre + '</b><br><b>Hábitat: </b>' + punt.habitat_nom + '<br>' + '<b>Tipo de Bosque: </b>' + punt.tipobosque_nombre +
                    '<br><b>Comunidad Autónoma: </b>' + punt.Comunidad_autonoma + '<br><b>Región biogeográfica: </b>' + punt.regionBiogeo + '<br>' +
                    '<b> Comparar con: </b><a href="/redbosques/comparador_new/' + punt.id_rodal + '/">Rodales</a> / ' +
                    '<a href="/redbosques/comparador_ifn/' + punt.id_rodal + '/">IFN</a><br><br>' +
                    '<div class="popup-table" style="text-align: center; width: 250px;"><table class="table"><tr><th>Ámbito</th>'+
                    '<th style="text-align: center;">Valor</th></tr><tr><td style="text-align: left;">Madurez</td><td>'+ punt.valor_nm +'</td></tr><tr>'+
                    '<td style="text-align: left;">Huella humana</td><td>'+ punt.valor_hh +'</td></tr><tr><td style="text-align: left;">Integridad Espacial</td><td>'+ punt.valor_ie +'</td></tr></table></div>' +
                    '<div class="imagenRodal"><img src="/static/redbosques_main/css/logo.png" alt="'+ punt.nombre +'" height="100"></div>'
                    );
                }else{
                    var marker = L.marker([punt.y,punt.x], {icon: current_icon}).bindPopup(
                    '<b>' + punt.nombre + '</b><br><b>Hábitat: </b>' + punt.habitat_nom + '<br>' + '<b>Tipo de Bosque: </b>' + punt.tipobosque_nombre +
                    '<br><b>Comunidad Autónoma: </b>' + punt.Comunidad_autonoma + '<br><b>Región biogeográfica: </b>' + punt.regionBiogeo + '<br>' +
                    '<b> Comparar con: </b><a href="/redbosques/comparador_new/' + punt.id_rodal + '/">Rodales</a> / ' +
                    '<a href="/redbosques/comparador_ifn/' + punt.id_rodal + '/">IFN</a><br><br>' +
                    '<div class="popup-table" style="text-align: center; width: 250px;"><table class="table"><tr><th>Ámbito</th>'+
                    '<th style="text-align: center;">Valor</th></tr><tr><td style="text-align: left;">Madurez</td><td>'+ punt.valor_nm +'</td></tr><tr>'+
                    '<td style="text-align: left;">Huella humana</td><td>'+ punt.valor_hh +'</td></tr><tr><td style="text-align: left;">Integridad Espacial</td><td>'+ punt.valor_ie +'</td></tr></table></div>' +
                    '<div class="imagenRodal"><img src="/media/'+ punt.imagen +'" alt="'+ punt.nombre +'" width="250" height="150"></div>'
                    );
                }

            }


            llista_punts.push(marker);

            //Tornar a activar els clusters dels punts
            //marker_cluster.addLayer(marker);
            //mymap.addLayer(marker_cluster);

        }

        markerLayer = L.layerGroup(llista_punts);
        mymap.addLayer(markerLayer);


    }

    setMapDataFase1 = function(data){



        if(markerLayerFase1){
            markerLayerFase1.clearLayers();
        }

        //###########################Icono/Leyenda##########################################


        //iconAnchor: [8,8]

        legendFase1.addTo(mymapFase1);
        //mymapFase1.removeControl(legendHH);

        var html_icon_0 = L.divIcon({className: "icon_0", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_0"></i>'});
        var html_icon_1 = L.divIcon({className: "icon_1", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_1"></i>'});
        var html_icon_2 = L.divIcon({className: "icon_2", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_2"></i>'});
        var html_icon_3 = L.divIcon({className: "icon_3", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_3"></i>'});
        var html_icon_4 = L.divIcon({className: "icon_4", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_4"></i>'});
        var html_icon_5 = L.divIcon({className: "icon_5", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_5"></i>'});
        var html_icon_6 = L.divIcon({className: "icon_6", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_6"></i>'});
        var html_icon_7 = L.divIcon({className: "icon_7", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_7"></i>'});
        var html_icon_8 = L.divIcon({className: "icon_8", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_8"></i>'});
        var html_icon_9 = L.divIcon({className: "icon_9", iconSize: [16,16], iconAnchor: [8,8], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_9"></i>'});
        //var html_icon_10 = L.divIcon({className: "icon_10", iconAnchor: [18, 24], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_10"></i>'});
        var html_icon_default = L.divIcon({className: "icon_null", iconAnchor: [18, 24], iconSize: [16,16], labelAnchor: [-6, 0], popupAnchor: [-8, -23], html: '<i class="fas fa-circle icon_null"></i>'});


        var taula_iconsFase1 = {
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
          //  10: html_icon_10
        };

        //#####################################################################################


        var llista_punts = [];

        for(var i = 0; i < data.length; i++){
            var punt = data[i];

            var current_icon;
            if (punt.valor){
                if(punt.valor > 9 || punt.valor < 0){
                    current_icon = html_icon_default;
                }else{
                    current_icon = taula_iconsFase1[(punt.valor).toFixed(0)];
                }

            }else{
                current_icon = html_icon_default;
            }

            var valFrase = null;
            if (punt.valor >= 1 && punt.valor <= 3){
                valFrase = "Rodal con madurez baja"
            }else if (punt.valor >= 4 && punt.valor <= 6){
                valFrase = "Rodal con tendencia a la madurez"
            }else if (punt.valor >= 7 && punt.valor <= 9){
                valFrase = "Rodal con indicios consistentes de un nivel elevado de madurez"
            }

            if (usuarioAut){
                if (punt.foto == null){
                    var marker = L.marker([punt.y,punt.x], {icon: current_icon}).bindPopup(
                    '<b>' + punt.nombre + '</b><br><b>Hábitat: </b>' + punt.habitat_nom + '<br>' + '<b>Tipo de Bosque: </b>' + punt.tipodebosque +
                    '<br><b>Comunidad Autónoma: </b>' + punt.Comunidad_autonoma + '<br>' +
                    //'<b>Valor: </b>' + punt.valor + ' - '+ valFrase +'<br>' + '<a href="/redbosques/fichaRodalFase1/' + punt.id_rodal + '/"><b>Ficha </b></a>' +
                    '<b>' + valFrase +'</b><br>' + '<a href="/redbosques/fichaRodalFase1/' + punt.id_rodal + '/"><b>Ficha </b></a>' +
                    '<div class="imagenRodal"><img src="/static/redbosques_main/css/logo.png" alt="'+ punt.nombre +'" height="100"></div>'
                    );
                }else{
                    var marker = L.marker([punt.y,punt.x], {icon: current_icon}).bindPopup(
                    '<b>' + punt.nombre + '</b><br><b>Hábitat: </b>' + punt.habitat_nom + '<br>' + '<b>Tipo de Bosque: </b>' + punt.tipodebosque +
                    '<br><b>Comunidad Autónoma: </b>' + punt.Comunidad_autonoma + '<br>' +
                    //'<b>Valor: </b>' + punt.valor +' - '+ valFrase + '<br>' + '<a href="/redbosques/fichaRodalFase1/' + punt.id_rodal + '/"><b>Ficha </b></a>' +
                    '<b>' + valFrase +'</b><br>' + '<a href="/redbosques/fichaRodalFase1/' + punt.id_rodal + '/"><b>Ficha </b></a>' +
                    '<div class="imagenRodal"><img src="/media/'+ punt.foto +'" alt="'+ punt.nombre +'" width="250" height="150"></div>'
                    );
                }
            }else{
                if (punt.foto == null){
                    var marker = L.marker([punt.y,punt.x], {icon: current_icon}).bindPopup(
                    '<b>' + punt.nombre + '</b><br><b>Hábitat: </b>' + punt.habitat_nom + '<br>' + '<b>Tipo de Bosque: </b>' + punt.tipodebosque +
                    '<br><b>Comunidad Autónoma: </b>' + punt.Comunidad_autonoma + '<br>' +
                    //'<b>Valor: </b>' + punt.valor + ' - '+ valFrase +'<br>' + '<a href="/redbosques/fichaRodalFase1/' + punt.id_rodal + '/"><b>Ficha </b></a>' +
                    '<b>' + valFrase +'</b><br>' +
                    '<div class="imagenRodal"><img src="/static/redbosques_main/css/logo.png" alt="'+ punt.nombre +'" height="100"></div>'
                    );
                }else{
                    var marker = L.marker([punt.y,punt.x], {icon: current_icon}).bindPopup(
                    '<b>' + punt.nombre + '</b><br><b>Hábitat: </b>' + punt.habitat_nom + '<br>' + '<b>Tipo de Bosque: </b>' + punt.tipodebosque +
                    '<br><b>Comunidad Autónoma: </b>' + punt.Comunidad_autonoma + '<br>' +
                    //'<b>Valor: </b>' + punt.valor +' - '+ valFrase + '<br>' + '<a href="/redbosques/fichaRodalFase1/' + punt.id_rodal + '/"><b>Ficha </b></a>' +
                    '<b>' + valFrase +'</b><br>' + 
                    '<div class="imagenRodal"><img src="/media/'+ punt.foto +'" alt="'+ punt.nombre +'" width="250" height="150"></div>'
                    );
                }
            }


            llista_punts.push(marker);
        }

        markerLayerFase1 = L.layerGroup(llista_punts);
        mymapFase1.addLayer(markerLayerFase1);
    }


//####################CAPAS##############################//

    var base = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
            maxZoom: 18,
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
                '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
                'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            id: 'mapbox.streets'
    });
    var baseFase1 = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
            maxZoom: 18,
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
                '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
                'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            id: 'mapbox.streets'
    });

    var bing = L.tileLayer.bing('AisLQm3JkrOKysYfF9FiIkwkH-kIryIOeJcEs4JV-Qb9fgdBZk3tM4NmTe-e94Zr');
    var bingFase1 = L.tileLayer.bing('AisLQm3JkrOKysYfF9FiIkwkH-kIryIOeJcEs4JV-Qb9fgdBZk3tM4NmTe-e94Zr');

    var openCycle = L.tileLayer('https://tile.thunderforest.com/cycle/{z}/{x}/{y}.png?apikey=dda4faab5df24211a8d46b5b607f51d6',{
        attribution: 'Maps &copy; <a href="https://www.thunderforest.com">Thunderforest</a>, Data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>',
        maxZoom: 22
    });
    var openCycleFase1 = L.tileLayer('https://tile.thunderforest.com/cycle/{z}/{x}/{y}.png?apikey=dda4faab5df24211a8d46b5b607f51d6',{
        attribution: 'Maps &copy; <a href="https://www.thunderforest.com">Thunderforest</a>, Data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>',
        maxZoom: 22
    });

    var ign = new L.TileLayer('http://www.ign.es/wmts/mapa-raster?service=WMTS&request=GetTile&version=1.0.0&layers=&styles=&tilematrixSet=GoogleMapsCompatible&format=image/jpeg&height=256&width=256&layer=MTN&style=default&tilematrix={z}&tilerow={y}&tilecol={x}',
      {
        maxZoom: 18,
        minZoom: 0,
        continuousWorld: true,
        attribution: 'Capa Raster CC BY 4.0 <a href="http://www.ign.es/web/ign/portal">ign.es</a>'
      });
    var ignFase1 = new L.TileLayer('http://www.ign.es/wmts/mapa-raster?service=WMTS&request=GetTile&version=1.0.0&layers=&styles=&tilematrixSet=GoogleMapsCompatible&format=image/jpeg&height=256&width=256&layer=MTN&style=default&tilematrix={z}&tilerow={y}&tilecol={x}',
      {
        maxZoom: 18,
        minZoom: 0,
        continuousWorld: true,
        attribution: 'Capa Raster CC BY 4.0 <a href="http://www.ign.es/web/ign/portal">ign.es</a>'
      });

    var baseLayers = {
		"Bing maps": bing,
		"IGN": ign,
		"Open street map": base,
		//"Open cycle map": openCycle
	};
    var baseLayersFase1 = {
		"Bing maps": bingFase1,
		"IGN": ignFase1,
		"Open street map": baseFase1,
		//"Open cycle map": openCycleFase1
	};

    mymap = L.map('mapid', {
            center: [40.0000000, -4.0000000],
            zoom: 6,
            //layers: [base,bing,ign,openCycle]
            layers: [bing,base,ign]
    });

    mymapFase1 = L.map('mapidFase1', {
            center: [40.0000000, -4.0000000],
            zoom: 6,
            //layers: [baseFase1,bingFase1,ignFase1,openCycleFase1]
            layers: [bingFase1,baseFase1,ignFase1]
    });


    L.control.layers(baseLayers).addTo(mymap);
    L.control.layers(baseLayersFase1).addTo(mymapFase1);


    var legend = L.control({position: 'bottomright'});
    var legendFase1 = L.control({position: 'bottomright'});
    var legendHH = L.control({position: 'bottomright'});

    legend.onAdd = function (mymap) {

        var div = L.DomUtil.create('div', 'info legend'),
            puntuacion = [
            {0: '#a50026'},
            {1: '#d73027'},
            {2: '#f46d43'},
            {3: '#fdae61'},
            {4: '#fee08b'},
            {5: '#ffffbf'},
            {6: '#d9ef8b'},
            {7: '#a6d96a'},
            {8: '#66bd63'},
            {9: '#1a9850'},
            {10:'#006837'}
            ];



        for (i=0; i<puntuacion.length; i++){
            div.innerHTML += '<p class="leyendaValoracion"><i class="fas fa-circle" style="color:' + Object.values(puntuacion[i]) + '; margin-right: 5px;"></i>' + Object.keys(puntuacion[i]) + '</p>';
        }
        return div;
    };

    legendHH.onAdd = function (mymap) {

        var div = L.DomUtil.create('div', 'info legend'),
            puntuacion = [
            {10: '#a50026'},
            {9: '#d73027'},
            {8: '#f46d43'},
            {7: '#fdae61'},
            {6: '#fee08b'},
            {5: '#ffffbf'},
            {4: '#d9ef8b'},
            {3: '#a6d96a'},
            {2: '#66bd63'},
            {1: '#1a9850'},
            {0: '#006837'}
            ];

        for (i=0; i<puntuacion.length; i++){
            div.innerHTML += '<p class="leyendaValoracion"><i class="fas fa-circle" style="color:' + Object.values(puntuacion[i]) + '; margin-right: 5px;"></i>' + Object.keys(puntuacion[i]) + '</p>';
        }
        return div;
    };

    legendFase1.onAdd = function (mymapFase1) {

        var div = L.DomUtil.create('div', 'info legend'),
            puntuacionFase1 = [
            {0: '#a50026'},
            {1: '#d73027'},
            {2: '#f46d43'},
            {3: '#fdae61'},
            {4: '#fee08b'},
            {5: '#ffffbf'},
            {6: '#d9ef8b'},
            {7: '#a6d96a'},
            {8: '#66bd63'},
            {9: '#1a9850'},
            //{10:'#006837'}
            ];



        for (i=0; i<puntuacionFase1.length; i++){
            div.innerHTML += '<p class="leyendaValoracion"><i class="fas fa-circle" style="color:' + Object.values(puntuacionFase1[i]) + '; margin-right: 5px;"></i>' + Object.keys(puntuacionFase1[i]) + '</p>';
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
        mymapFase1.setView([40.0000000, -4.0000000], 6);
    }


    //legend.addTo(mymap);
    updateMapData();
    updateMapDataProsp();

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




var getCodiRodalProsp = function(){
    codi_rodal = $('.selector_rodal_prospeccio').val();

    if(codi_rodal == ''){
        return null;
    }
    return codi_rodal;
}

var getHabitatProsp = function(){
    var tipo_habitat_prosp = $(".tipo_habitat_prospeccio").val();
    if(tipo_habitat_prosp == ''){
       return null;
    }else{
        return tipo_habitat_prosp;
    }
}



var getSubHabitatProsp = function(){
    id_tipo_habitat_sel_prospeccio = $('.tipo_habitat_sel_prospeccio').val();

    if(id_tipo_habitat_sel_prospeccio == ''){
        return null;
    }else{
        return id_tipo_habitat_sel_prospeccio;
    }
}




//#########################################################//


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

        if(codigo_subHabitat != null){
            if (codigo_subHabitat.includes("&")){
                codigo_subHabitat = codigo_subHabitat.replace(/&/gi, "%26");
                console.log(codigo_subHabitat);
            }
        }





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
    //console.log(url);
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
                    setMapDataFase1(data.llista_punts_RodalsProsp);


                    if(id_rodal){
                        mymap.setView([data.llista_punts[0].y, data.llista_punts[0].x], 13);
                        mymapFase1.setView([data.llista_punts[0].y, data.llista_punts[0].x], 13);
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

    if(codiSubHabitat != null){
        if (codiSubHabitat.includes("&")){
            codiSubHabitat = codiSubHabitat.replace(/&/gi, "%26");
            console.log(codiSubHabitat);
        }
    }

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

    //console.log(urlAmbito);

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
                    //console.log(data.rodalData);
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



function selector_Habitat_prospeccio(data){
    $(".tipo_habitat_prosp").empty();
        $(".tipo_habitat_prosp").append('<option value="" selected="selected">------</option>');
        for(i=0; i<data.length; i++){
            $(".tipo_habitat_prosp").append('<option value=' + data[i].cod + ' class="habitat_seleccionada">' + data[i].nombre + '</option>');
        }

        if(id_tipo_habitat){
            $(".tipo_habitat_prosp").val(id_tipo_habitat);
        }
}

function selector_subHabitat_prospeccio(data){
    $(".tipo_habitat_sel_prospeccio").empty();
        $(".tipo_habitat_sel_prospeccio").append('<option value="" selected="selected">------</option>');
        for(i=0; i<data.length; i++){
            $(".tipo_habitat_sel_prospeccio").append('<option value=' + data[i].cod + ' class="subHabitat_seleccionada">' + data[i].nombre + '</option>');
        }

        if(id_tipo_habitat_sel){
            $(".tipo_habitat_sel_prospeccio").val(id_tipo_habitat_sel);
        }
}

function selector_rodal_prospeccio(data){
    $(".selector_rodal_prospeccio").empty();

        $(".selector_rodal_prospeccio").append('<option value="" class="rodal">------</option>');
        for(i=0; i<data.length; i++){
            $(".selector_rodal_prospeccio").append('<option value=' + data[i].id_rodal + ' class="rodal">' + data[i].nombre + '</option>');
        }

        if(codi_rodal){
            $(".selector_rodal_prospeccio").val(codi_rodal);
        }
}



var limpiarFiltros = function(){
    markerLayer.clearLayers();

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
    urlCleaner = urlCleaner+'?f=fase2';

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

$('.mapaFase1Tab').on("click", function(){
    $('.mapaFase2').hide();
    $('.mapaFase1').show();
    setTimeout(function(){ mymapFase1.invalidateSize()}, 20);
});

$('.mapaFase2Tab').on("click", function(){
    $('.mapaFase2').show();
    $('.mapaFase1').hide();
    setTimeout(function(){ mymap.invalidateSize()}, 20);
});


var updateMapDataProsp = function(){

    url = '/redbosques/datos_mapa';
    var eje = getEje();
    var id_rodal = getCodiRodalProsp();
    var codigo_habitat = getHabitatProsp();
    var codigo_subHabitat = getSubHabitatProsp();



    url = url+'?e='+eje;


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
                setMapDataFase1(data.llista_punts_RodalsProsp);
                if(id_rodal){
                    mymapFase1.setView([data.llista_punts[0].y, data.llista_punts[0].x], 13);
                }
            }
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        }
    });
}

var limpiarFiltrosProsp = function(){
    markerLayerFase1.clearLayers();

    $('.tipo_habitat_prospeccio').prop('selectedIndex',0);
    $('.tipo_habitat_sel_prospeccio').prop('selectedIndex',0);
    $('.selector_rodal_prospeccio').prop('selectedIndex',0);

    //Per que tornin a sortir tots els registres al mapa
    mymapFase1.setView([40.0000000, -4.0000000], 6);
    updateMapDataProsp();
    //habitatData();
    //subHabitatData();
    //rodalData();

    urlCleaner = '/redbosques/dataCleaner';
    urlCleaner = urlCleaner+'?f=fase1';

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
                    selector_Habitat_prospeccio(data.habitatData);
                    selector_subHabitat_prospeccio(data.subHabitatDataProsp);
                    selector_rodal_prospeccio(data.rodalesProspData);

                }
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
}

var habitatDataProsp = function(){

    var codiHabitat = getHabitatProsp();
    urlHabitat = '/redbosques/habitatDataProsp';
    urlHabitat = urlHabitat+'?ch='+codiHabitat;
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
                selector_subHabitat_prospeccio(data.newSubHabitatData);
                selector_rodal_prospeccio(data.newRodalesData);
                setMapDataFase1(data.newRodalesData);
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
}

var subHabitatDataProsp = function(){

    var codiSubHabitat = getSubHabitatProsp();

    urlSubHabitat = '/redbosques/subHabitatDataProsp';
    urlSubHabitat = urlSubHabitat+'?csh='+codiSubHabitat;

    $('.selector_rodal_prospeccio').prop('selectedIndex',0);

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
                    selector_rodal_prospeccio(data.newRodalesData2);
                    setMapDataFase1(data.newRodalesData2);

                }
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
}


var rodalDataProsp = function(){
    var codiRodal = getCodiRodalProsp();
    urlRodal = '/redbosques/rodalDataProsp';
    urlRodal = urlRodal+'?cr='+codiRodal;

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
                    setMapDataFase1(data.rodalData);
                    if(codiRodal){
                        mymapFase1.setView([data.rodalData[0].y, data.rodalData[0].x], 13);
                    }
                }
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
}



var redirectFaseMap = function(){
        var pathname = window.location.href;
        console.log(pathname);
        var faseMap = window.location.hash;

        if (faseMap == "#mapaFase1"){
            $('.mapaFase1Tab').addClass("active");
            $('.mapaFase2Tab').removeClass("active");

            $('.mapaFase1').css("display", "block")
            $('.mapaFase2').css("display", "none")

        }else if (faseMap == "#mapaFase2"){
            $('.mapaFase1Tab').removeClass("active");
            $('.mapaFase2Tab').addClass("active");

            $('.mapaFase1').css("display", "none")
            $('.mapaFase2').css("display", "block")
        }

    }








