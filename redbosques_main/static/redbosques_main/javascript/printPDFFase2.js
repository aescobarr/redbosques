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
        "Mapa Base de España - IGNBaseTodo": ign,
        "Open street map": base,
        //"Open cycle map": openCycle
    };

    map = L.map('mapaID', {
            preferCanvas:true,
            center: [40.0000000, -4.0000000],
            zoom: 6,
            layers: [base, ign]
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

var crearPDF = function(id_rodal, token){

    enableSpinner();
    url = '/redbosques/crearPDF/' + id_rodal;
    var filename = "Nombre.pdf";
    var img = document.createElement('img');
    var imagen;

    leafletImage(map, function(err, canvas) {
        var dimensions = map.getSize();
        img.width = dimensions.x;
        img.height = dimensions.y;
        img.src = canvas.toDataURL("image/png");
        img.id = 'printMapImage'


        document.getElementById('images').innerHTML = '';
        document.getElementById('images').appendChild(img);

        var formData = new FormData();

        imagen = img.src
        url = url + '/';

        formData.append("image", imagen);

        var xhr = new XMLHttpRequest();
        xhr.open("POST", url, true);
        xhr.setRequestHeader("X-CSRFToken", token);
        xhr.responseType = "arraybuffer";
        xhr.onload = function () {
            if (this.status === 200) {
                var blob = new Blob([xhr.response], {type: 'application/pdf', filename: 'test.pdf'});
                var objectUrl = URL.createObjectURL(blob);
                var a = document.createElement('a'), blob;
                disableSpinner();
                window.open(objectUrl);
            }
        }
        xhr.send(formData);

    });



};

var valoresMetricos = function(element){
    jQuery.each(element, function(i, actual) {
        if(!element[i].valorunidad || element[i].valorunidad == null){
            $('.valMet_' + element[i].indicador_cod).html('---');
        }else{
            $('.valMet_' + element[i].indicador_cod).html(element[i].valorunidad);
        }
    });
};


