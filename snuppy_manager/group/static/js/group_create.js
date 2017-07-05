(function(){
    'use strict';

    function appendData(data){
        var group_table = document.getElementById('groupTable');
        $(group_table).append(data);
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

    $("#createGroupBtn").submit(function(event) {
        event.preventDefault();
        $('#createGroupMdl').modal('show');
    });


    $("#createGroupSend").submit(function(event) {
        event.preventDefault();
        $.ajaxSetup({
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        });

        var send_data = {
            group_name : document.getElementById('group_name').value
        }

        $.ajax({
              url: "add",
              type: "post",
              data: send_data,
              datatype: 'json',
              success: function(data){
                    if (data.error) {
                        alert(data.error_text);
                    } else {
                        alert('Группа успешно создана!');
                        appendData(data);
                        $('#createGroupMdl').modal('hide');
                    }
              },
              error:function(data){
                  alert('Ошибка создания группы!');
              }
        });
    });
}());