$(document).ready(function() {



});





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