import random
import re
import pandas as pd
import pathlib
from np_detect import judge_np
LUNCH_LIST = {}
count = 0
# TODO 複数人が接続しても大丈夫なようにする。 return_dictの中に入れて、web側で表示しないけど保持しておく？
# TODO ファイル読み込み LUNCHI_LIST

def make_response_two_ai(json_dict):
    global count, LUNCH_LIST
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
        categories = ["和食", "洋食", "中華"]
        human_choice_category = json_dict["#chat_{}".format(len(json_dict) - 1)]
        # カテゴリ判定
        for cat in categories:
            if cat in human_choice_category:
                c = cat
                break

        ai1_item = random.choice(LUNCH_LIST[LUNCH_LIST["category1"] == c]["name"].tolist())
        LUNCH_LIST = LUNCH_LIST[LUNCH_LIST["name"] != ai1_item]  # remove ai1_item from subsequent candidates
        ai2_item = random.choice(LUNCH_LIST[LUNCH_LIST["category1"] == c]["name"].tolist())
        LUNCH_LIST = LUNCH_LIST[LUNCH_LIST["name"] != ai2_item]

        ai1_response1 = "{}にしたらどう？".format(ai1_item)
        ai2_response1 = "やっぱ{}でしょ！？".format(ai2_item)
        ai1_response2 = "また{}食べるとママに怒られるよ".format(ai2_item)
        ai2_response2 = "きっとパパも{}食べたいはずだよ".format(ai2_item)

        responses = [ai1_response1, ai2_response1, ai1_response2, ai2_response2]
        _classes = ['talk_left1', 'talk_left2', 'talk_left1', 'talk_left2']
    elif l == 8:
        categories = ["和食", "洋食", "中華"]
        human_choice_category = json_dict["#chat_{}".format(len(json_dict) - 6)]
        latest_human_response = json_dict["#chat_{}".format(len(json_dict) - 1)]
        # カテゴリ判定
        for cat in categories:
            if cat in human_choice_category:
                c = cat
                break
        positive = judge_np(latest_human_response)
        if positive:
            responses, _classes = response_when_accepted(json_dict, c)
        else:
            # ここで両方否定された場合はai2から喋る
            prev_ai1_item = json_dict["#chat_{}".format(len(json_dict) - 5)][:-8]
            prev_ai2_item = json_dict["#chat_{}".format(len(json_dict) - 4)][3:-5]

            ai2_item = random.choice(LUNCH_LIST[LUNCH_LIST["category1"] == c]["name"].tolist())
            LUNCH_LIST = LUNCH_LIST[LUNCH_LIST["name"] != ai2_item]
            ai1_item = random.choice(LUNCH_LIST[LUNCH_LIST["category1"] == c]["name"].tolist())
            LUNCH_LIST = LUNCH_LIST[LUNCH_LIST["name"] != ai1_item]

            ai2_response1 = "{}はやめておこう。{}にしよう！".format(prev_ai2_item, ai2_item)
            ai1_response1 = "じゃあ{}はどう？".format(ai1_item)

            responses = [ai2_response1, ai1_response1]
            _classes = ['talk_left2', 'talk_left1']
    if l == 11:
        categories = ["和食", "洋食", "中華"]
        human_choice_category = json_dict["#chat_{}".format(len(json_dict) - 9)]
        latest_human_response = json_dict["#chat_{}".format(len(json_dict) - 4)]
        # カテゴリ判定
        for cat in categories:
            if cat in human_choice_category:
                c = cat
                break
        positive = judge_np(latest_human_response)
        if positive:
            responses, _classes = response_when_accepted(json_dict, c)
        else:
            # ここまでで決まらなかったらギブアップ
            ai1_response1 = "力不足でござった..."
            ai2_response1 = "お手上げです..."
            responses = [ai1_response1, ai2_response1]
            _classes = ['talk_left1', 'talk_left2']

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
