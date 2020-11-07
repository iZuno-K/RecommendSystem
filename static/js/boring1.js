if (window.addEventListener) {
    window.addEventListener('load', postMessages);
} else if (window.attachEvent) {
    window.attachEvent('onload', postMessages);
} else {
    window.onload = postMessages;
}

function renderChat(text, _class) {
    var tmp = $(`<div class=${_class}/>`);
    var _id = "chat_" + String($('#msgDiv').children().length);
    tmp.append($(`<p id=${_id}/>`).text(text));
    tmp.appendTo($('#msgDiv'));
    $('#msgDiv')[0].scrollTop = $('#msgDiv')[0].scrollHeight;
}

function getTexts() {
    var _dict = {};
    var _txt;
    for (var i = 0; i < $('#msgDiv').children().length; i++) {
        _txt = $("#chat_" + String(i)).text();
        _dict["#chat_" + String(i)] = _txt;
    }
    return _dict;
}

function postMessages() {
    $("#button").click(function () {
        var _txt = $("#input-text").val();
        $("#input-text").val("");
        renderChat(_txt, 'talk_right');
        var textData = JSON.stringify({"talks": getTexts()});
        $.ajax({
            type: 'POST',
            url: '/boring1post',
            data: textData,
            contentType: 'application/json',
            success: function (data) {
                var responses = JSON.parse(data.ResultSet).responses;
                var _classes = JSON.parse(data.ResultSet)._classes;
                for (var i = 0; i < responses.length; i++) {
                    renderChat(responses[i], _classes[i]);
                }
            }
        });
        return false;
    });
}
