$(document).ready(function() {



});





var compararRodal = function(){
    var rodalSelected = $('.rodalSelected').val();

    if (rodalSelected === ''){
        alert ("Por favor seleccione un rodal");
    }else{
        location.href = "/redbosques/comparador/" + rodalSelected + "/";
    }

};
