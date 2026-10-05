$(document).ready(function() {
    var Marker = {};
    $('#id_volarrodal').val(0);

    $(".rodalOblig").show();
    $("#btnSubmitForm").prop("disabled", true);

    var base = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
    });

    /*var openCycle = L.tileLayer('https://tile.thunderforest.com/cycle/{z}/{x}/{y}.png?apikey=dda4faab5df24211a8d46b5b607f51d6', {
        attribution: 'Maps &copy; <a href="https://www.thunderforest.com">Thunderforest</a>, Data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>',
        maxZoom: 22
    });*/
    var ign = new L.TileLayer('https://tms-ign-base.idee.es/1.0.0/IGNBaseTodo/{z}/{x}/{-y}.jpeg',
    {
      maxZoom: 20,
      minZoom: 0,
      continuousWorld: true,
      attribution: '&copy; <a href="https://www.ign.es/web/ca/ide-area-nodo-ide-ign">Mapa Base de España - IGNBaseTodo</a>'
    });

    var baseLayers = {
		"Open street map": base,
		"Mapa Base de España - IGNBaseTodo": ign,
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

        /*$(".rodalOblig").hide();
        $("#btnSubmitForm").prop("disabled", false);*/


        blockUnblockSubmit(string_json);
    });

    map.on(L.Draw.Event.EDITED, function (e) {
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
        $("#btnSubmitForm").prop("disabled", true);
        string_json = '';
        blockUnblockSubmit(string_json);
    });


});


$(".selectBox").click(function(event) {
    var idData = $(this).attr('id');
    var idCampo = idData.split("_sel");
    var valor = $('#' + idData).children("option:selected").val();
    $('#' + idCampo[0]).val(valor);
});


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

    console.log(array);

    for (i=0; i<array.length; i++){
        if (array[i] != "null"){
            if(array[i] == "True"){
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

var blockUnblockSubmit = function(string_json){
    if(string_json == ""){
        $(".rodalOblig").show();
        $("#btnSubmitForm").prop("disabled", true);
    }else{
        $(".rodalOblig").hide();
        $("#btnSubmitForm").prop("disabled", false);
    }
};

var changeDecimalDelimiter = $("[class*='dotDel']");
var dotDel = function(){
    var test = parseFloat(val.replace(',', '.'));
}

for(d=0; d<changeDecimalDelimiter.length; d++){
    changeDecimalDelimiter[d].addEventListener('input', evt => {
        var val = evt.target.value;
        var fieldName = evt.target.name;
        console.log(val);
        modDelim(val, fieldName);
    });
}

var modDelim = function(val, fieldName){
    var test = val.replace(',', '.');
    console.log(test);
    $('#id_' + fieldName).val(test);
}