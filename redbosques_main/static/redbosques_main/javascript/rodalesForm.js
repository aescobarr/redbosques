

$(document).ready(function() {
    setMapa();

});

var setMapa = function(){
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


    mymap = L.map('mapDraw', {
            center: [40.0000000, -4.0000000],
            zoom: 5,
            layers: [base,bing]
    });

    L.control.layers(baseLayers).addTo(mymap);
    mymap.addControl(drawControl);

}



var drawControl = new L.Control.Draw({
    position: 'topright',
    draw: {
        polyline: {
            metric: true
        },
        polygon: {
            allowIntersection: false,
            showArea: true,
            drawError: {
                color: '#b00b00',
                timeout: 1000
            },
            shapeOptions: {
                 color: '#bada55'

           }

        },

        rectangle: false,
        circle: false,
        marker: true
    },
    edit: {
        featureGroup: drawnItems,
        remove: true
    }
});




