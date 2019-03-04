var ccaa_rodalForm = function(){
    var ccaaSelected = $('#id_comautonom').val();
    if(ccaaSelected){
        $('#id_comautonom_cod').val(ccaaSelected);
    }

    $('#id_provincia_cod').val('');
    $('#id_municipio1').val('');

    $.ajax({
            url: _ccaaFilter_url + "?id=" + ccaaSelected,
            method: "GET",
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },

            success: function( data, textStatus, jqXHR ) {
                if(data){
                    var provincias = data.provincias;
                    var municipios = data.municipios;
                    $('#id_provincia .provincia').remove();
                    $('#id_municipio_cod .municipio').remove();

                    provincias.forEach(p => {
                        $('#id_provincia').append('<option class="provincia" value="' + p.cod + '">'+ p.nombre + '</option>');
                    });


                    municipios.forEach(m => {
                        $('#id_municipio_cod').append('<option class="municipio" value="' + m.id + '">'+ m.nombre + '</option>');
                    });

                }
            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });

};

var prov_rodalForm = function(){
    var provSelected = $('#id_provincia').val();
    if(provSelected){
        $('#id_provincia_cod').val(provSelected);
        console.log(provSelected);
    }
    $('#id_municipio1').val('');

    $.ajax({
        url: _provFilter_url + '?id=' + provSelected,
        method: "GET",
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                var csrftoken = getCookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },

        success: function( data, textStatus, jqXHR ) {
            if(data){
                var municipios = data.municipios;
                 $('#id_municipio_cod .municipio').remove();

                 municipios.forEach(m => {
                        console.log(m);
                        $('#id_municipio_cod').append('<option class="municipio" value="' + m.id + '">'+ m.nombre + '</option>');
                 });
            }
        },
        error: function(jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        }
    });
};

var muni_rodalForm = function(){
    var muniSelected = $('#id_municipio_cod').val();
    if(muniSelected){
        $('#id_municipio1').val(muniSelected);
    }
};

