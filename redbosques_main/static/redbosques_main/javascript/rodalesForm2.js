$(document).ready(function(){


    var valpropbosc56_val = $('#id_valpropbosc56.id_valpropbosc56').val();

    console.log(valpropbosc56_val);

    $('#id_valpropbosc56.selectBox option[value=' + valpropbosc56_val + ']').attr("selected", "selected");


    var valagropasant_val = $('#id_valagropasant.id_valagropasant').val();
    $('#id_valagropasant.selectBox option[value=' + valagropasant_val + ']').attr("selected", "selected");

    var valforestant_val = $('#id_valforestant.id_valforestant').val();
    $('#id_valforestant.selectBox option[value=' + valforestant_val + ']').attr("selected", "selected");

    var valforestrec_val = $('#id_valforestrec.id_valforestrec').val();
    $('#id_valforestrec.selectBox option[value=' + valforestrec_val + ']').attr("selected", "selected");
    var valespinvas_val = $('#id_valespinvas.id_valespinvas').val();
    $('#id_valespinvas.selectBox option[value=' + valespinvas_val + ']').attr("selected", "selected");
    var valfragment_val = $('#id_valfragment.id_valfragment').val();
    $('#id_valfragment.selectBox option[value=' + valfragment_val + ']').attr("selected", "selected");

    var valcaza_val = $('#id_valcaza.id_valcaza').val();
    $('#id_valcaza.selectBox option[value=' + valcaza_val + ']').attr("selected", "selected");
    var valherbiv_val = $('#id_valherbiv.id_valherbiv').val();
    $('#id_valherbiv.selectBox option[value=' + valherbiv_val + ']').attr("selected", "selected");
    var valfrecuent_val = $('#id_valfrecuent.id_valfrecuent').val();
    $('#id_valfrecuent.selectBox option[value=' + valfrecuent_val + ']').attr("selected", "selected");
    var valdurabusos_val = $('#id_valdurabusos.id_valdurabusos').val();
    $('#id_valdurabusos.selectBox option[value=' + valdurabusos_val + ']').attr("selected", "selected");

});

    $(".selectBox").click(function(event) {
        var idData = $(this).attr('id');
        var valor = $('#' + idData).children("option:selected").val();
        $('.' + idData).val(valor);
    });
