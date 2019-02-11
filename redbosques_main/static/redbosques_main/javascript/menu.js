$(document).ready(function() {




});

var editarRodal = function(){
        var rodalSelected = $('.rodalSelected').val();

        if (rodalSelected === ''){
            //location.href = "/redbosques/comparador";
            alert("Por favor seleccione un rodal.")
        }else{
            location.href = "/redbosques/editrodalForm/" + rodalSelected + "/";
        }
    };




var compararRodal = function(){
    var rodalSelected = $('.rodalSelected').val();

    if (rodalSelected === ''){
        location.href = "/redbosques/comparador";
    }else{
        location.href = "/redbosques/comparador/" + rodalSelected + "/";
    }
};



var zoomRodalMapa = function(){
    var rodalSelected = $('.rodalSelected').val();

    if (rodalSelected === ''){
        location.href = "/redbosques/herramientas";
    }else{
        location.href = "/redbosques/herramientas/" + rodalSelected + "/";
    }
};