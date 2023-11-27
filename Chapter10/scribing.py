from typing import Final
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup, element, Tag
from re import search
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 参考：https://qiita.com/hujuu/items/b0339404b8b0460087f9

URL: Final = "https://db.netkeiba.com/?pid=race_list&word=&track%5B%5D=1&start_year=2014&start_mon=none&end_year=2014&end_mon=none&jyo%5B%5D=01&jyo%5B%5D=02&jyo%5B%5D=03&jyo%5B%5D=04&jyo%5B%5D=05&jyo%5B%5D=06&jyo%5B%5D=07&jyo%5B%5D=08&jyo%5B%5D=09&jyo%5B%5D=10&grade%5B%5D=4&kyori_min=&kyori_max=&sort=date&list=20"
HTML_TAG: Final = "div"
HTML_CLS: Final = "pager"
FILE: Final = "pager.csv"

# URLの指定
html = urlopen(url=URL)
bsObj = BeautifulSoup(html, "html.parser")

# <div> pagerの中身を取得
pager = bsObj.find("div", {"class":"pager"}).get_text().strip()

# 正規表現で数字部分を抽出
match = search(r'\d+', pager)

if match:
    result = match.group()
    print(result)
else:
    print("数字が見つかりませんでした")
    exit()
exit()

# テーブルを指定
table: Tag = bsObj.findAll(HTML_TAG, {"class":HTML_CLS})[0]
# print(len(table), table)
rows: list[Tag] = table.findAll("tr")

with open(FILE, "w", encoding='utf-8') as file:
    writer = csv.writer(file)
    table_text = [table.get_text().strip()]
    writer.writerow(table_text)
    # for row in rows:
    #     csvRow: list[str] = []
    #     cell: Tag
    #     for cell in row.findAll(['td', 'th']):
    #         cell_text = cell.get_text().strip()
    #         csvRow.append(cell_text)
    #     writer.writerow(csvRow)
print('CSVファイルが作成されました。{}'.format(FILE))
