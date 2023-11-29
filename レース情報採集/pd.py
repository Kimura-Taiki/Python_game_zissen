import pandas as pd
from pandas.core.frame import DataFrame
from re import search
from glob import glob
from datetime import datetime
from collections import Counter
from functools import reduce, partial

MAPPING = [r'\d+万', r'未勝利', r'未出走', r'1勝', r'2勝', r'3勝', r'新馬', r'G1', r'G2', r'G3', r'OP', r'\(L\)', r'\(G\)']
DIACHRONIC = ["Nooo!!!", "G1", "G2", "G3", "(G)", "(L)", "OP", "3勝", "2勝", "1勝"]

# 開催日,開催,天気,R,レース名,映像,距離,頭数,馬場,タイム,ペース,勝ち馬,騎手,調教師,2着馬,3着馬

def load_table(path: str) -> DataFrame:
    df = pd.read_csv(path)
    races = df.loc[:, ["開催日", "レース名", "距離"]]
    skin = [terrain[0] for terrain in df.loc[:, "距離"]]
    distance = [terrain[-(len(terrain)-1):] for terrain in df.loc[:, "距離"]]
    rank = [get_class(name) for name in df.loc[:, "レース名"]]
    diachronic_class = [get_diachronic_class(
        name=rank,year=datetime.strptime(date, "%Y/%m/%d").year) for rank, date in zip(rank, df.loc[:, "開催日"])]
    group = [get_group(skin, distance) for skin, distance in zip(skin, distance)]
    races["地肌"], races["距離"], races["クラス"], races["通時"], races["適性"] = skin, distance, rank, diachronic_class, group
    return races

def get_class(name: str) -> str:
    for morphism in MAPPING:
        if match := search(morphism, name):
            return match.group()
    return "NoClass"

def organize_races(year_range: range) -> None:
    for year in year_range:
        pd.concat(
            [load_table(path=path) for path in sorted(glob('競争一覧/{}/races*.csv'.format(year)))],
            ignore_index=True).to_csv("年単位競争一覧/races{}.csv".format(year), index=False)
        print("{}年度の競争の簡易整理が終わりました。".format(year))
    print("全ての年度の競争の簡易整理が終わりました。")

def all_races_integrate() -> None:
    pd.concat(
        [pd.read_csv(filepath_or_buffer=path) for path in sorted(glob('年単位競争一覧/races*.csv'))],
        ignore_index=True).to_csv("簡易整理競争全統合.csv", index=False)
    print("簡易整理の全統合が終わりました。")

def make_database() -> None:
    organize_races(range(1975, 2022+1))
    all_races_integrate()
    df = pd.read_csv(filepath_or_buffer="簡易整理競争全統合.csv")
    df[df["クラス"] == "NoClass"].to_csv("クラス未定義競争一覧.csv", index=False)
    print("クラス未定義競争一覧を作成しました。")

def race_count_table(year: int) -> DataFrame:
    return DataFrame(
        data=list(Counter(pd.read_csv(
            filepath_or_buffer="年単位競争一覧/races{}.csv".format(year)).loc[:, "クラス"]).items()),
        columns=["クラス", str(year)])

def make_class_count_table() -> None:
    func = partial(pd.merge, how="outer", on="クラス")
    tables = [race_count_table(year=year) for year in range(1975, 2022+1)]
    reduce(func, tables).to_csv(path_or_buf="クラス別年間競争一覧.csv", index=False, float_format="%.0f")
    print("クラス別年間競争一覧を作成しました。")


def get_diachronic_class(name: str, year: int=2020) -> str:
    if name[-1] == "万":
        prize = int(name[:-1])
        if (prize > 1000) or (prize > 800 and year < 1984) or (prize > 600 and year < 1978):
            return "7.3勝"
        elif (prize > 500) or (prize >300 and year <1979):
            return "8.2勝"
        else:
            return "9.1勝"
    for i, cond in enumerate(DIACHRONIC):
        if name == cond:
            return "{}.{}".format(i, cond)
    if (name == "未勝利") or (name == "未出走") or (name == "新馬"):
        return "o.未勝利"
    return "z.NoClass"

def get_group(skin: str, distance: str) -> str:
    if skin == "障":
        return "7.障害"
    lgh = int(distance)
    if skin == "芝":
        if lgh < 1600:
            return "1.芝 短距離"
        elif lgh < 1900:
            return "2.芝 マイル"
        else:
            return "3.芝 中以遠"
    elif skin == "ダ":
        if lgh < 1600:
            return "4.砂 短距離"
        elif lgh < 1900:
            return "5.砂 マイル"
        else:
            return "6.砂 中以遠"
    return "z.----"

# print(load_table(path="競争一覧/1975/races001.csv"))
# exit()

make_database()
