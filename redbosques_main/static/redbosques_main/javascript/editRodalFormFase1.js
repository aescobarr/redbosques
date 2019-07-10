var map;
$(document).ready(function() {
    var base = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
            maxZoom: 18,
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
                '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
                'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            id: 'mapbox.streets'
    });

    var bing = L.tileLayer.bing('AisLQm3JkrOKysYfF9FiIkwkH-kIryIOeJcEs4JV-Qb9fgdBZk3tM4NmTe-e94Zr');

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
		"Bing maps": bing,
		"Open street map": base,
		"IGN": ign,
		"Open cycle map": openCycle
	};


	var map = L.map('map', {
            center: [40.0000000, -4.0000000],
            zoom: 6,
            layers: [base,bing,ign,openCycle]
    });

    L.control.layers(baseLayers).addTo(map);

    var editableLayers = new L.FeatureGroup();


    var draw_options = {
      position: 'topleft',
      draw: {
          polyline: false,
          polygon: false,
          circle: false,
          rectangle: false,
          marker: true,
          circlemarker: false
      },
      edit: {
          featureGroup: editableLayers,
          remove: true,
          edit: true
      }
    };


    var drawControl = new L.Control.Draw(draw_options);
    map.addLayer(editableLayers);
    map.addControl(drawControl);


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
        $('#marker_string').val(geo);
    }


    map.on(L.Draw.Event.CREATED, function (e) {

        lat = e.layer._latlng.lat;
        lon = e.layer._latlng.lng;

        var type = e.layerType,layer = e.layer;

        if(editableLayers.getLayers().length > 0){
            editableLayers.clearLayers();
            string_json = '';
        }

        editableLayers.addLayer(layer);
        Marker = L.marker([lat,lon]);

        var string_json = JSON.stringify(Marker.toGeoJSON());
        $('#marker_string').val(string_json);

        blockUnblockSubmit(string_json);
    });

    map.on(L.Draw.Event.EDITED, function(e){
        /*var layers = editableLayers.toGeoJSON();
        console.log(layers);
        var lat = layers['features'][0]['geometry']['coordinates'][0];
        var lon = layers['features'][0]['geometry']['coordinates'][1];

        Marker = L.marker([lat,lon]).addTo(editableLayers);

        var string_json = JSON.stringify(Marker.toGeoJSON());
        $('#marker_string').val(string_json);*/

        var layers = e.layers;
        layers.eachLayer(function (layer) {
             lat = layer._latlng.lat;
             lon = layer._latlng.lng;
         });

        Marker = L.marker([lat,lon]);

        var string_json = JSON.stringify(Marker.toGeoJSON());
        $('#marker_string').val(string_json);
        blockUnblockSubmit(string_json);

    });

    map.on(L.Draw.Event.DELETED, function(e){
        $('#marker_string').val('');
        string_json = "";
        blockUnblockSubmit(string_json);
    });

    blockUnblockSubmit(geo);

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

    var valspparb = $('#id_valspparb').val();

    if(valspparb){
        $('#id_valspparb_sel.selectBox option[value=' + valspparb + ']').attr("selected", "selected");
    }

    var valmasa = $('#id_valmasa').val();

    if(valmasa){
        $('#id_valmasa_sel.selectBox option[value=' + valmasa + ']').attr("selected", "selected");
    }

    var valestratos = $('#id_valestratos').val();
    if(valestratos){
        $('#id_valestratos_sel.selectBox option[value=' + valestratos + ']').attr("selected", "selected");
    }

    var valarboexcep = $('#id_valarboexcep').val();
    if(valarboexcep){
        $('#id_valarboexcep_sel.selectBox option[value=' + valarboexcep + ']').attr("selected", "selected");
    }

    var valmmpie = $('#id_valmmpie').val();
    if(valmmpie){
        $('#id_valmmpie_sel.selectBox option[value=' + valmmpie + ']').attr("selected", "selected");
    }

    var valmmsuelo = $('#id_valmmsuelo').val();
    if(valmmsuelo){
        $('#id_valmmsuelo_sel.selectBox option[value=' + valmmsuelo + ']').attr("selected", "selected");
    }

    var valmicrohab = $('#id_valmicrohab').val();
    if(valmicrohab){
        $('#id_valmicrohab_sel.selectBox option[value=' + valmicrohab + ']').attr("selected", "selected");
    }

    var valhuecos = $('#id_valhuecos').val();
    if(valhuecos){
        $('#id_valhuecos_sel.selectBox option[value=' + valhuecos + ']').attr("selected", "selected");
    }

    var valregen = $('#id_valregen').val();
    if(valregen){
        $('#id_valregen_sel.selectBox option[value=' + valregen + ']').attr("selected", "selected");
    }

    var volarrodal = $('#id_volarrodal').val();
    if(volarrodal){
        $('#id_volarrodal_val').val(volarrodal);
    }

    if (volarrodal >=1 && volarrodal <=3){
	    $('.valTxt').html("Rodal con naturalidad baja");
    }else if (volarrodal >=4 && volarrodal <=6){
	    $('.valTxt').html("Rodal con tendencia a la naturalidad");
	}else if (volarrodal >=7 && volarrodal <=9){
	    $('.valTxt').html("Rodal con indicios consistentes de un nivel elevado de naturalidad");
	}else{
	    "-"
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


function sumar(valor) {
    var array = [];
    var total = 0;
    array[0] = $(id_valspparb_sel).val();
    array[1] = $(id_valmasa_sel).val();
    array[2] = $(id_valestratos_sel).val();
    array[3] = $(id_valarboexcep_sel).val();
    array[4] = $(id_valmmpie_sel).val();
    array[5] = $(id_valmmsuelo_sel).val();
    array[6] = $(id_valmicrohab_sel).val();
    array[7] = $(id_valhuecos_sel).val();
    array[8] = $(id_valregen_sel).val();

    for (i=0; i<array.length; i++){
        if (array[i] != "null"){
            if(array[i] == "True"){
                //total = total + parseInt(array[i]);
                total = total + 1;
            }
        }
    }

	$('#id_volarrodal').val(total);
	$('#id_volarrodal_val').val(total);

	if (total >=1 && total <=3){
	    $('.valTxt').html("Rodal con naturalidad baja");
    }else if (total >=4 && total <=6){
	    $('.valTxt').html("Rodal con tendencia a la naturalidad");
	}else if (total >=7 && total <=9){
	    $('.valTxt').html("Rodal con indicios consistentes de un nivel elevado de naturalidad");
	}else{
	    "-"
	}
}

$(".selectBox").click(function(event) {
    var idData = $(this).attr('id');
    var idCampo = idData.split("_sel");
    var valor = $('#' + idData).children("option:selected").val();
    $('#' + idCampo[0]).val(valor);
});



