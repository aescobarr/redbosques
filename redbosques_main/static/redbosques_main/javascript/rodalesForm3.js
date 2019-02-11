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
          "<button class='btn btn-danger btn-sm btn-del btn-del-img imatgeRodal' type='submit' id="+ data.result.id_foto +" onclick='deleteFile()'>Eliminar</button></td></tr>"
        )
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
          "<button class='btn btn-danger btn-sm btn-del btn-del-doc documentRodal' type='submit' id=" + data.result.id_doc + " onclick='deleteDoc()'>Eliminar</button></td></tr>"
        )
      }else{
        alert(data.result.error_documento);
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
};


/*$("tbody button.btn-del").click(function(){
    var url;
    if($(this).hasClass("btn-del-doc")){
        var urlDoc = '/redbosques/eliminarDoc';
        idDoc = $('.btn-del-doc').attr('id');
        url = urlDoc + '/' + idDoc + '/';
    }else if ($(this).hasClass("btn-del-img")){
        var urlImg = '/redbosques/eliminarImagen';
        idFoto = $('.btn-del-img').attr('id');
        url = urlImg + '/' + idFoto + '/';
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
            $("#gallery").load(" #gallery");
            $("#library").load(" #library");

        },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(errorThrown);
            }
        });
});*/