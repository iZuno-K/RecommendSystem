import random

def make_response_boring1(json_dict):
    response = []
    _class = ['talk_left3']
    lunch_list = ["カレー",
                  "おすし",
                  "からあげ",
                  "ハンバーグ",
                  "ポテトフライ",
                  "ラーメン",
                  "やきにく",
                  "オムライス",
                  "ピザ",
                  "チャーハン",
                  "ほかのもの"]
    l = len(list(json_dict.keys()))
    if l == 1:
        response = ["どれか選んでね！\n" \
                    "1.カレー\n" \
                    "2.おすし\n" \
                    "3.からあげ\n" \
                    "4.ハンバーグ\n" \
                    "5.ポテトフライ\n" \
                    "6.ラーメン\n" \
                    "7.やきにく\n" \
                    "8.オムライス\n" \
                    "9.ピザ\n" \
                    "10.チャーハン\n" \
                    "11.ほかのもの\n" \
                    "(すうじでおしえてね)"]
    elif l == 3:
        latest_human_response = json_dict["#chat_{}".format(len(json_dict) - 1)]
        item = lunch_list[int(latest_human_response) - 1]
        response = ["じゃ、{}にしたら？".format(item)]
    return response, _class


response_candidate = []
prev_item = ""
def make_response_boring2(json_dict):
    global prev_item, response_candidate
    l = len(list(json_dict.keys()))
    response = []
    _class = []
    _class = ['talk_left3']
    if l == 1:
        response = ["好きな食べ物を5つ「、」で区切って教えてね。例えば「カレー、チャーハン」みたいにね。"]
    elif l == 3:
        latest_human_response = json_dict["#chat_{}".format(len(json_dict) - 1)]
        response_candidate = latest_human_response.split('、')
        item = random.choice(response_candidate)
        response_candidate.remove(item)
        response = ["わかりました。\n今日のお昼ご飯は、\n{}にしたら？(はい/いいえ)".format(item)]
        prev_item = item
    elif l >= 5:
        latest_human_response = json_dict["#chat_{}".format(len(json_dict) - 1)]
        if latest_human_response =="はい":
            response = ["じゃあ{}で決まりだね".format(prev_item)]
        else:
            if len(response_candidate) == 0:
                response = ["あとは自分で考えてね！"]
            else:
                item = random.choice(response_candidate)
                response_candidate.remove(item)
                response = ["{}はどう？(はい/いいえ)".format(item)]
    return response, _class
