$(document).ready(function(){

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


    function collectData(){
        var _app_id = $('#app_id').val();
//        var _app_name = $('#app_name').val();
//        var _app_description = $('#app_description').val();
//        var _app_source = $('#app_source').val();
//        var _group_id = $('#group_id').val();

        var add_app_data = {
            _app_id: _app_id,
//            _app_name: _app_name,
//            _app_description: _app_description,
//            _app_source: _app_source,
//            _group_id: _group_id,
        }

        return add_app_data;
    }

//    function appendNewData(data, group_id){
//        var tables = document.getElementsByClassName('group_tbl');
//        for (var i=0; i < tables.length; i++){
//            if (tables[i].getAttribute('group-id') == group_id){
//                var app_group = tables[i];
//            }
//        }
//        console.log(app_group);
//        $(app_group).append(data);
//
//    }


    $("#delete_app_btn").click(function(event) {
        event.preventDefault();
        var send_data = collectData();
        console.log(send_data)

            $.ajaxSetup({
                headers: { "X-CSRFToken": getCookie("csrftoken") }
            });

//            $.ajax({
//                  url: "",
//                  type: "post",
//                  data: send_data,
//                  datatype: 'json',
//                  success: function(data){
//                        alert('Приложение изменено!');
//                        window.location.replace('/application/')
//    //                    $('#add_app').modal('hide');
//    //                    appendNewData(data, send_data['_group_id']);
//                  },
//                  error: function(){
//                      alert('Ошибка! Какая-нибудь...');
//                  },
//            });
//

            $.ajax({
                  url: "delete_app",
                  type: "post",
                  data: send_data,
                  datatype: 'json',
                  success: function(data){
                        alert('Приложение удалено!');
                        window.location.replace('/application/')
    //                    $('#add_app').modal('hide');
    //                    appendNewData(data, send_data['_group_id']);
                  },
                  error: function(){
                      alert('Ошибка! Какая-нибудь...');
                  },
            });


    });


});