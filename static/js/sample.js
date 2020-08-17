if (window.addEventListener) {
    window.addEventListener('load', init);
} else if (window.attachEvent) {
    window.attachEvent('onload', init);
} else {
    window.onload = init;
}

function dspChatMsg(text, _class) {
    // $('<div/>').text(text).prepend($('<em/>').text(': ')).appendTo($('#msgDiv'));
    // var modified_txt = `<p ${text}/>`;
    // $(`<div class=${_class}/>`).text(text).appendTo($('#msgDiv'));
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

function init() {
    $("#button").click(function () {
        var _txt = $("#input-text").val();
        dspChatMsg(_txt, 'talk_right');
        var textData = JSON.stringify({"talks": getTexts()});
        $.ajax({
            type: 'POST',
            url: '/postText',
            data: textData,
            contentType: 'application/json',
            success: function (data) {
                // var ai1 = JSON.parse(data.ResultSet).ai1;
                // var ai2 = JSON.parse(data.ResultSet).ai2;
                // dspChatMsg(ai1, 'talk_left1');
                // dspChatMsg(ai2, 'talk_left2');
                var responses = JSON.parse(data.ResultSet).responses;
                var _classes = JSON.parse(data.ResultSet)._classes;
                for (var i = 0; i < responses.length; i++) {
                    dspChatMsg(responses[i], _classes[i]);
                }
            }
        });
        return false;
    });
}
