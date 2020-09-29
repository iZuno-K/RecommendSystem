//if (window.addEventListener) {
//    window.addEventListener('load', debug);
//} else if (window.attachEvent) {
//    window.attachEvent('onload', debug);
//} else {
//    window.onload = debug;
//}

function renderChat(text, _class, delay) {
    var tmp = $(`<div class=${_class}/>`);
    var _id = "chat_" + String($('#msgDiv').children().length);
    setTimeout(tmp.append($(`<p id=${_id}/>`).text(text)).appendTo($('#msgDiv')), delay);
    $('#msgDiv')[0].scrollTop = $('#msgDiv')[0].scrollHeight;
}

function renderChat2(text, _class, delay) {
    target = document.getElementById("hello")
    target.innerText = target.innerText + text
}

function renderChat3(_text, _class, _delay) {
    $('#hello').text($('#hello').text() + _text);
}


//document.getElementById("button").onclick = function () {
//     setTimeout(renderChat2("fuga-", "talk_left1", 1000), 1000);
//     setTimeout(renderChat2("hoge-", "talk_left1", 3000), 3000);
//}

$('#button').on('click', function() {
    setTimeout(function() {renderChat3("hoge", "talk_left", 1000)}, 1000);
    setTimeout(function() {renderChat3("fuga", "talk_left", 3000)}, 3000);
})