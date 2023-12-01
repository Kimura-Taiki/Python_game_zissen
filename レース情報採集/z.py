import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv(filepath_or_buffer="通時クラス別年間競争一覧.csv")

x = pd.DataFrame(df.columns)
y = df[(df["通時"] == "o.未勝利") & (df["適性"] == "3.芝 中以遠")].T
t = list(df.columns)
# print(x)
# exit(y)

plt.title("Sales by Product (m$)", fontsize = 22) # (3)タイトル
plt.xlabel("Product", fontsize = 22) # (4)x軸ラベル
plt.ylabel("Sales", fontsize = 22) # (5)y軸ラベル
plt.grid(True) # (6)目盛線表示
plt.tick_params(labelsize=14) # (7)目盛線ラベルサイズ

plt.bar(x, y, tick_label=t,
        align="center", color = "c") # (8)棒グラフ描画
plt.show()

# df_sales=pd.read_csv("electric_appliances_sales.csv")
# print(df_sales)

# plt.title("Sales by Product (m$)", fontsize = 22) # (3)タイトル
# plt.xlabel("Product", fontsize = 22) # (4)x軸ラベル
# plt.ylabel("Sales", fontsize = 22) # (5)y軸ラベル
# plt.grid(True) # (6)目盛線表示
# plt.tick_params(labelsize=14) # (7)目盛線ラベルサイズ

# plt.bar(df_sales["Product"], df_sales["Sales"], tick_label=df_sales["Product"],
#         align="center", color = "c") # (8)棒グラフ描画
# plt.show()
