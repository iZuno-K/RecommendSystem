import random
import re
import pandas as pd
import pathlib
from np_detect import judge_np
LUNCH_LIST = {}
count = 0
recommend_items = {}
# TODO 複数人が接続しても大丈夫なようにする。 return_dictの中に入れて、web側で表示しないけど保持しておく？
# TODO ファイル読み込み LUNCHI_LIST

def make_response_two_ai(json_dict):
    global count, LUNCH_LIST, recommend_items
    count += 1

    l = len(list(json_dict.keys()))
    responses = []
    _classes = []
    if l == 1:
        # global 変数初期化
        LUNCH_LIST = pd.read_csv(pathlib.Path(__file__).parent.joinpath("data/lunch_list.csv"), encoding='shift-jis')
        # count = 0

        responses = ["和食、洋食、中華どれがいい？".format(count)]
        _classes = ['talk_left1']
    elif l == 3:
        human_choice_category = json_dict["#chat_{}".format(len(json_dict) - 1)]
        # カテゴリ判定
        c = find_category(human_choice_category)
        if c is None:
            return [], []
        ai1_item = random.choice(LUNCH_LIST[LUNCH_LIST["category1"] == c]["name"].tolist())
        LUNCH_LIST = LUNCH_LIST[LUNCH_LIST["name"] != ai1_item]  # remove ai1_item from subsequent candidates
        ai2_item = random.choice(LUNCH_LIST[LUNCH_LIST["category1"] == c]["name"].tolist())
        LUNCH_LIST = LUNCH_LIST[LUNCH_LIST["name"] != ai2_item]

        recommend_items["ai1_recommend"] = [ai1_item]
        recommend_items["ai2_recommend"] = [ai2_item]

        ai1_response1 = "{}にしたらどう？".format(ai1_item)
        ai2_response1 = "やっぱ{}でしょ！？".format(ai2_item)
        ai1_response2 = "また{}食べるとママに怒られるよ".format(ai2_item)
        ai2_response2 = "きっとパパも{}食べたいはずだよ".format(ai2_item)

        responses = [ai1_response1, ai2_response1, ai1_response2, ai2_response2]
        _classes = ['talk_left1', 'talk_left2', 'talk_left1', 'talk_left2']
    elif l == 8:
        human_choice_category = json_dict["#chat_{}".format(len(json_dict) - 6)]
        latest_human_response = json_dict["#chat_{}".format(len(json_dict) - 1)]
        # カテゴリ判定
        c = find_category(human_choice_category)
        if c is None:
            return [], []
        positive, accpeted_side = judge_which_is_accepted(latest_human_response)

        if positive and accpeted_side != "both":
            responses, _classes = response_when_accepted_side(accpeted_side, c)
        else:
            # ここで両方否定された場合はai2から喋る
            prev_ai1_item = json_dict["#chat_{}".format(len(json_dict) - 5)][:-8]
            prev_ai2_item = json_dict["#chat_{}".format(len(json_dict) - 4)][3:-5]

            ai2_item = random.choice(LUNCH_LIST[LUNCH_LIST["category1"] == c]["name"].tolist())
            LUNCH_LIST = LUNCH_LIST[LUNCH_LIST["name"] != ai2_item]
            ai1_item = random.choice(LUNCH_LIST[LUNCH_LIST["category1"] == c]["name"].tolist())
            LUNCH_LIST = LUNCH_LIST[LUNCH_LIST["name"] != ai1_item]

            recommend_items["ai1_recommend"].append(ai1_item)
            recommend_items["ai2_recommend"].append(ai2_item)

            ai2_response1 = "{}はやめておこう。{}にしよう！".format(prev_ai2_item, ai2_item)
            ai1_response1 = "じゃあ{}はどう？".format(ai1_item)

            responses = [ai2_response1, ai1_response1]
            _classes = ['talk_left2', 'talk_left1']
    if l == 11:
        human_choice_category = json_dict["#chat_{}".format(len(json_dict) - 9)]
        latest_human_response = json_dict["#chat_{}".format(len(json_dict) - 1)]
        # カテゴリ判定
        c = find_category(human_choice_category)
        if c is None:
            return [], []

        positive, accpeted_side = judge_which_is_accepted(latest_human_response)
        if positive and accpeted_side != "both":
            responses, _classes = response_when_accepted_side(accpeted_side, c)
        else:
            # ここまでで決まらなかったらギブアップ
            ai1_response1 = "力不足でござった..."
            ai2_response1 = "お手上げです..."
            responses = [ai1_response1, ai2_response1]
            _classes = ['talk_left1', 'talk_left2']
    print(recommend_items)
    return responses, _classes


def response_when_accepted(json_dict, category):
    l = len(list(json_dict.keys()))
    if l == 8:
        prev_ai1_item = json_dict["#chat_{}".format(len(json_dict) - 5)][:-7]
        prev_ai2_item = json_dict["#chat_{}".format(len(json_dict) - 4)][3:-5]
    elif l == 11:
        prev_ai1_item = json_dict["#chat_{}".format(len(json_dict) - 2)][3:-4]
        prev_ai2_item = re.findall(r"\w+はやめておこう。(\w+)にしよう！", json_dict["#chat_{}".format(len(json_dict) - 3)])[0]
    else:
        return [], []
    latest_human_response = json_dict["#chat_{}".format(len(json_dict) - 1)]

    if prev_ai1_item in latest_human_response:
        accepted_side1 = "そうだね{}にしよう！".format(prev_ai1_item)
        _classes = ['talk_left1', 'talk_left2', 'talk_left2', 'talk_left1']
    else:
        accepted_side1 = "そうだね{}にしよう！".format(prev_ai2_item)
        _classes = ['talk_left2', 'talk_left1', 'talk_left1', 'talk_left2']

    denied_side1 = "えーっ！じゃ、じゃあ・・・"
    denied_side2 = "{}なんてオススメだよ！".format(random.choice(LUNCH_LIST[LUNCH_LIST["category1"] == category]["name"].tolist()))
    accepted_side2 = "もうええわー！"
    responces = [accepted_side1, denied_side1, denied_side2, accepted_side2]
    return responces, _classes


def find_category(txt):
    c = None
    categories = ["和食", "洋食", "中華", "和", "洋", "中"]
    for cat in categories:
        if cat in txt:
            c = cat
            break
    if c == "和":
        c = "和食"
    elif c == "洋":
        c = "洋食"
    elif c == "中":
        c = "中華"
    return c

def recommend_item_detector(json_dict):
    l = len(json_dict)
    if l == 8:
        prev_ai1_items = [re.findall(r"(\w+)にしたらどう？", json_dict["#chat_{}".format(l - 5)])[0]]
        prev_ai2_items = [re.findall(r"やっぱ(\w+)でしょ！？", json_dict["#chat_{}".format(l - 4)])[0]]
    elif l == 11:
        prev_ai1_items = [re.findall(r"(\w+)にしたらどう？", json_dict["#chat_{}".format(l - 8)])[0]]
        prev_ai2_items = [re.findall(r"やっぱ(\w+)でしょ！？", json_dict["#chat_{}".format(l - 7)])[0]]
        prev_ai1_items.append(re.findall(r"\w+はやめておこう。(\w+)にしよう！", json_dict["#chat_{}".format(len(json_dict) - 3)])[0])
        prev_ai2_items.append(re.findall(r"\w+はやめておこう。(\w+)にしよう！", json_dict["#chat_{}".format(len(json_dict) - 3)])[0])
    else:
        prev_ai1_items = []
        prev_ai2_items = []

    return prev_ai1_items, prev_ai2_items

def judge_which_is_accepted(human_response):
    positive = False
    judged_side = "both"
    ai_lunch = recommend_items
    keys = ["ai1_recommend", "ai2_recommend"]
    for k in keys:
        for l in ai_lunch[k]:
            if (l == human_response) or (human_response in l):
                # 人間のレスポンスが料理名もしくはその省略形だけだった場合、それはその料理名を肯定したことになる
                positive = True
                judged_side = k
                return positive, judged_side
            elif l in human_response:
                positive = judge_np(human_response)
                judged_side = k
                return positive, judged_side
            else:
                positive = judge_np(human_response)
                judged_side = "both"
    return positive, judged_side


def response_when_accepted_side(side, category):
    if side != "both":
        key = side
    accepted_side1 = "そうだね{}にしよう！".format(recommend_items[key][-1])  # 最後に提案したランチ
    if side == "ai1_recommend":
        _classes = ['talk_left1', 'talk_left2', 'talk_left2', 'talk_left1']
    else:
        _classes = ['talk_left2', 'talk_left1', 'talk_left1', 'talk_left2']

    denied_side1 = "えーっ！じゃ、じゃあ・・・"
    denied_side2 = "{}なんてオススメだよ！".format(random.choice(LUNCH_LIST[LUNCH_LIST["category1"] == category]["name"].tolist()))
    accepted_side2 = "もうええわー！"
    responces = [accepted_side1, denied_side1, denied_side2, accepted_side2]
    return responces, _classes
