var map;
$(document).ready(function() {
    //map = L.map('map').setView([40.0000000, -4.0000000], 5);
    /*if (geo){
        var test = JSON.parse(geo);
        var coord = test.coordinates[0];
        console.log(coord[0]);
        latlon = L.GeoJSON.coordsToLatLng(coord[0]);
        var map = L.map('map').setView(latlon, 12);
    }else{
        var map = L.map('map').setView([40.0000000, -4.0000000], 5);
    }*/

    var base = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
    });
    

    var openCycle = L.tileLayer('https://tile.thunderforest.com/cycle/{z}/{x}/{y}.png?apikey=dda4faab5df24211a8d46b5b607f51d6',{
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
		"Open street map": base,
		"IGN": ign,
		//"Open cycle map": openCycle
	};


	var map = L.map('map', {
            center: [40.0000000, -4.0000000],
            zoom: 6,
            layers: [base,ign]            
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


    /*map.on(L.Draw.Event.CREATED, function (e) {
        var type = e.layerType,layer = e.layer;
        editableLayers.addLayer(layer);
        var string_json = JSON.stringify(editableLayers.toGeoJSON());
        $('#geometria_string').val(string_json);
    });*/



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


    map.on(L.Draw.Event.CREATED, function (e) {

        var type = e.layerType,layer = e.layer;
        editableLayers.addLayer(layer);
        var string_json = JSON.stringify(editableLayers.toGeoJSON());
        $('#geometria_string').val(string_json);
        blockUnblockSubmit(string_json);
    });

    map.on(L.Draw.Event.EDITED, function(e){
        var string_json = JSON.stringify(editableLayers.toGeoJSON());
        $('#geometria_string').val(string_json);
        blockUnblockSubmit(string_json);
    });

    map.on(L.Draw.Event.DELETED, function(e){
        $('#geometria_string').val('');
        string_json = "";
        blockUnblockSubmit(string_json);
    });

    blockUnblockSubmit(geo);

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
                blockUnblockSubmit(string_json);
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

    var comunidadAutonoma = $('#id_comautonom_cod').val();
    if(comunidadAutonoma){
        $('#id_comautonom.selectBox option[value=' + comunidadAutonoma + ']').attr("selected", "selected");
    }

    var provincia = $('#id_provincia_cod').val();
    if(provincia){
        $('#id_provincia.selectBox option[value="' + provincia + '"]').attr("selected", "selected");
    }

    var municipio = $('#id_municipio1').val();
    if(municipio){
        $('#id_municipio_cod.selectBox option[value=' + municipio + ']').attr("selected", "selected");
    }

    var espcomp_cod = $("#id_espcomp_cod").val();
    if (espcomp_cod == ""){
        $("#altDomEspPrinAcomp").prop("disabled", true);
        $("#cavCubespPrinAcomp").prop("disabled", true);
    }



    if(geo == ""){
        $("#btnSubmitForm").prop("disabled", true);
    }else{
        $("#btnSubmitForm").prop("disabled", false);
    }


    if( missatge_geometria ){
        toastr.error(missatge_geometria,'No hay geometría');
    }
});



var disEnEspecieAcomp = function(){
    var espcomp_cod = $("#id_espcomp_cod").val();

    if (espcomp_cod == ""){
        $("#altDomEspPrinAcomp").prop("disabled", true);
        $("#altDomEspPrinAcomp").val('');
        $("#cavCubespPrinAcomp").prop("disabled", true);
        $("#cavCubespPrinAcomp").val('');
    }else if(espcomp_cod != ""){
        $("#altDomEspPrinAcomp").prop("disabled", false);
        $("#cavCubespPrinAcomp").prop("disabled", false);
    }
};

var blockUnblockSubmit = function(string_json){

    if(string_json == ""){
        $(".rodalOblig").show();
        $("#btnSubmitForm").prop("disabled", true);
    }else{
        $(".rodalOblig").hide();
        $("#btnSubmitForm").prop("disabled", false);
    }
};


