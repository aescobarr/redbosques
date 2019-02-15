var map;
$(document).ready(function() {
    map = L.map('map').setView([40.0000000, -4.0000000], 5);
    /*if (geo){
        var test = JSON.parse(geo);
        var coord = test.coordinates[0];
        console.log(coord[0]);
        latlon = L.GeoJSON.coordsToLatLng(coord[0]);
        var map = L.map('map').setView(latlon, 12);
    }else{
        var map = L.map('map').setView([40.0000000, -4.0000000], 5);
    }*/

    var base = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
            maxZoom: 18,
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
                '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
                'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            id: 'mapbox.streets'
    }).addTo(map);



    var editableLayers = new L.FeatureGroup();

    var draw_options = {
      position: 'topleft',
      draw: {
          polyline: false,
          polygon: {
              allowIntersection: false, // Restricts shapes to simple polygons
              drawError: {
                  color: '#FF0000', // Color the shape will turn when intersects
                  message: '<strong>Oh snap!<strong> you can\'t draw that!' // Message that will show when intersect
              },
              shapeOptions: {
                  color: '#33cc33'
              }
          },
          circle: false,
          rectangle: false,
          marker: false,
          circlemarker: false
      },
      edit: {
          featureGroup: editableLayers,
          remove: true
      }
    };

    var drawControl = new L.Control.Draw(draw_options);
    map.addLayer(editableLayers);
    map.addControl(drawControl);


    /*map.on(L.Draw.Event.CREATED, function (e) {
        var type = e.layerType,layer = e.layer;
        editableLayers.addLayer(layer);
        var string_json = JSON.stringify(editableLayers.toGeoJSON());
        $('#geometria_string').val(string_json);
    });*/




    var geoJson2 = JSON.parse(geo);
    var geoJSONLayer = L.geoJson(geoJson2);
    editableLayers.clearLayers();

    geoJSONLayer.eachLayer(
        function(l){
          editableLayers.addLayer(l);
        }
    );

    map.fitBounds(geoJSONLayer.getBounds());


    map.on(L.Draw.Event.CREATED, function (e) {

        var type = e.layerType,layer = e.layer;
        editableLayers.addLayer(layer);
        var string_json = JSON.stringify(editableLayers.toGeoJSON());
        console.log(string_json);
        $('#geometria_string').val(string_json);
    });

    map.on(L.Draw.Event.EDITED, function(e){
        var string_json = JSON.stringify(editableLayers.toGeoJSON());
        console.log(string_json);
        $('#geometria_string').val(string_json);
    });

    map.on(L.Draw.Event.DELETED, function(e){
        console.log("eliminado");
        $('#geometria_string').val('');
    });

});


