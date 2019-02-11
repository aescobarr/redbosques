$(document).ready(function() {
    table = $('#user_admin_list').DataTable( {
        'ajax': {
            'url': _user_admin_list,
            'dataType': 'json'
        },
        'serverSide': true,
        'createdRow': function( row, data, dataIndex){
            if( data.user.is_active == true ){
                $(row).addClass('dtGreen');
            }else{
                $(row).addClass('dtOrange');
            }
        },
        'processing': true,
        'language': table_language,
        'pageLength': 25,
        'pagingType': 'full_numbers',
        'bLengthChange': false,
        'responsive': true,
        'order': [ [4, "desc"], [ 2, "asc" ] ],
        stateSave: true,
        'dom': '<"top"iflp<"clear">>rt<"bottom"iflp<"clear">>',
        stateSaveCallback: function(settings,data) {
            localStorage.setItem( 'DataTables_' + settings.sInstance, JSON.stringify(data) );
        },
        stateLoadCallback: function(settings) {
            return JSON.parse( localStorage.getItem( 'DataTables_' + settings.sInstance ) );
        },
        'columns': [
            { 'data': 'user.first_name' }
            ,{ 'data': 'user.last_name' }
            ,{ 'data': 'user.username' }
            ,{ 'data': 'institucion.nombre' }
            ,{ 'data': 'user.is_active' }
        ],
        'columnDefs': [
            {
                'targets':0,
                'title': 'Nombre'
            },
            {
                'targets':1,
                'title': 'Apellidos'
            },
            {
                'targets':2,
                'title': 'Nombre usuario'
            },
            {
                'targets':3,
                'title': 'Institución'
            }
            ,
            {
                'targets':4,
                'title': 'Activo?',
                "render": function(value){
                    var retVal = "";
                    if(value){
                        retVal += '<input type="checkbox" class="visible_chk" checked/>';
                    }else{
                        retVal += '<input type="checkbox" class="visible_chk"/>';
                    }
                    return retVal;
                }
            },
        ]
    } );

    var confirmDialog = function(message,id,pref_value){
        $('<div></div>').appendTo('body')
            .html('<div><h6>'+message+'</h6></div>')
            .dialog({
                modal: true, title: 'Activación/desactivación de usuario', zIndex: 10000, autoOpen: true,
                width: 'auto', resizable: false,
                buttons: {
                    Yes: function () {
                        activate_user(id,pref_value);
                        $(this).dialog("close");
                    },
                    No: function () {
                        table.ajax.reload(null,false);
                        $(this).dialog("close");
                    }
                },
                close: function (event, ui) {
                    $(this).remove();
                }
        });
    };

    var activate_user = function(user_id, pref_value){
        $.ajax({
            url: _user_activate_url,
            data: 'id=' + encodeURI(user_id) + '&value=' + encodeURI(pref_value),
            method: 'POST',
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    var csrftoken = getCookie('csrftoken');
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            },
            success: function( data, textStatus, jqXHR ) {
                table.ajax.reload(null,false);
            },
            error: function(jqXHR, textStatus, errorThrown){
                table.ajax.reload(null,false);
                alert("He ha producido un error activando/desactivando el usuario")
            }
        });
    }

    $('#user_admin_list tbody').on('click', 'td input.visible_chk', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );
        var id = row.data().user.id
        console.log(id);
        var activating = $(this).is(":checked");
        var message = '';
        if(activating){
            message = "Atención, estás a punto de <b>ACTIVAR</b> el usuario. Cuando lo hagas, este usuario podrá iniciar sesión en la aplicación y podrá introducir datos. ¿quieres Continuar?";
        }else{
            message = "Atención, estás a punto de <b>DESACTIVAR</b> el usuario. Un usuario inactivo no podrá iniciar sesión en la aplicación. ¿quieres Continuar?";
        }
        confirmDialog(message,id,activating);
    });

});