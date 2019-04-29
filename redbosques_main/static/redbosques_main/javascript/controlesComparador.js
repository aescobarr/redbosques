$(document).ready(function(){

    function loadHabitat(selected){
        resetUIHabitat();
        setLoadingUI('habitat');
        block_from('habitat');
        if(cached_data_habitat[selected]!=null){
            var data = cached_data_habitat[selected];
            set_habitat_data(data,'habitat');
            unblock('habitat');
        }else{
            $.ajax({
                url: _habitat_list + "?tb=" + escape(selected),
                method: "GET",
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type)) {
                        var csrftoken = getCookie('csrftoken');
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                success: function( data, textStatus, jqXHR ) {
                    cached_data_habitat[selected] = data;
                    set_habitat_data(data,'habitat');
                    unblock('habitat');
                },
                error: function(jqXHR, textStatus, errorThrown){
                    console.log('error');
                    unblock_all();
                }
            });
        }
    };

    $('#tipoBosque').change(function(){
        var selected = $('#tipoBosque').find(":selected").val();
        resetUIRodal();
        resetUIRodalComp();
        loadHabitat(selected);
    });

    $('#habitat').change(function(){
        var selected = $('#habitat').find(":selected").val();
        if(selected == 'null'){
            block_from('selector_rodales');
            block_from('selector_ComAut');
            block_from('selector_ComAut_Comp');
        }else{
            var idHabitat = $('#habitat').val();
            var idComAut = $('#selector_ComAut').val();
            var idRegBiogeo = $('#selector_RegBio').val();
            load_rodals(idHabitat,idComAut,idRegBiogeo);
        }
    });

    initUI();

    if(init_data){
        //select initial habitat
        $('#habitat').val(init_data.habitat_ini);

        //unblock selectors
        unblock('selector_ComAut');
        unblock('selector_RegBio');
        unblock('selector_RegBio_Comp');
        unblock('selector_rodales');
        unblock('selector_rodales_comp');
        unblock('selector_ComAut_Comp');

        //load cc_aa in selectors and select starting elements
        set_ccaa_data(init_data.cc_aa_ini_list,'selector_ComAut');
        set_ccaa_data(init_data.cc_aa_ini_list,'selector_ComAut_Comp');

        //load regbio data in selectors and select starting elements
        set_regbio_data(init_data.reg_ini_list,'selector_RegBio');
        set_regbio_data(init_data.reg_ini_list,'selector_RegBio_Comp');

        //load rodal data in selectors and select starting elements
        set_rodal_data(init_data.rodals_ini_list,'selector_rodales');
        resetUIRodalComp();
        set_rodal_data(init_data.rodals_ini_list,'selector_rodales_comp');
        $('#selector_rodales').val(init_data.rodal_ini);

        //show rodal Data in table
        rodalData(init_data.rodal_ini);

        //cache everything
        rodals_habitat_cached[init_data.habitat_ini] = init_data.rodals_ini_list;
    }


});

var jerarquia_controls = {
        name : 'habitat',
        children : [
            {
                name: 'selector_ComAut',
                children: [
                    {
                        name: 'selector_RegBio',
                        children: [
                            {
                                name: 'selector_rodales',
                                children : []
                            }
                        ]
                    }
                ]
            },
            {
                name: 'selector_ComAut_Comp',
                children: [
                    {
                        name: 'selector_RegBio_Comp',
                        children: [
                            {
                                name: 'selector_rodales_comp',
                                children : []
                            }
                        ]
                    }
                ]
            }
        ]
    };



function tree_disable(root,disable_root){
    if(root.name == disable_root){
        $('#' + root.name).attr('disabled', 'disabled');
    }
    for( var i = 0; i < root.children.length; i++ ){
        if(root.name == disable_root){
            tree_disable(root.children[i],root.children[i].name);
        }else{
            tree_disable(root.children[i],disable_root);
        }
    }
};

function tree_enable(root){
    $('#' + root.name).removeAttr('disabled');
    $('#' + root.name).removeClass("asyncload");
    for( var i = 0; i < root.children.length; i++ ){
        tree_enable(root.children[i]);
    }
};

function block_from(from_label){
    tree_disable(jerarquia_controls,from_label);
};

function unblock_all(){
    tree_enable(jerarquia_controls);
};


function slice_cc_aa_data(rodals_data){
    var retVal = [];
    var id_set = new Set();
    for(var i = 0; i < rodals_data.length; i++){
        var n_data = rodals_data[i];
        if(!id_set.has(n_data.codi_ccaa)){
            retVal.push({ 'codigo': n_data.codi_ccaa, 'nombre_es': n_data.ccaa_nombre })
            id_set.add(n_data.codi_ccaa);
        }
    }
    retVal.sort(function(a,b){
        return (a.nombre_es < b.nombre_es) ? -1 : (a.nombre_es > b.nombre_es) ? 1 : 0;
    });
    return retVal;
}

function slice_regbio_data(rodals_data){
    var retVal = [];
    var id_set = new Set();
    for(var i = 0; i < rodals_data.length; i++){
        var n_data = rodals_data[i];
        if(!id_set.has(n_data.codi_rb)){
            retVal.push({ 'cod': n_data.codi_rb, 'nombre_es': n_data.nom_rb })
            id_set.add(n_data.codi_rb);
        }
    }
    retVal.sort(function(a,b){
        return (a.nombre_es < b.nombre_es) ? -1 : (a.nombre_es > b.nombre_es) ? 1 : 0;
    });
    return retVal;
}

var filtre_ccaa = function(row, selected_ccaa){
    if(selected_ccaa == 'null'){
        return true;
    }else if( selected_ccaa == row.codi_ccaa ){
        return true;
    }
    return false;
}

var filtre_regbio = function(row, selected_regbio){
    if(selected_regbio == 'null'){
        return true;
    }else if( selected_regbio == row.codi_rb ){
        return true;
    }
    return false;
}

var filtre_referencia = function(row, ref){
    if(ref == null || ref == '0'){
        return true;
    }else{
        if( ref == '1' && row.rodalref == true ){
            return true;
        }
    }
    return false;
}

function filter_rodal_data(unfiltered_rodal_data,selected_ccaa,selected_regbio, ref){
    var retData = [];
    for(var i = 0; i < unfiltered_rodal_data.length; i++){
        var candidate = unfiltered_rodal_data[i];
        if( filtre_ccaa(candidate,selected_ccaa) && filtre_regbio(candidate,selected_regbio) && filtre_referencia(candidate, ref) ){
            retData.push(candidate);
        }
    }
    return retData;
}

function setLoadingUI(select_id){
        $('#' + select_id).addClass("asyncload");
        //$('#' + select_id).attr('disabled', 'disabled');
    }

function initUI(){
    $('#tipoBosque').val("null");
    $('#habitat').val("null");
    $("#boolRodRefNO").prop("checked", true);
    block_from('selector_ComAut');
    block_from('selector_ComAut_Comp');
}

 function resetUIRodal(){
    $('.bgColorRod').html('');
    $('#selector_rodales').empty();
    $('#selector_rodales').append('<option value="null" selected="selected">Seleccione un rodal</option>');
    $('.bgColorRod').html('');
}

function resetUIRodalComp(){
    resetUITable();
    rodalReferencia = null;
    $('#selector_rodales_comp').empty();
    $('#selector_rodales_comp').append('<option value="null" selected="selected">Rodal / Conjunto de rodales a comparar</option>');
    $('#selector_rodales_comp').append('<option value="medRod">Todos los rodales</option>');
    //$('.bgColorRod').html('');
}

function resetUIRegBioGeo(){
    $('#selector_RegBio').empty();
    $('#selector_RegBio').append('<option value="null" selected="selected">Seleccione región biogeográfica</option>');
}

function resetUIRegBioGeoComp(){
    $('#selector_RegBio_Comp').empty();
    $('#selector_RegBio_Comp').append('<option value="null" selected="selected">Seleccione región biogeográfica</option>');
    //$('#selector_RegBio_Comp').append('<option value="all">Todas las Regiones Biogeográficas</option>');
}

function resetUIHabitat(){
    $('#habitat').empty();
    $('#habitat').append('<option value="null" selected="selected">Seleccione un hábitat</option>');
}

function set_rodal_data(data,selector){
    for(var i = 0; i < data.length; i++){
        var label = data[i].nombre;
        if(data[i].rodalref && data[i].rodalref == 1){
            label = label + ' *';
        }
        $('#' + selector ).append('<option value="' + data[i].id_rodal + '">' + label + '</option>')
     }
}

function unblock(selector){
    $('#' + selector).removeAttr('disabled');
    $('#' + selector).removeClass('asyncload');
};


function set_ccaa_data(data, id_selector){
    for(var i = 0; i < data.length; i++){
        $('#' + id_selector).append('<option value="' + data[i].codigo + '">' + data[i].nombre_es + '</option>')
    }
};

function set_regbio_data(data, id_selector){
    for(var i = 0; i < data.length; i++){
        $('#' + id_selector ).append('<option value="' + data[i].cod + '">' + data[i].nombre_es + '</option>')
    }
};

function resetUICcaa(){
    $('#selector_ComAut').empty();
    $('#selector_ComAut').append('<option value="null" selected="selected">Seleccione Comunidad autónoma</option>');
}

function resetUICcaaComp(){
    $('#selector_ComAut_Comp').empty();
    $('#selector_ComAut_Comp').append('<option value="null" selected="selected">Seleccione Comunidad autónoma</option>');
    //$('#selector_ComAut_Comp').append('<option value="all" selected="selected">Todas las comunidades autónomas</option>');
}

function getValorRodRefString(){
    var rodRef = $('input[name=boolRodRef]:checked').val();
    return rodRef == "True" ? rodRef = '1' : rodRef = '0';
}

function set_habitat_data(data,selector){
    for(var i = 0; i < data.length; i++){
        $('#' + selector ).append('<option value="' + data[i].habitat_cod + '">' + data[i].habitat_nombre + '</option>');
    }
}



function load_rodals(idHabitat,idComAut,idRegBiogeo){
    resetUIRodal();
    resetUIRodalComp();

    setLoadingUI('selector_rodales');
    setLoadingUI('selector_rodales_comp');

    block_from('selector_rodales');
    block_from('selector_ComAut');
    block_from('selector_ComAut_Comp');

    if(rodals_habitat_cached[idHabitat]!=null){
        var data = rodals_habitat_cached[idHabitat];
        refreshRodalData(data);
    }else{
        var params = [];
        if( idHabitat != "null" ){
            params.push('idHab=' + escape(idHabitat));
        }
        if( idComAut != "null" ){
            params.push('comAut=' + escape(idComAut));
        }
        if( idRegBiogeo != "null" ){
            params.push('regBiogeo=' + escape(idRegBiogeo));
        }
        var params_string = params.join("&");

        var url = '';
        if( params_string == '' ){
            url = _rodal_list;
        }else{
            url = _rodal_list + '?' + params_string;
        }

        $.ajax({
            url: url,
            method: "GET",
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },

            success: function( data, textStatus, jqXHR ) {
                rodals_habitat_cached[idHabitat] = data;
                refreshRodalData(data);
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
                unblock_all();
            }
        });
    }
};


/*function load_rodal_ref(idHabitat, idComAut, idRegBiogeo, valRod){
    url = _rodal_ref_list;
    var params = [];
    if(idHabitat != "null"){
        params.push('idHab='+escape(idHabitat));
    }
    if(idComAut != "null"){
        params.push('comAut='+escape(idComAut));
    }
    if(idRegBiogeo != "null"){
        params.push('regBiogeo='+escape(idRegBiogeo));
    }
    if(valRod != "null"){
        params.push('vr='+escape(valRod));
    }

    //params.push('rodRef='+escape(rodRef));

    url = url + "?" + params.join('&');

    if(valRod == "null"){
        resetUITable();
    }else{
        resetUITable();
        $('.data-table').addClass("asyncload-big");
        $.ajax({
            url: url,
            method: "GET",
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success: function( data, textStatus, jqXHR ) {
                rodalReferencia = data.rodal_referencia;
                recorreArbre('', rodalReferencia);
                //recorreRodal('', rodalSelData);
                if(rodalSelData){
                    if(rodalReferencia != null){
                        //calcDiferencia();
                        $('.grafico div').html('');
                        dataGraph(rodalSelData, rodalReferencia);
                    }else{
                        //('.grafico div').html('');
                        //$('td.diff-col').html('---');
                        //$('td.col-diff').html('---');
                        //$('td.col-diff').css("background-color", "#FFFFFF");
                        //$('td.diff-col').css("background-color", "#FFFFFF");
                        //$('.valGraf').html('---');
                        //$('.valGraf').css("background-color", "#FFFFFF");
                    }
                }
                if (valRod == "null"){
                    $('td.diff-col').html('---');
                    $('td.col-diff').html('---');
                }
                $('.data-table').removeClass("asyncload-big");
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
                $('.data-table').removeClass("asyncload-big");
            }
        });
    }
};*/



var refrescaLlistaRodals = function(){
    var selected_habitat = $('#habitat').find(":selected").val();
    var selected_ccaa = $('#selector_ComAut').find(":selected").val();
    var selected_regbio = $('#selector_RegBio').find(":selected").val();
    resetUIRodal();
    var unfiltered_rodal_data = rodals_habitat_cached[selected_habitat];
    var filtered_rodal_data = filter_rodal_data(unfiltered_rodal_data,selected_ccaa,selected_regbio);
    set_rodal_data(filtered_rodal_data,'selector_rodales');
}

var refrescaLlistaRodalsComp = function(){
    var selected_habitat = $('#habitat').find(":selected").val();
    var selected_ccaa = $('#selector_ComAut_Comp').find(":selected").val();
    var selected_regbio = $('#selector_RegBio_Comp').find(":selected").val();
    resetUIRodalComp();
    var unfiltered_rodal_data = rodals_habitat_cached[selected_habitat];
    var rodRef = getValorRodRefString();

    var filtered_rodal_data = filter_rodal_data(unfiltered_rodal_data,selected_ccaa,selected_regbio,rodRef);
    set_rodal_data(filtered_rodal_data,'selector_rodales_comp');
}

$('#selector_ComAut').change(function(){
    refrescaLlistaRodals();
});

$('#selector_ComAut_Comp').change(function(){
    refrescaLlistaRodalsComp();
});

$('#selector_RegBio').change(function(){
    refrescaLlistaRodals();
});

 $('#selector_RegBio_Comp').change(function(){
    refrescaLlistaRodalsComp();
 });

$('#selector_rodales').change(function(){
    var valRod = $('.selector_rodal option:selected').val();
    rodalData(valRod);
});

$('#selector_rodales_comp').change(function(){
    var idHabitat = $('#habitat').val();
    var idComAut = $('#selector_ComAut_Comp').val();
    var idRegBiogeo = $('#selector_RegBio_Comp').val();
    var valRod = $('#selector_rodales_comp option:selected').val();
    load_rodal_ref(idHabitat, idComAut, idRegBiogeo, valRod);
});

var getRodRefVal = function(){
    var val = $('input[type=radio][name=boolRodRef]:checked').val();
    if(val == 'True'){
        return '1';
    }else{
        return '0';
    }
}

$('input[type=radio][name=boolRodRef]').change(function() {
    var idHabitat = $('#habitat').val();
    var idComAut = $('#selector_ComAut_Comp').val();
    var idRegBiogeo = $('#selector_RegBio_Comp').val();
    var rodRef = '';
    if (this.value == 'True') {
        rodRef = '1';
    }else{
        rodRef = '0';
    }
    refrescaLlistaRodalsComp();
});

var refreshRodalData = function(data){
    resetUIRodalComp();
    set_rodal_data(data,'selector_rodales_comp');
    unblock('selector_rodales_comp');

    resetUIRodal();
    set_rodal_data(data,'selector_rodales');
    unblock('selector_rodales');

    data_ccaa = slice_cc_aa_data(data);
    data_regbio = slice_regbio_data(data);

    resetUICcaa();
    set_ccaa_data(data_ccaa,'selector_ComAut');
    unblock('selector_ComAut');

    resetUIRegBioGeo();
    set_regbio_data(data_regbio,'selector_RegBio');
    unblock('selector_RegBio');

    resetUICcaaComp();
    set_ccaa_data(data_ccaa,'selector_ComAut_Comp');
    unblock('selector_ComAut_Comp');

    resetUIRegBioGeoComp();
    set_regbio_data(data_regbio,'selector_RegBio_Comp');
    unblock('selector_RegBio_Comp');
}


