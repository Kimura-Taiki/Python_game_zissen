import pandas as pd

# 開催日,開催,天気,R,レース名,映像,距離,頭数,馬場,タイム,ペース,勝ち馬,騎手,調教師,2着馬,3着馬

# CSVファイルのパス
csv_file_path = "競争一覧/1975/races001.csv"

# CSVファイルを読み込んでDataFrameを作成
df = pd.read_csv(csv_file_path)

# 有効列のみ抽出
races = df.loc[:, ["レース名", "距離"]]



# 地形から地肌を
# skin_and_distance = [[terrain[0], terrain[-(len(terrain)-1):]] for terrain in df.loc[:, "距離"]]
skin = [terrain[0] for terrain in df.loc[:, "距離"]]
distance = [terrain[-(len(terrain)-1):] for terrain in df.loc[:, "距離"]]
rank = [get_rank(name) for name in df.loc[:, "レース名"]]
races["地肌"], races["距離"] = skin, distance


# DataFrameを表示
print(races)
