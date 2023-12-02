import matplotlib.pyplot as plt

# 参考:   https://qiita.com/skotaro/items/08dc0b8c5704c94eafb9#fn1

# サブプロットを2つ作成
fig, axes = plt.subplots(2, 1)

# axesはnumpy.ndarrayで、各要素がAxesのインスタンス
ax1 = axes[0]
ax2 = axes[1]

# 各Axesに対してプロットを追加
ax1.plot([0, 1, 2], [0, 1, 0], label='Plot 1')
ax2.scatter([0, 1, 2], [0, -1, 0], label='Plot 2')

# 各Axesに対して独自の設定を行うことができる
ax1.set_title('Subplot 1')
ax2.set_title('Subplot 2')

# グラフが重ならないように調整
plt.tight_layout()

# 凡例を表示
plt.legend()

# プロットを表示
plt.show()
