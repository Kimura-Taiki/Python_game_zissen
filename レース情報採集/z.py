import pandas as pd

# 例としてDataFrameを作成
data = {'Column1': [1, 2, 3], 'Column2': ['A', 'B', 'C']}
df = pd.DataFrame(data)

# DataFrameをCSVファイルとして保存
df.to_csv('output.csv', index=False)
