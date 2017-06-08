$(document).ready(function() {


    $('#add_btn').click(function(event) {
        event.preventDefault();

        // using jQuery
//        function getCookie(name) {
//            var cookieValue = null;
//            if (document.cookie && document.cookie !== '') {
//                var cookies = document.cookie.split(';');
//                for (var i = 0; i < cookies.length; i++) {
//                    var cookie = jQuery.trim(cookies[i]);
//                    // Does this cookie string begin with the name we want?
//                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                        break;
//                    }
//                }
//            }
//            return cookieValue;
//        }
//        var csrftoken = getCookie('csrftoken');


        var csrftoken = $.cookie('csrftoken');

        function csrfSafeMethod(method){
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))
        }

        $.ajaxSetup({
            beforeSend: function(xhr, settings){
                if(!csrfSafeMethod(settings.type) && !this.crossDomain){
                    xhr.setRequestHeader("X-CSRFToken", csrftoken)
                }
            }

        });


        var _app_name = $('#app_name').val();
        var _app_description = $('#app_description').val();
        var _app_source = $('#app_source').val();
        var _group_id = $('#group_id').val();

        var add_app_data = {
            _app_name: _app_name,
            _app_description: _app_description,
            _app_source: _app_source,
            _group_id: _group_id,
//            'csrfmiddleware‌​token': csrftoken,
        }


        $.ajax({
//            url: 'http://127.0.0.1:8000/application/add',
            data: add_app_data,
            type: 'POST',
            // data-type: JSON,
            success: function(resp) {
                if (resp === 'ok') {
                    console.log(resp);
//                    window.location = 'app_success.html';
                }
            },
            error: function(resp) {
                console.log(resp);
            },

        });
    });


});