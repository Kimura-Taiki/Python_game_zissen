import glob

# ファイル一覧を取得
file_list = glob.glob('競争一覧/1975/races*.csv')

# 索引順にソート
file_list_sorted = sorted(file_list)

# ソートされた結果を表示
print(file_list_sorted)
