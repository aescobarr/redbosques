$(document).ready(function() {




});

var editarRodal = function(){
        var editRodalSelected = $('.editRodalSelected').val();

        if (editRodalSelected === ''){
            //location.href = "/redbosques/comparador";
            alert("Por favor seleccione un rodal.")
        }else{
            location.href = "/redbosques/editrodalForm/" + editRodalSelected + "/";
        }
    };




var compararRodal = function(){
    var rodalSelected = $('.rodalSelected').val();

    if (rodalSelected === ''){
        location.href = "/redbosques/comparador_new";
    }else{
        location.href = "/redbosques/comparador_new/" + rodalSelected + "/";
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