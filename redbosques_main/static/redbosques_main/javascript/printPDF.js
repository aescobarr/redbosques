var map;
$(document).ready(function() {
    /*var map = L.mapbox.map('map', 'mapaID').setView([38.9, -77.03], 14);
    console.log(map);
    leafletImage(map, function(err, canvas) {
        // now you have canvas
        // example thing to do with that canvas:
        var img = document.createElement('img');
        var dimensions = map.getSize();
        img.width = dimensions.x;
        img.height = dimensions.y;
        img.src = canvas.toDataURL();
        document.getElementById('images').innerHTML = '';
        document.getElementById('images').appendChild(img);
    });*/

    /*leafletImage(map, function(err, canvas) {
        getBase64FromImageUrl(url_image,function(data){

            $("#boton_informe").html(html_boton);
            url_image = data;
            generar_informe(url_image,canvas.toDataURL("image/png"));

        });
    });*/

    var base = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 18,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
        '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        id: 'mapbox.streets'
    });

    var bing = L.tileLayer.bing('AisLQm3JkrOKysYfF9FiIkwkH-kIryIOeJcEs4JV-Qb9fgdBZk3tM4NmTe-e94Zr');

    var openCycle = L.tileLayer('https://tile.thunderforest.com/cycle/{z}/{x}/{y}.png?apikey=dda4faab5df24211a8d46b5b607f51d6', {
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

    var baseLayers = {
        "Bing maps": bing,
        "Open street map": base,
        "IGN": ign,
        "Open cycle map": openCycle
    };

    map = L.map('mapaID', {
            preferCanvas:true,
            center: [40.0000000, -4.0000000],
            zoom: 6,
            layers: [base, bing, ign, openCycle]
    });

    L.control.layers(baseLayers).addTo(map);

    var editableLayers = new L.FeatureGroup();
    map.addLayer(editableLayers);

    if(geo){
        var geoJson2 = JSON.parse(geo);
        var geoJSONLayer = L.geoJson(geoJson2);
        editableLayers.clearLayers();

        geoJSONLayer.eachLayer(
            function(l){
              editableLayers.addLayer(l);
            }
        );

        map.fitBounds(geoJSONLayer.getBounds());
            $('#geometria_string').val(geo);
    }


});

function enableSpinner() {
    document.getElementById('spinner').style.display = 'block';
    document.getElementById('dwnButton').style.display = 'none'
}

function disableSpinner() {
    document.getElementById('spinner').style.display = 'none';
    document.getElementById('dwnButton').style.display = 'block'
}


