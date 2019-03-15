$("#abrirPopup").click(function(){

    $("#instruc").dialog({
      modal: true,
      buttons: {
        Cerrar: function() {
          $( this ).dialog( "close" );
        }
      },
      draggable: false,
      classes: {
            "ui-dialog": "popupInstrucciones"
      }
    });

});