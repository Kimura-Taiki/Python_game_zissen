# import matplotlib.pyplot as plt
# import japanize_matplotlib

# x = [1, 2, 3, 4, 5]
# y = [1, 4, 9, 16, 25]
# plt.plot(x, y, color='limegreen', linewidth=2, linestyle="solid", marker="o")
# plt.xlabel('X', fontsize=18)
# plt.ylabel('Y', fontsize=18)
# plt.grid()
# plt.annotate('annotation', xy=(3,9), xytext=(1,20), fontsize=15, color="red",
#              arrowprops=dict(color="grey"))
# plt.title('グラフタイトル(Graph)')
# plt.show()

# from pandas_datareader import data
# import pandas as pd
# import matplotlib.pyplot as plt

# start = "2019-11-01"
# end = "2020-11-01"

# df = data.DataReader("^N225", "yahoo", start, end)

# print(df)

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import matplotlib.dates as mdates

start = "2019-11-01"
end = "2020-11-01"

df: pd.DataFrame = yf.download("^N225", start=start, end=end)
# df["index_num"] = df.reset_index().index
# # print(df.head(20)); exit()

x = df.index
y = df["Adj Close"] #終値

#移動平均線追加(５日、２５日)
span05 = 5
span25 = 25
df["sma05"] = y.rolling(window=span05).mean()
df["sma25"] = y.rolling(window=span25).mean()

plt.figure(figsize=(15, 7))
plt.plot(x, y, label="close", color="skyblue", linewidth=3, linestyle="dashed", marker="o")
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel("日付", fontsize=30)
plt.ylabel("Price", fontsize=30)
plt.grid(axis="y")
plt.title("日経平均株価2019-2020", fontsize=35)
plt.annotate("points", xy=(mdates.date2num(x[10]), y[10]),
             xytext=(mdates.date2num(x[10])+10, 24000), fontsize=30,
             color="red", arrowprops=dict(color="black"))
plt.plot(x, df["sma05"], label="sma05", color="limegreen")
plt.plot(x, df["sma25"], label="sma25", color="turquoise")
plt.legend(fontsize=20)
plt.savefig("N225.png")
plt.show()