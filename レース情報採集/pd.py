import pandas as pd
from pandas.core.frame import DataFrame
from re import search
from glob import glob
from datetime import datetime

# 1.G1, 2.G2, 3.G3, 4.G, 5.L, 6.OP, 7.４勝, 8.３勝, 9.２勝, 10.１勝, 11.未勝利, 12.新馬戦, 13.勝入
# MAPPING = [r'G1', r'G2', r'G3', r'(G)', r'(L)', r'(OP)', r'\d+万', r'勝入', r'未勝利', r'未出走', r'新馬']
# MAPPING = [r'G1', r'G2', r'G3', r'\(G\)', r'\(L\)', r'\(OP\)', r'\d+万', r'勝入', r'未勝利', r'未出走', r'新馬']
MAPPING = [r'\d+万', r'未勝利', r'未出走', r'1勝', r'2勝', r'3勝', r'新馬', r'G1', r'G2', r'G3', r'OP', r'\(L\)', r'\(G\)']

# 開催日,開催,天気,R,レース名,映像,距離,頭数,馬場,タイム,ペース,勝ち馬,騎手,調教師,2着馬,3着馬

def load_table(path: str) -> DataFrame:
    df = pd.read_csv(path)
    races = df.loc[:, ["開催日", "レース名", "距離"]]
    skin = [terrain[0] for terrain in df.loc[:, "距離"]]
    distance = [terrain[-(len(terrain)-1):] for terrain in df.loc[:, "距離"]]
    rank = [get_rank(name) for name in df.loc[:, "レース名"]]
    races["地肌"], races["距離"], races["クラス"] = skin, distance, rank
    return races

def get_rank(name: str) -> str:
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

make_database()