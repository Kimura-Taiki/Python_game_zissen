from collections import Counter

# 該当集合（例としてリストを使用）
original_set = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]

# 重複のない集合を作成
unique_set = set(original_set)

# 各要素の個数を記録するCounterを作成
element_counts = Counter(original_set)

print("重複のない集合:", unique_set)
print("各要素の個数:", element_counts)
