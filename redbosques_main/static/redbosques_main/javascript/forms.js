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

var changeDecimalDelimiter = $("[class*='dotDel']");

for(d=0; d<changeDecimalDelimiter.length; d++){
    changeDecimalDelimiter[d].addEventListener('input', evt => {
        var val = evt.target.value;
        var fieldName = evt.target.name;
        var id = evt.target.id;
        console.log(id);
        var test = val.replace(',', '.');
        $('#' + id).val(test);

    });
}

var modDelim = function(val, fieldName){
    var test = val.replace(',', '.');
    console.log(test);
    $('#id_' + fieldName).val(test);
}