$(document).ready(function(){

    $("#link").click(function(event) {
        event.preventDefault();
        $('#add_app').modal('show');
    });


    /* Ищем все submit-кнопки с классом link и заменяем их на ссылки */
    function windowLoad() {
        var buttons = document.getElementsByTagName('button');
        for (var i = 0; i < buttons.length ; i++) {
            if (buttons[i].getAttribute('type') == 'submit' && buttons[i].className == 'link') {
                var link = document.createElement('a');
                link.appendChild(document.createTextNode(buttons[i].firstChild.firstChild.nodeValue));
                link.setAttribute('href', '#');
                addEvent(link, 'click', linkClick);

                var parent = buttons[i].parentNode;
                parent.removeChild(buttons[i]);
                parent.appendChild(link);
            }
        }
    }

});