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

    // parse the possible invitations from localStorage
//    console.log(localStorage["invitations"]);
    if (localStorage["invitations"]){
        var invitations_str = localStorage["invitations"];
//        var invitations_arr = JSON.parse(localStorage["invitations"]);
    }else{var invitations_str = '';};



    function checkInvite(invitations_str){
//        var _group_id_val = $('#group_id_val').val();
//        if (_group_id_val){
        if (invitations_str){
            $('#accept_invite').modal('show');
        };
        console.log(invitations_str);
    };
    checkInvite(invitations_str);


    function collectData(invitations_str){
        var _new_user = $('#new_user').val();
//        var _group_id_val = $('#group_id_val').val();
        // invitations_arr = ["7", "9", .., "last_group_id_val"];
        var add_app_data = {
            _new_user: _new_user,
//            _group_id_val: _group_id_val,
            invitations_str: invitations_str,

        };

        return add_app_data;
    };


    $("#accept_invite_btn").click(function(event) {
        event.preventDefault();
        var send_data = collectData(invitations_str);
        console.log(send_data)

            $.ajaxSetup({
                headers: { "X-CSRFToken": getCookie("csrftoken") }
            });


            $.ajax({
                  url: '/group/invite/accept',
                  type: "post",
                  data: send_data,
                  datatype: 'json',
                  success: function(data){
                        alert('Приглашение принято!');
                        $('#accept_invite').modal('hide');

                  },
                  error: function(){
                      alert('Ошибка! Какая-нибудь...');
                      $('#accept_invite').modal('hide');
                  },
            });


    });


});
