$(document).ready(function() {

var setMapData = function(data){
    marker_cluster.clearLayers();
    for(var i = 0; i < data.length; i++){
        var punt = data[i];
        /*var marker = L.marker([punt.y,punt.x]).bindPopup(
            '<b>Nombre habitad: </b>' + punt.habitat_nom + '<br><b>Localización: </b>' + punt.nombre + '<br><b>Comunidad Autónoma: </b>' + punt.Comunidad_autonoma).addTo(mymap);*/

        var marker = L.marker([punt.y,punt.x]).bindPopup(
            '<b>Nombre habitad: </b>' + punt.habitat_nom + '<br><b>Localización: </b>' + punt.nombre + '<br><b>Comunidad Autónoma: </b>' + punt.Comunidad_autonoma);

        marker_cluster.addLayer(marker);
        mymap.addLayer(marker_cluster);
    }
       if (testData){
            testData.markerClusterGroup();
       }

}

var updateMapData = function(){
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
            console.log(data);
            setMapData(data);
            /*var markers = setMapData(data);
            zoomToMarkers(markers);*/
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        }
    });
}

    //rodals = L.layerGroup();

var base = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
		maxZoom: 18,
		/*attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
			'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',*/
		id: 'mapbox.streets'
});

	//var mymap = L.map('mapid').setView([40.0000000, -4.0000000], 6);

	mymap = L.map('mapid', {
		center: [40.0000000, -4.0000000],
		zoom: 6,
		layers: [base]
	});

	marker_cluster = L.markerClusterGroup({
        spiderLegPolylineOptions: { weight: 1.5, color: '#222', opacity: 0.5 },
        spiderfyDistanceMultiplier: 3
    });

	//L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
		//maxZoom: 18,
		/*attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
			'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',*/
		//id: 'mapbox.streets'
	//}).addTo(mymap);

updateMapData();
selector_valoracion();


});


/*var tipoBosque = function(){
        alert($(".tipo_habitad option:checked").val());

        var codigo = $(".tipo_habitad").val();



    $.ajax({
        url: 'http://127.0.0.1:8000/redbosques/datos_habitat?h=' + codigo,
        method: "GET",
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                var csrftoken = getCookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },

        success: function( data, textStatus, jqXHR ) {

            //setMapData(data);
            selector_Habitad(data);

        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        }
    });
}*/


$('.tipo_bosque').on("click", function(){


        alert($(".tipo_habitad").val());

        var codigo = $(".tipo_habitad").val();



    $.ajax({
        url: 'http://127.0.0.1:8000/redbosques/datos_habitat?h=' + codigo,
        method: "GET",
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                var csrftoken = getCookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },

        success: function( data, textStatus, jqXHR ) {

            /*for(i=0; i<data.length; i++){
                console.log(data[i].nombre);
            }*/

            //setMapData(data);
            selector_Habitad(data);

        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        }
    });
});

function selector_Habitad(data){
    $(".tipo_habitad_sel").empty();
    for(i=0; i<data.length; i++){
        console.log(data[i].nombre);
        $(".tipo_habitad_sel").append('<option value=' + data[i].cod + '>' + data[i].nombre + '</option>');
    }
}

function selector_valoracion(){
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
        $(".selector_valoracion").append('<option value=' + Object.values(puntuacion[i]) + ' style="color:'+ Object.values(puntuacion[i]) +'">'  + Object.keys(puntuacion[i]) + '</option>');
    }
}



