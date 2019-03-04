$(document).ready(function(){


    var valpropbosc56_val = $('#id_valpropbosc56').val();

    if(valpropbosc56_val){
        $('#id_valpropbosc56_sel.selectBox option[value=' + valpropbosc56_val + ']').attr("selected", "selected");
    }

    var valagropasant_val = $('#id_valagropasant').val();
    if(valagropasant_val){
        $('#id_valagropasant_sel.selectBox option[value=' + valagropasant_val + ']').attr("selected", "selected");
    }

    var valforestant_val = $('#id_valforestant').val();
    if(valforestant_val){
        $('#id_valforestant_sel.selectBox option[value=' + valforestant_val + ']').attr("selected", "selected");
    }

    var valforestrec_val = $('#id_valforestrec').val();
    if(valforestrec_val){
        $('#id_valforestrec_sel.selectBox option[value=' + valforestrec_val + ']').attr("selected", "selected");
    }

    var valespinvas_val = $('#id_valespinvas').val();
    if(valespinvas_val){
        $('#id_valespinvas_sel.selectBox option[value=' + valespinvas_val + ']').attr("selected", "selected");
    }


    var valfragment_val = $('#id_valfragment').val();
    if(valfragment_val){
        $('#id_valfragment_sel.selectBox option[value=' + valfragment_val + ']').attr("selected", "selected");
    }

    var valcaza_val = $('#id_valcaza').val();
    if(valcaza_val){
        $('#id_valcaza_sel.selectBox option[value=' + valcaza_val + ']').attr("selected", "selected");
    }

    var valherbiv_val = $('#id_valherbiv').val();
    if(valherbiv_val){
        $('#id_valherbiv_sel.selectBox option[value=' + valherbiv_val + ']').attr("selected", "selected");
    }

    var valfrecuent_val = $('#id_valfrecuent').val();
    if(valfrecuent_val){
        $('#id_valfrecuent_sel.selectBox option[value=' + valfrecuent_val + ']').attr("selected", "selected");
    }

    var valdurabusos_val = $('#id_valdurabusos').val();
    if(valdurabusos_val){
        $('#id_valdurabusos_sel.selectBox option[value=' + valdurabusos_val + ']').attr("selected", "selected");
    }

});

    $(".selectBox").click(function(event) {
        var idData = $(this).attr('id');
        var idCampo = idData.split("_sel");
        console.log(idCampo[0]);
        var valor = $('#' + idData).children("option:selected").val();
        console.log(valor);
        $('#' + idCampo[0]).val(valor);
    });
