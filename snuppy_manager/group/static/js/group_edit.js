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

    function collectData(){
        var _group_id_val = $('#group_id').val();
        var _new_user = $('#new_user').val();

        var add_app_data = {
            _group_id_val: _group_id_val,
            _new_user: _new_user,
        }

        return add_app_data;
    }

    $("#inviteUser").submit(function(event) {
        event.preventDefault();

        $.ajaxSetup({
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        });

        var send_data = collectData();
        console.log(send_data);

        $.ajax({
              url: "invite/user",
              type: "post",
              data: send_data,
              datatype: 'json',
              success: function(data){
                    if (data.error) {
                        alert(data.error_text);
                    } else {
                        alert('Приглашение отправлено пользователю!');
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

    $('#changeGroup').submit( function(event) {
        event.preventDefault();
        var send_data = {};
        var tst_str = /([0-9]+|group)/;
        for (var i = 0; i < this.elements.length; i++) {
            send_data[this.elements[i].name] = this.elements[i].value;
        }
        console.log(send_data);

        $.ajaxSetup({
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        });

        $.ajax({
              url: "",
              type: "post",
              data: send_data,
              datatype: 'json',
              success: function(data){
                    if (data.error) {
                        alert(data.error_text);
                    } else {
                        alert('Изменения внесены');
                        location.reload();
                    }
              },
              error:function(data){
                  alert('Ошибка изменения группы!');
              }
        });

    } );

// select name = key for post data, value = value for this key
}());