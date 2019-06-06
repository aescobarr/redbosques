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



var fichaRodal = function(){
    var rodalSelected = $('.rodalPDFselected').val();
    if (rodalSelected === ''){
        location.href = "/redbosques/menu";
    }else{
        location.href = "/redbosques/fichaRodal/" + rodalSelected + "/";
    }
}


/*$.ajaxSetup({
  beforeSend:function(jqXHR,settings){
    if (settings.dataType === 'binary'){
      settings.xhr().responseType='arraybuffer';
      settings.processData=false;
    }
  }
})*/





