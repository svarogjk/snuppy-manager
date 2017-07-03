(function(){
    'use strict';

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

    function send_data(){

        var ver_number = document.getElementById('ver_number').value;
        var app_id = document.getElementById('app_id').value;
        var os_type = document.getElementById('os_type').value;

        var data = {
            app_id : app_id,
            os_type : os_type,
            ver_number : ver_number
        };

        $.ajaxSetup({
                headers: { "X-CSRFToken": getCookie("csrftoken") }
            });

        $.ajax({
              url: "",
              type: "post",
              data: data,
              datatype: 'json',
              success: function(data){
                    alert('Приложение добавленно!');
                    location.reload();
              },
              error: function(){
                  alert('Ошибка! Какая-нибудь...');
              },
        });
    }

    $("#add_version").submit(function(event) {
        event.preventDefault();
        $('#add_ver_modal').modal('show');
    });

    $("#add_ver_btn").submit(function(event) {
        event.preventDefault();
        send_data();
    });

    $("#rm-form").submit(function(event) {
        event.preventDefault();
        var app_id = document.getElementById('app_id_rm').value;
        var ver_id = []
        $("input:checkbox[class=ver_id_rm]:checked").each(function(){
            ver_id.push($(this).val());
//            ver_id += $(this).val() + ',';
        });
        if (ver_id.length == ''){
            alert('Ничего не выбранно!')
        } else {
            var is_sure = window.confirm('Уверены, что хотите удалить выбранные?');
            if (is_sure){
                var data = {
                    app_id: app_id,
                    ver_id: JSON.stringify(ver_id)
                }
                send_remove(data);
            }
        }

    });

    function send_remove(data){
        $.ajaxSetup({
                headers: { "X-CSRFToken": getCookie("csrftoken") }
        });

        $.ajax({
            url: "delete",
            type: "post",
            data: data,
            datatype: 'json',
            success: function(data){
                alert('Версия удалена!');
                location.reload();
            },
            error: function(){
              alert('Ошибка! Какая-нибудь...');
            },
        });
    }


}());