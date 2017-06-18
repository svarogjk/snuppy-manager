(function(){
    'use strict';
    function GetURLParameter(sParam) {
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++){
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam){
            return sParameterName[1];
            }
        }
    }

    function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

    $("#inviteUser").submit(function(event) {
        event.preventDefault();

        $.ajaxSetup({
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        });

        var send_data = {
            group_id : GetURLParameter('group_id'),
            new_user : document.getElementById('new_user').value
        }

        $.ajax({
              url: "invite/user",
              type: "post",
              data: send_data,
              datatype: 'json',
              success: function(data){
                    if (data.error) {
                        alert(data.error_text);
                    } else {
                        alert('Приглашение отправленно пользователю!');
                    }
                    document.getElementById('new_user').value = '';
              },
              error:function(data){
                  console.log(data)
                  alert('Ошибка добавления пользователя!');
              }
        });
    });

    $("#deleteGroup").submit(function(event) {

        $.ajaxSetup({
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        });

        var send_data = {
            group_id : GetURLParameter('group_id')
        }

        $.ajax({
              url: "delete",
              type: "post",
              data: send_data,
              datatype: 'json',
              success: function(data){
                    if (data.error) {
                        alert(data.error_text);
                    } else {
                        alert('Группа успешно удалена!');
                    }
              },
              error:function(data){
                  alert('Ошибка удаления группы!');
              }
        });

        return true
    });
}());