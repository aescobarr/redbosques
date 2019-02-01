
$(document).ready(function(){

    // cached_data['tipo_bosque']['habitat']['cc_aa']['rodal']

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
    }

    function tree_enable(root){
        $('#' + root.name).removeAttr('disabled');
        $('#' + root.name).removeClass("asyncload");
        for( var i = 0; i < root.children.length; i++ ){
            tree_enable(root.children[i]);
        }
    }

    function block_from(from_label){
        tree_disable(jerarquia_controls,from_label);
    }

    function unblock_all(){
        tree_enable(jerarquia_controls);
    }

    function unblock(selector){
        $('#' + selector).removeAttr('disabled');
        $('#' + selector).removeClass('asyncload');
    }

    function set_ccaa_data(data, id_selector){
        for(var i = 0; i < data.length; i++){
            $('#' + id_selector).append('<option value="' + data[i].codigo + '">' + data[i].nombre_es + '</option>')
        }
    }

    function set_regbio_data(data, id_selector){
        for(var i = 0; i < data.length; i++){
            $('#' + id_selector ).append('<option value="' + data[i].cod + '">' + data[i].nombre_es + '</option>')
        }
    }

    function load_biogeo_comp(selected_ccaa, selected_habitat){
        if(selected_ccaa == 'null'){
            resetUIRegBioGeoComp();
            block_from('selector_RegBio_Comp');
        }else{
            resetUIRegBioGeoComp();
            setLoadingUI('selector_RegBio_Comp');
            block_from('selector_RegBio_Comp');
            if(cached_data_regbio[selected_ccaa+selected_habitat]!=null){
                var data = cached_data_regbio[selected_ccaa+selected_habitat];
                set_regbio_data(data,'selector_RegBio_Comp');
                unblock('selector_RegBio_Comp');
            }else{
                $.ajax({
                    url: _regbiogeo_list + "?ca=" + escape(selected_ccaa) + "&hab=" + escape(selected_habitat),
                    method: "GET",
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type)) {
                            var csrftoken = getCookie('csrftoken');
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    },
                    success: function( data, textStatus, jqXHR ) {
                        cached_data_regbio[selected_ccaa+selected_habitat] = data;
                        set_regbio_data(data,'selector_RegBio_Comp');
                        unblock('selector_RegBio_Comp');
                    },
                    error: function(jqXHR, textStatus, errorThrown){
                        console.log('error');
                        unblock_all();
                    }
                });
            }
        }
    }

    function load_biogeo(selected_ccaa, selected_habitat){
        if(selected_ccaa == 'null' || selected_habitat == 'null'){
            resetUIRegBioGeo();
            block_from('selector_RegBio');
        }else{
            resetUIRegBioGeo();
            setLoadingUI('selector_RegBio')
            block_from('selector_RegBio');
            if(cached_data_regbio[selected_ccaa+selected_habitat] != null){
                var data = cached_data_regbio[selected_ccaa+selected_habitat];
                set_regbio_data(data,'selector_RegBio');
                if(data.length==1){
                    $('#selector_RegBio').val(data[0].cod);
                    load_rodals($('#habitat').find(":selected").val(),$('#selector_ComAut').find(":selected").val(),$('#selector_RegBio').find(":selected").val());
                }
                //unblock_all();
                unblock('selector_RegBio');
            }else{
                $.ajax({
                    url: _regbiogeo_list + "?ca=" + escape(selected_ccaa) + "&hab=" + escape(selected_habitat),
                    method: "GET",
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type)) {
                            var csrftoken = getCookie('csrftoken');
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    },
                    success: function( data, textStatus, jqXHR ) {
                        cached_data_regbio[selected_ccaa+selected_habitat]=data;
                        set_regbio_data(data,'selector_RegBio');
                        if(data.length==1){
                            $('#selector_RegBio').val(data[0].cod);
                            load_rodals($('#habitat').find(":selected").val(),$('#selector_ComAut').find(":selected").val(),$('#selector_RegBio').find(":selected").val());
                        }
                        //unblock_all();
                        unblock('selector_RegBio');
                    },
                    error: function(jqXHR, textStatus, errorThrown){
                        console.log('error');
                        unblock_all();
                    }
                });
            }
        }
    }

    function load_cc_aa_comp(selected){
        if(selected == 'null'){
            resetUICcaaComp();
            block_from('selector_ComAut_Comp');
        }else{
            resetUICcaaComp();
            setLoadingUI('selector_ComAut_Comp');
            block_from('selector_ComAut_Comp');
            if(cached_data_cc_aa[selected]!=null){
                var data = cached_data_cc_aa[selected];
                set_ccaa_data(data,'selector_ComAut_Comp');
                 if(data.length == 1){
                    $('#selector_ComAut_Comp').val(data[0].codigo);
                    load_biogeo_comp(data[0].codigo,$('#habitat').find(":selected").val());
                 }
                 //unblock_all();
                 unblock('selector_ComAut_Comp');
            }else{
                $.ajax({
                    url: _cc_aa_list + "?hab=" + escape(selected),
                    method: "GET",
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type)) {
                            var csrftoken = getCookie('csrftoken');
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    },
                    success: function( data, textStatus, jqXHR ) {
                         cached_data_cc_aa[selected] = data;
                         set_ccaa_data(data,'selector_ComAut_Comp');
                         if(data.length == 1){
                            $('#selector_ComAut_Comp').val(data[0].codigo);
                            load_biogeo_comp(data[0].codigo,$('#habitat').find(":selected").val());
                         }
                         //unblock_all();
                         unblock('selector_ComAut_Comp');
                    },
                    error: function(jqXHR, textStatus, errorThrown){
                        console.log('error');
                        unblock_all();
                    }
                });
            }
        }
    }

    function load_cc_aa(selected){
        if(selected == 'null'){
            resetUICcaa();
            block_from('selector_ComAut');
        }else{
            resetUICcaa();
            setLoadingUI('selector_ComAut');
            block_from('selector_ComAut');
            if(cached_data_cc_aa[selected]!=null){
                var data = cached_data_cc_aa[selected];
                set_ccaa_data(data,'selector_ComAut');
                 if(data.length == 1){
                    $('#selector_ComAut').val(data[0].codigo);
                    load_biogeo(data[0].codigo,$('#habitat').find(":selected").val());
                 }
                 //unblock_all();
                 unblock('selector_ComAut');
            }else{
                $.ajax({
                    url: _cc_aa_list + "?hab=" + escape(selected),
                    method: "GET",
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type)) {
                            var csrftoken = getCookie('csrftoken');
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    },
                    success: function( data, textStatus, jqXHR ) {
                         cached_data_cc_aa[selected] = data;
                         set_ccaa_data(data,'selector_ComAut');
                         if(data.length == 1){
                            $('#selector_ComAut').val(data[0].codigo);
                            load_biogeo(data[0].codigo,$('#habitat').find(":selected").val());
                         }
                         //unblock_all();
                         unblock('selector_ComAut');
                    },
                    error: function(jqXHR, textStatus, errorThrown){
                        console.log('error');
                        unblock_all();
                    }
                });
            }
        }
    }

    function rodalData(valorRodal){
        if(valorRodal == 'null'){
            //clear taula
            $('.bgColorRod').html('');
        }else{
            var url = '/redbosques/valorRodal';
            url = url + '?vr=' + valorRodal;
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
                    rodalSelData = data.rodal;
                    //console.log(rodalSelData);
                    recorreRodal('', rodalSelData);
                    if(rodalReferencia){
                        calcDiferencia();
                        $('.grafico div').html('');
                        dataGraph(rodalSelData, rodalReferencia);
                    }
                },
                error: function(jqXHR, textStatus, errorThrown){
                    console.log(errorThrown);
                }
            });
        }
    };

    function initUI(){
        $('#tipoBosque').val("null");
        $('#habitat').val("null");
        block_from('selector_ComAut');
        block_from('selector_ComAut_Comp');
    }

    function resetUITable(){
        $('td.diff-col').html('---');
        $('td.col-diff').html('---');
        $('.valGraf').html('---');
        $('.valGraf').css("background-color", "#FFFFFF");
        $('.divGraf').empty();
        $('.col-diff').removeAttr("style");
        $('.diff-col').removeAttr("style");
    }

    function resetUIRodal(){
        $('#selector_rodales').empty();
        $('#selector_rodales').append('<option value="null" selected="selected">Seleccione un rodal</option>');
        $('.bgColorRod').html('');
    }

    function resetUIRodalComp(){
        $('#selector_rodales_comp').empty();
        $('#selector_rodales_comp').append('<option value="null" selected="selected">Rodal / Conjunto de rodales a comparar</option>');
        $('#selector_rodales_comp').append('<option value="medRod">Todos los rodales</option>');
        resetUITable();
        //$('.bgColorRod').html('');
    }

    function resetUIRegBioGeo(){
        $('#selector_RegBio').empty();
        $('#selector_RegBio').append('<option value="null" selected="selected">Seleccione región biogeográfica</option>');
    }

    function resetUIRegBioGeoComp(){
        $('#selector_RegBio_Comp').empty();
        $('#selector_RegBio_Comp').append('<option value="null" selected="selected">Seleccione región biogeográfica</option>');
        $('#selector_RegBio_Comp').append('<option value="all">Todas las Regiones Biogeográficas</option>');
    }

    function resetUIHabitat(){
        $('#habitat').empty();
        $('#habitat').append('<option value="null" selected="selected">Seleccione un hábitat</option>');
    }

    function setLoadingUI(select_id){
        $('#' + select_id).addClass("asyncload");
        //$('#' + select_id).attr('disabled', 'disabled');
    }

    function resetUICcaa(){
        $('#selector_ComAut').empty();
        $('#selector_ComAut').append('<option value="null" selected="selected">Seleccione Comunidad autónoma</option>');
    }

    function resetUICcaaComp(){
        $('#selector_ComAut_Comp').empty();
        $('#selector_ComAut_Comp').append('<option value="null" selected="selected">Seleccione Comunidad autónoma</option>');
        $('#selector_ComAut_Comp').append('<option value="all" selected="selected">Todas las comunidades autónomas</option>');
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

    function loadHabitat(selected){
        resetUIHabitat();
        setLoadingUI('habitat');
        block_from('habitat');
        if(cached_data_habitat[selected]!=null){
            var data = cached_data_habitat[selected];
            set_habitat_data(data,'habitat');
             if(data.length == 1){
                $('#habitat').val(data[0].cod);
                load_cc_aa($('#habitat').find(":selected").val());
                load_cc_aa_comp($('#habitat').find(":selected").val());
             }
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
                    if(data.length == 1){
                        $('#habitat').val(data[0].cod);
                        load_cc_aa($('#habitat').find(":selected").val());
                        load_cc_aa_comp($('#habitat').find(":selected").val());
                    }
                    //unblock_all();
                    unblock('habitat');
                },
                error: function(jqXHR, textStatus, errorThrown){
                    console.log('error');
                    unblock_all();
                    //unblock('habitat');
                }
            });
        }
    }

    function load_rodals_comp(idHabitat,idComAut,idRegBiogeo,rodRef){
        if( idComAut == 'null' || idRegBiogeo == 'null' ){
            resetUIRodalComp();
            block_from('selector_rodales_comp');
        }else{
            resetUIRodalComp();
            setLoadingUI('selector_rodales_comp');
            block_from('selector_rodales_comp');
            if(cached_data_rodal[idHabitat+idComAut+idRegBiogeo+rodRef]!=null){
                var data = cached_data_rodal[idHabitat+idComAut+idRegBiogeo+rodRef];
                for(var i = 0; i < data.length; i++){
                    var label = data[i].nombre;
                    if(data[i].rodalref && data[i].rodalref == 1){
                        label = label + ' *';
                    }
                    $('#selector_rodales_comp').append('<option value="' + data[i].id_rodal + '">' + label + '</option>')
                }
                unblock('selector_rodales_comp');
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
                if(rodRef != null){
                    params.push('rodRef=' + escape(rodRef));
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
                        cached_data_rodal[idHabitat+idComAut+idRegBiogeo+rodRef] = data;
                        for(var i = 0; i < data.length; i++){
                            var label = data[i].nombre;
                            if(data[i].rodalref && data[i].rodalref == 1){
                                label = label + ' *';
                            }
                            $('#selector_rodales_comp').append('<option value="' + data[i].id_rodal + '">' + label + '</option>')
                        }
                        unblock('selector_rodales_comp');
                    },
                    error: function(jqXHR, textStatus, errorThrown){
                        console.log(errorThrown);
                        unblock_all();
                    }
                });
            }
        }
    }

    function load_rodal_ref(idHabitat, idComAut, idRegBiogeo, valRod){
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
                            calcDiferencia();
                            $('.grafico div').html('');
                            dataGraph(rodalSelData, rodalReferencia);
                        }else{
                            $('.grafico div').html('');
                            $('td.diff-col').html('---');
                            $('td.col-diff').html('---');
                            $('td.col-diff').css("background-color", "#FFFFFF");
                            $('td.diff-col').css("background-color", "#FFFFFF");
                            $('.valGraf').html('---');
                            $('.valGraf').css("background-color", "#FFFFFF");
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
    };

    function set_rodal_data(data,selector){
        for(var i = 0; i < data.length; i++){
            var label = data[i].nombre;
            if(data[i].rodalref && data[i].rodalref == 1){
                label = label + ' *';
            }
            $('#' + selector ).append('<option value="' + data[i].id_rodal + '">' + label + '</option>')
         }
    }

    function load_rodals(idHabitat,idComAut,idRegBiogeo){
        if( idComAut == 'null' || idRegBiogeo == 'null' ){
            resetUIRodal();
            block_from('selector_rodales');
        }else{
            resetUIRodal();
            setLoadingUI('selector_rodales');
            block_from('selector_rodales');
            if(cached_data_rodal[idHabitat+idComAut+idRegBiogeo+'0']!=null){
                var data = cached_data_rodal[idHabitat+idComAut+idRegBiogeo+'0'];
                set_rodal_data(data,'selector_rodales');
                 if(data.length == 1){
                    $('#selector_rodales').val(data[0].id_rodal);
                    rodalData(data[0].id_rodal);
                 }
                //unblock_all();
                unblock('selector_rodales');
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
                        cached_data_rodal[idHabitat+idComAut+idRegBiogeo+'0'] = data;
                        set_rodal_data(data,'selector_rodales');
                         if(data.length == 1){
                            $('#selector_rodales').val(data[0].id_rodal);
                            rodalData(data[0].id_rodal);
                         }
                        //unblock_all();
                        unblock('selector_rodales');
                    },
                    error: function(jqXHR, textStatus, errorThrown){
                        console.log(errorThrown);
                        unblock_all();
                    }
                });
            }
        }
    }

    $('#tipoBosque').change(function(){
        var selected = $('#tipoBosque').find(":selected").val();
        resetUICcaa();
        resetUICcaaComp();
        resetUIRegBioGeo();
        resetUIRegBioGeoComp();
        resetUIRodal();
        resetUIRodalComp();
        loadHabitat(selected);
    });

    $('#habitat').change(function(){
        var selected = $('#habitat').find(":selected").val();
        resetUIRegBioGeo();
        resetUIRegBioGeoComp();
        resetUIRodal();
        resetUIRodalComp();
        load_cc_aa(selected);
        load_cc_aa_comp(selected);
    });

    $('#selector_ComAut').change(function(){
        var selected_ccaa = $('#selector_ComAut').find(":selected").val();
        var selected_habitat = $('#habitat').find(":selected").val();
        resetUIRegBioGeo();
        resetUIRodal();
        load_biogeo(selected_ccaa,selected_habitat);
    });

    $('#selector_ComAut_Comp').change(function(){
        var selected_ccaa = $('#selector_ComAut_Comp').find(":selected").val();
        var selected_habitat = $('#habitat').find(":selected").val();
        resetUIRegBioGeoComp();
        resetUIRodalComp();
        load_biogeo_comp(selected_ccaa,selected_habitat);
    });

    $('#selector_RegBio').change(function(){
        var idHabitat = $('#habitat').val();
        var idComAut = $('#selector_ComAut').val();
        var idRegBiogeo = $('#selector_RegBio').val();
        resetUIRodal();
        load_rodals(idHabitat,idComAut,idRegBiogeo);
    });

     $('#selector_RegBio_Comp').change(function(){
        var idHabitat = $('#habitat').val();
        var idComAut = $('#selector_ComAut_Comp').val();
        var idRegBiogeo = $('#selector_RegBio_Comp').val();
        var rodRef = getValorRodRefString();
        resetUIRodalComp();
        load_rodals_comp(idHabitat,idComAut,idRegBiogeo, rodRef);
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
        /*var rodRef = $('input[name=boolRodRef]:checked').val();
        rodRef == "True" ? rodRef = '1' : rodRef = '0';*/
        load_rodal_ref(idHabitat, idComAut, idRegBiogeo, valRod);
    });

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
        resetUIRodalComp();
        load_rodals_comp(idHabitat,idComAut,idRegBiogeo, rodRef);
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
        unblock('selector_ComAut_Comp');

        //load cc_aa in selectors and select starting elements
        set_ccaa_data(init_data.cc_aa_ini_list,'selector_ComAut');
        set_ccaa_data(init_data.cc_aa_ini_list,'selector_ComAut_Comp');
        $('#selector_ComAut').val(init_data.ccaa_ini);
        $('#selector_ComAut_Comp').val(init_data.ccaa_ini);

        //load regbio data in selectors and select starting elements
        set_regbio_data(init_data.reg_ini_list,'selector_RegBio');
        set_regbio_data(init_data.reg_ini_list,'selector_RegBio_Comp');
        $('#selector_RegBio').val(init_data.regbio_ini);

        //load rodal data in selectors and select starting elements
        set_rodal_data(init_data.rodals_ini_list,'selector_rodales');
        $('#selector_rodales').val(init_data.rodal_ini)

        //show rodal Data in table
        rodalData(init_data.rodal_ini);

        //cache everything
        cached_data_cc_aa[init_data.habitat_ini] = init_data.cc_aa_ini_list;
        cached_data_regbio[init_data.ccaa_ini + init_data.habitat_ini] = init_data.reg_ini_list;
        cached_data_rodal[init_data.habitat_ini + init_data.ccaa_ini + init_data.regbio_ini + false] = init_data.rodals_ini_list;
    }

});