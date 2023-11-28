import pandas as pd
from pandas.core.frame import DataFrame
from re import search
from glob import glob

# 1.G1, 2.G2, 3.G3, 4.G, 5.L, 6.OP, 7.４勝, 8.３勝, 9.２勝, 10.１勝, 11.未勝利, 12.新馬戦, 13.勝入
MAPPING = [r'G1', r'G2', r'G3', r'(G)', r'(L)', r'(OP)', r'\d+万下', r'勝入', r'未勝利', r'新馬']

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
    return ""

pd.concat([load_table(path=path) for path in sorted(glob('競争一覧/1975/races*.csv'))], ignore_index=True).to_csv("年単位競争一覧/races1975.csv", index=False)
