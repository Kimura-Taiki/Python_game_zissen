from typing import Type, Any

# 参考:   https://docs.python.org/ja/3/library/typing.html#building-generic-types-and-type-aliases

def 新規関数[X](instance: Any, cond: Type[X]) -> X:
    if isinstance(instance, cond):
        return instance
    else:
        raise TypeError(f"検証インスタンスは{type(instance)}型、要求型は{cond}です。")

a = 100
b = func(a, int)
c = func(a, str)
print(b, c)
exit()


def example_function[X](class_type: Type[X]) -> X:
    print()
    return class_type()

class Hoge():
    def __init__(self) -> None:
        self.x = 11
        self.y = 22

    def coord(self) -> str:
        return f'({self.x},{self.y})'

h = example_function(Hoge)
print(h.coord())

# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# import japanize_matplotlib
# from matplotlib.axes import Axes

# df = pd.read_csv(filepath_or_buffer="通時クラス別年間競争一覧.csv")

# filtered_df = df[(df["通時"] == "o.未勝利") & ((df["適性"] == "1.芝 短距離") | (df["適性"] == "2.芝 マイル") | (df["適性"] == "3.芝 中以遠"))]

# x = df.columns[2:]
# x = [int(i) for i in list(x)]
# y1 = filtered_df[filtered_df["適性"] == "1.芝 短距離"].values.flatten()[2:]
# y2 = filtered_df[filtered_df["適性"] == "2.芝 マイル"].values.flatten()[2:]
# y3 = filtered_df[filtered_df["適性"] == "3.芝 中以遠"].values.flatten()[2:]
# labels = ["短距離", "マイル", "中以遠"]
# print(x, y1, y2, y3)

# ax: Axes
# fig, ax = plt.subplots()
# ax.stackplot(x, [list(y1), list(y2), list(y3)], labels=labels)
# ax.legend(loc="upper left")
# plt.show()


# exit([len(y1), len(y2), len(y3), [int(i) for i in list(x)]])

# # Plot the data
# # plt.plot(x, y1, label="(o.未勝利,1.芝 短距離)")
# # plt.plot(x, y2, label="(o.未勝利,2.芝 マイル)")
# # plt.plot(x, y3, label="(o.未勝利,3.芝 中以遠)")

# # Set plot labels and title
# plt.title("Performance Over the Years")
# plt.xlabel("Year")
# plt.ylabel("Performance")
# plt.legend()  # Show legend

# # plt.bar(x, y3, tick_label=x, align="center", color = "c") # (8)棒グラフ描画
# # plt.bar(x, y2, bottom=y3, tick_label=x, align="center", color = "b") # (8)棒グラフ描画
# # plt.bar(x, y1, bottom=y3+y2, tick_label=x, align="center", color = "y") # (8)棒グラフ描画
# plt.stackplot(
#   x,
#   y3,
#   y2,
#   y1,)


# # Show the plot
# plt.show()
