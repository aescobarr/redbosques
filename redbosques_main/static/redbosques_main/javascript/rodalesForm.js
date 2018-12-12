$(document).ready(function() {
      var map = L.map('map').setView([40.0000000, -4.0000000], 5);

  /*L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);*/


  var base = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
            maxZoom: 18,
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
                '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
                'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            id: 'mapbox.streets'
    }).addTo(map);;


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
    console.log(e.layerType);
    editableLayers.addLayer(layer);
    console.log(editableLayers.toGeoJSON());
    $('#geometria').val(JSON.stringify(editableLayers.toGeoJSON()));
    console.log(JSON.stringify(editableLayers.toGeoJSON()));
  });

});

var sendData = function(){

    var test = $('#geometria').val();
    //console.log(test['geometry']);

    url = '/redbosques/rodalFormData'

    $.ajax({
    url: url,
    method: "POST",
    data: { test },
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            var csrftoken = getCookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    },

    success: function( data, textStatus, jqXHR ) {
        console.log("Tot OK !!!!")
    },
    error: function(jqXHR, textStatus, errorThrown){
        console.log(errorThrown);
    }
});




}



