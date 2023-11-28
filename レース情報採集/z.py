import re

race = "農林省賞典中山大障害(OP) "

# 正規表現で"OP"が含まれているか判定
if re.search(r'OP', race):
    print("文字列中に'OP'が含まれています。")
else:
    print("文字列中に'OP'は含まれていません。")

print(re.search(r'OP', race))
