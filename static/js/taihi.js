if (window.addEventListener) {
    window.addEventListener('load', postMessages);
} else if (window.attachEvent) {
    window.attachEvent('onload', postMessages);
} else {
    window.onload = postMessages;
}

function wrapper(texts, _classes, i) {
    if (texts.length > i) {
        renderChat(texts[i], _classes[i]);
        setTimeout(wrapper(texts, _classes, i+1), (i+1)*3000);
    }

}

function renderChat(text, _class) {
    var tmp = $(`<div class=${_class}/>`);
    var _id = "chat_" + String($('#msgDiv').children().length);
    tmp.append($(`<p id=${_id}/>`).text(text)).delay;
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
    $("#button").click(function() {
        var hoge;
        mypost().done(function(result) {
            draw(result);
        }).fail(function(result) {
            hoge = result;
        });
        return false;
    });
}

function mypost() {
    var _txt = $("#input-text").val();
    renderChat(_txt, 'talk_right');
    var textData = JSON.stringify({"talks": getTexts()});
    return $.ajax({
        type: 'POST',
        url: '/postText',
        data: textData,
        contentType: 'application/json'
    });
}

function draw(data) {
    var timerId = 0;
    var responses = JSON.parse(data.ResultSet).responses;
    var _classes = JSON.parse(data.ResultSet)._classes;
//                for (var i = 0; i < responses.length; i++) {
//                    setTimeout(renderChat(responses[i], _classes[i]), 3000);
//                }
    wrapper(responses, _classes, 0);
}