import re

names = ["クリスマスハンデキャ(800万下)", "4歳以上500万下", "3歳200万下"]

pattern = re.compile(r'\d+万下')

for name in names:
    match = pattern.search(name)
    if match:
        result = match.group()
        print(result)
    else:
        print("マッチなし")
