# import csv
# from urllib.request import urlopen
# from bs4 import BeautifulSoup
# import ssl
# ssl._create_default_https_context = ssl._create_unverified_context

# # URLの指定
# html = urlopen("https://db.netkeiba.com/horse/sire/2009105084/")
# bsObj = BeautifulSoup(html, "html.parser")

# # テーブルを指定
# table = bsObj.findAll("table", {"summary":"産駒成績"})[0]
# rows = table.findAll("tr")

# with open("ebooks.csv", "w", encoding='utf-8') as file:
#     writer = csv.writer(file)
#     for row in rows:
#         csvRow = []
#         for cell in row.findAll(['td', 'th']):
#             csvRow.append(cell.get_text())
#         writer.writerow(csvRow)


import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# URLの指定
html = urlopen("https://db.netkeiba.com/horse/sire/2009105084/")
bsObj = BeautifulSoup(html, "html.parser")

# テーブルを指定
table = bsObj.find("table", {"summary": "産駒成績"})
rows = table.findAll("tr")

# ヘッダーの取得
header_row = rows[0]
headers = [th.text.strip() for th in header_row.find_all(["th", "td"])]

# 年度と出走頭数の列のインデックスを取得
year_index = headers.index("年度")
starts_index = headers.index("出走頭数")

# 年度と出走頭数のデータを取得
data = []
for row in rows[1:]:
    columns = row.find_all(["th", "td"])
    year = columns[year_index].text.strip()
    starts = columns[starts_index].text.strip()
    data.append({"年度": year, "出走頭数": starts})

# 結果を表示
for entry in data:
    print(entry)
