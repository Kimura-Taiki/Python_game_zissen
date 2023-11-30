import pandas as pd

# # ダミーのデータを作成 (実際にはCSVから読み込んでください)
# data = {
#     "通時": [1, 2, 3, 4, 5],
#     "適性": [6, 7, 8, 9, 10]
# }

# df = pd.DataFrame(data)

# # "通時" 列と "適性" 列を結合した新しい列を追加
# df["結合列"] = df.apply(lambda row: (row["通時"], row["適性"]), axis=1)

# # 結果を表示
# print(df)
# exit()

# from collections import Counter

# # 該当集合（例としてリストを使用）
# original_set = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]

# # 重複のない集合を作成
# unique_set = set(original_set)

# # 各要素の個数を記録するCounterを作成
# element_counts = Counter(original_set)

# print("重複のない集合:", unique_set)
# print("各要素の個数:", element_counts)


import pandas as pd
from pandas.core.frame import DataFrame
# df = pd.read_csv(filepath_or_buffer="年単位競争一覧/races1975.csv")
# frequency_distribution = df[["通時", "適性"]].value_counts().reset_index(name="1975")
# print(frequency_distribution)
# frequency_distribution.to_csv(path_or_buf="test3.csv", index=True, float_format="%.0f")


fd1975 = pd.read_csv(filepath_or_buffer="年単位競争一覧/races1975.csv")[["通時", "適性"]].value_counts().reset_index(name="1975")
fd1976 = pd.read_csv(filepath_or_buffer="年単位競争一覧/races1976.csv")[["通時", "適性"]].value_counts().reset_index(name="1976")
pd.merge(fd1975, fd1976, how="outer", on=["通時", "適性"]).to_csv(path_or_buf="test4.csv", index=True, float_format="%.0f")