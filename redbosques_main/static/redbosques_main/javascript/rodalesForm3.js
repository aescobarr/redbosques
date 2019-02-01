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
        $("#gallery tbody").prepend(
          "<tr><td><a target='_blank' href='" + data.result.url +  "'><img id="+ data.result.id_foto +" style='height: 150px;' src='" + data.result.url + "'></a></td>" +
          "<td><p>Nombre: '" + data.result.nombre_foto +  "'</p>" +

          "<button class='btn btn-danger btn-sm btn-del-img' type='submit' id="+ data.result.id_foto +" onclick='deleteFile()'>Eliminar</button></td></tr>"
        )
      }else{
        alert(data.result.error_imagen);
      }
    }
  });
});

var deleteFile = function(){

    url = '/redbosques/eliminarImagen';
    idFoto = $('.btn-del-img').attr('id');
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