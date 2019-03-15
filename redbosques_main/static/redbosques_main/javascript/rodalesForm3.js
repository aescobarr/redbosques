$(function () {
  /* 1. OPEN THE FILE EXPLORER WINDOW */
  $(".js-upload-photos").click(function () {
    $("#fileupload").click();
  });

  /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
  $("#fileupload").fileupload({
    dataType: 'json',
    formData: [
        { name: "csrfmiddlewaretoken", value: "{{ csrf_token }}"}
    ],
    done: function (e, data) {  /* 3. PROCESS THE RESPONSE FROM THE SERVER */
      if (data.result.is_valid) {
        if(data.result.fotoprincipal){
            $("#gallery tbody").prepend(
            "<tr><td><a target='_blank' href='" + data.result.url +  "'><img id="+ data.result.id_foto +" style='height: 150px;' src='" + data.result.url + "'></a></td>" +
            "<td><p>Nombre: '" + data.result.nombre_foto +  "'</p><p name='fotoPrinc' value="+ data.result.id_foto +">"+ data.result.id_foto +"</p>" +
            "<button class='btn btn-danger btn-sm btn-del btn-del-img imatgeRodal deleteFoto' type='submit' id="+ data.result.id_foto +">Eliminar</button></td></tr>" +
            "<input id=" + data.result.id_foto + " type='radio' class='fotoPrinc' name='fotoPrinc' value='ture' checked='checked' onchange='fotoPrincipal()'>"
            )

            $('.fotoPrinc').is(':checked');
            var id_foto_princ = data.result.id_foto;
            fotoPrincipal(id_foto_princ);

        }else{
            $("#gallery tbody").prepend(
            "<tr><td><a target='_blank' href='" + data.result.url +  "'><img id="+ data.result.id_foto +" style='height: 150px;' src='" + data.result.url + "'></a></td>" +
            "<td><p>Nombre: '" + data.result.nombre_foto +  "'</p><p name='fotoPrinc' value="+ data.result.id_foto +">"+ data.result.id_foto +"</p>" +
            "<button class='btn btn-danger btn-sm btn-del btn-del-img imatgeRodal deleteFoto' type='submit' id="+ data.result.id_foto +">Eliminar</button>" +
            "<div class='fotoPrincipal' style='padding-top: 10px;'><p>Foto principal</p>" +
            "<input id=" + data.result.id_foto + " type='radio' class='fotoPrinc' name='fotoPrinc' value='ture' checked='checked' onchange='fotoPrincipal()'></div></td></tr>"
            )
        }
      }else{
        alert(data.result.error_imagen);
      }
    }
  });
});

$(function () {
  /* 1. OPEN THE FILE EXPLORER WINDOW */
  $(".js-upload-docs").click(function () {
    $("#docupload").click();
  });

  /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
  $("#docupload").fileupload({
    dataType: 'json',
    formData: [
        { name: "csrfmiddlewaretoken", value: "{{ csrf_token }}"}
    ],
    done: function (e, data) {  /* 3. PROCESS THE RESPONSE FROM THE SERVER */
      if (data.result.is_valid) {
        $("#library tbody").prepend(
          "<tr><td><a target='_blank' href=" + data.result.url +  "><img id="+ data.result.id_doc +" style='height: 100px;' src=" + fileIconUrl + "></a>" +
          "<p>Nombre: " + data.result.nombre_doc +  "</p>" +
          "<button class='btn btn-danger btn-sm btn-del btn-del-doc documentRodal deleteDoc' type='submit' id=" + data.result.id_doc + ">Eliminar</button></td></tr>"
        )
      }else{
        alert(data.result.error_documento);
      }
    }
  });
});


//$('.deleteFoto').click(function() {
$(document).on('click', '.deleteFoto', function() {
    console.log("delete");
    idFoto = null
    url = '/redbosques/eliminarImagen';
    idFoto = $(this).attr('id');

    url = url + '/' + idFoto + '/';
    $.ajax({
        url: url,
        method: "POST",
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                var csrftoken = getCookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function( data, textStatus, jqXHR ) {
            $("#gallery").load(" #gallery");
        },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
});

//$('.deleteDoc').click(function(){
$(document).on('click', '.deleteDoc', function() {
    url = '/redbosques/eliminarDoc';
    idDoc = $(this).attr('id');
    url = url + '/' + idDoc + '/';
    $.ajax({
        url: url,
        method: "POST",
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                var csrftoken = getCookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function( data, textStatus, jqXHR ) {
            $("#library").load(" #library");
        },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
});



var fotoPrincipal = function(){
    var idRodal = window.location.pathname.split("/")[3];

    url = '/redbosques/mainImage';

    fotoSelected = $( "input:checked" ).attr("id");

    if (fotoSelected == null){
        $("#gallery").load(" #gallery");
    }else{
        url = url + '/' + idRodal + '/' + fotoSelected + '/';
    }

    $.ajax({
        url: url,
        method: "POST",
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                var csrftoken = getCookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function( data, textStatus, jqXHR ) {


        },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
};




/*$(".fotoPrinc").change(function(){

    console.log("hola");


});


var deleteFile = function(){

    url = '/redbosques/eliminarImagen';
    idFoto = $(this).attr('id');
    console.log($(this).attr('id'));
    url = url + '/' + idFoto + '/';
    $.ajax({
        url: url,
        method: "POST",
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                var csrftoken = getCookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function( data, textStatus, jqXHR ) {
            $("#gallery").load(" #gallery");
        },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
};


var deleteDoc = function(){

    url = '/redbosques/eliminarDoc';
    idDoc = $('.btn-del-doc').attr('id');
    url = url + '/' + idDoc + '/';
    $.ajax({
        url: url,
        method: "POST",
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                var csrftoken = getCookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function( data, textStatus, jqXHR ) {
            $("#library").load(" #library");
        },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
};*/





