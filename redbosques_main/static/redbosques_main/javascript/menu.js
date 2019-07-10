$(document).ready(function() {




});

/*------- Fase 2---------- */

var editarRodal = function(){
        var editRodalSelected = $('.editRodalSelected').val();

        if (editRodalSelected === ''){
            //location.href = "/redbosques/comparador";
            alert("Por favor seleccione un rodal.")
        }else{
            location.href = "/redbosques/editrodalForm/" + editRodalSelected + "/";
        }
};



var eliminarRodal = function(){
        var eliminarRodalSelected = $('.editRodalSelected').val();

        if (eliminarRodalSelected === ''){
            alert("Por favor seleccione un rodal.")
        }else{
            var resp = confirm("Estas seguro que deseas eliminar el rodal?");

            if(resp == true){
                location.href = "/redbosques/eliminarRodal/" + eliminarRodalSelected + "/";
            }
        }
};

var fichaRodal = function(){
    var rodalSelected = $('.editRodalSelected').val();
    if (rodalSelected === ''){
        //location.href = "/redbosques/menu";
        alert("Por favor seleccione un rodal.")
    }else{
        location.href = "/redbosques/fichaRodal/" + rodalSelected + "/";
    }
}


/*------- Fase 1---------- */

var editarRodalFase1 = function(){
        var editRodalF1Selected = $('.editRodalF1Selected').val();

        if (editRodalF1Selected === ''){
            //location.href = "/redbosques/comparador";
            alert("Por favor seleccione un rodal.")
        }else{
            console.log(editRodalF1Selected);
            location.href = "/redbosques/editRodalFormFase1/" + editRodalF1Selected + "/";
        }
};



var eliminarRodalFase1 = function(){
        var rodalF1Selected = $('.editRodalF1Selected').val();

        if (rodalF1Selected === ''){
            alert("Por favor seleccione un rodal.")
        }else{
            var resp = confirm("Estas seguro que deseas eliminar el rodal?");

            if(resp == true){
                location.href = "/redbosques/eliminarRodalFase1/" + rodalF1Selected + "/";
            }
        }
};

var fichaRodalFase1 = function(){
    var rodalF1Selected = $('.editRodalF1Selected').val();
    if (rodalF1Selected === ''){
        alert("Por favor seleccione un rodal.")
    }else{
        location.href = "/redbosques/fichaRodalFase1/" + rodalF1Selected + "/";
    }
}

/* ------------------------------------------------------------------------------------------- */


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






/*$.ajaxSetup({
  beforeSend:function(jqXHR,settings){
    if (settings.dataType === 'binary'){
      settings.xhr().responseType='arraybuffer';
      settings.processData=false;
    }
  }
})*/





