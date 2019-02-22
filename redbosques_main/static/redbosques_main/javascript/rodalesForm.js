$(document).ready(function() {
    //var map = L.map('map').setView([40.0000000, -4.0000000], 5);

    /*L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);*/


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


	var map = L.map('map', {
            center: [40.0000000, -4.0000000],
            zoom: 6,
            layers: [base,bing]
    });

	L.control.layers(baseLayers).addTo(map);

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

    map.on(L.Draw.Event.CREATED, function (e) {
        var type = e.layerType,layer = e.layer;
        editableLayers.addLayer(layer);

        console.log(layer);
        console.log(e.layerType);
        console.log(editableLayers.toGeoJSON());

        test = editableLayers.toGeoJSON();

        console.log(test);

        var string_json = JSON.stringify(editableLayers.toGeoJSON());
        //var latLng = map.layerPointToLatLng(string_json);
        console.log(string_json);
        $('#geometria_string').val(string_json);
        console.log(string_json);
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


    var importa_shapefile = function(filepath){
        $.ajax({
            url: _import_shapefile_url,
            data: 'path=' + encodeURI(filepath),
            method: 'GET',
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            },
            success: function( data, textStatus, jqXHR ) {
                editableLayers.clearLayers();
                var geoJson = JSON.parse(data.detail);
                var geoJSONLayer = L.geoJson(geoJson);
                geoJSONLayer.eachLayer(
                    function(l){
                        editableLayers.addLayer(l);
                    }
                );
                map.fitBounds(editableLayers.getBounds());
                var string_json = JSON.stringify(editableLayers.toGeoJSON());
                $('#geometria_string').val(string_json);
                $('.qq-upload-list').empty();
            },
            error: function(jqXHR, textStatus, errorThrown){
                if(jqXHR.responseJSON && jqXHR.responseJSON.detail){
                    alert('Error importando fichero: ' + jqXHR.responseJSON.detail);
                }else{
                    alert('Error importando fichero');
                }
                $('.qq-upload-list').empty();
            }
        });
    };

    var uploader = new qq.FileUploader({
        action: _ajax_upload_url,
        element: $('#fileuploader')[0],
        multiple: false,
        onComplete: function(id, fileName, responseJSON) {
            if(responseJSON.success) {
                var path = responseJSON.path;
                importa_shapefile(path);
            } else {
                alert('La subida del fichero shapefile ha fallado!');
            }
        },
        template:'<div class="qq-uploader">' +
            '<div class="qq-upload-drop-area"><span>Subir limites (shapefile, proyeccion EPSG:4326)</span></div>' +
            '<div class="qq-upload-button ui-widget-content ui-button ui-corner-all ui-state-default"><span>Subir limites (shapefile, proyeccion EPSG:4326)</span></div>' +
            '<ul class="qq-upload-list"></ul>' +
            '</div>',
        params: {
            'csrf_token': csrf_token,
            'csrf_name': 'csrfmiddlewaretoken',
            'csrf_xname': 'X-CSRFToken',
        }
    });


});
