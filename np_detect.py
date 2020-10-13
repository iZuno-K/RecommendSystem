'''
文章データから、形態素解析して、文字列に対して感情分析を実施する

単語感情極性対応表は、以下のものを使わせていただきました。

参考資料：
高村大也, 乾孝司, 奥村学
"スピンモデルによる単語の感情極性抽出", 情報処理学会論文誌ジャーナル, Vol.47 No.02 pp. 627--637, 2006.
http://www.lr.pi.titech.ac.jp/~takamura/pndic_ja.html
'''

# TODO オススメのランチ単語をファイル読み込みして、それのNPスコアは常に0とする。もしくは、計算しない。

import re
import MeCab
import pandas as pd
import pathlib

# 感情ファイルの辞書を作成する
def read_pn_di():
    dic_pn = {}
    with open('data/pn_ja.txt', 'r') as f:
    # with open('data/pn_ja.txt', 'r', encoding="utf-8_sig") as f:
        lines = f.readlines()  # 1行を文字列として読み込む(改行文字も含まれる)
        for line in lines:
            # フォーマット
            # 見出し語:読み(ひらがな):品詞:感情極性実数値
            columns = line.split(':')
            dic_pn[columns[0]] = float(columns[3])
    return dic_pn


def judge_np(src_txt):
    LUNCH_LIST = pd.read_csv(pathlib.Path(__file__).parent.joinpath("data/lunch_list.csv"), encoding="shift-jis")['name'].tolist()
    # LUNCH_LIST = pd.read_csv(pathlib.Path(__file__).parent.joinpath("data/lunch_list.csv"), encoding="utf-8_sig")['name'].tolist()

    # 単語感情極性対応表データを取得する
    dic_pn = read_pn_di()

    # セパレータを「。」とする。
    seperator = "。"
    mixi_diary_origin = src_txt
    mixi_diary_origin = re.sub("[｜ 　「」\n]", "", mixi_diary_origin)  # | と全角半角スペース、「」と改行の削除

    mixi_diary_list = mixi_diary_origin.split(seperator)  # セパレーターを使って文章をリストに分割する
    mixi_diary_list = [x + seperator for x in mixi_diary_list]  # 文章の最後に。を追加

    # この時点でデータの準備が終わりです
    # ここから形態素分析に入ります
    # t = Tokenizer()
    m = MeCab.Tagger("-Ochasen")
    # m = MeCab.Tagger("-Owakati")


    mixi_diary_words = []  # 形態素分析したあとに出てきた語句を格納するリスト(この例では、名詞、形容詞のみの語句を取っています)

    semantic_value = 0
    semantic_count = 0
    for sentence in mixi_diary_list:

        # tokens = t.tokenize(sentence)
        tokens = m.parse(sentence).split('\n')
        # print([t.split() for t in tokens])
        words = []
        for token in tokens:
            if len(token.split()) > 1:  # remove EOS
                hinshi = token.split()[3].split('-')[0]
                word = token.split()[0]
                _l = [word in lunch for lunch in LUNCH_LIST]
                if (hinshi == '名詞' and sum(_l) > 0):
                    continue  # lunch listのlunchに文字列が含まれてたら計算から除外 ex.)カレー in チキンカレー はNP計算しない
                if hinshi in ['動詞', '名詞', '形容詞', '副詞']:
                    # 感情分析(感情極性実数値より)
                    if (word in dic_pn):
                        data = token + ":" + str(dic_pn[word])
                        semantic_value = dic_pn[word] + semantic_value
                        semantic_count = semantic_count + 1
            words.append(token)

        if len(words) > 0:
            mixi_diary_words.extend(words)

    # data = "分析した単語数:" + str(semantic_count) + " 感情極性実数値合計:" + str(semantic_value) + " 感情極性実数値平均値:" + str(
    #     semantic_value / semantic_count)
    # print(data)
    return semantic_value > 0

if __name__ == '__main__':
    judge = judge_np('パエリアいいね')
