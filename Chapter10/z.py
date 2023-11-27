for i in range(1, 10+1):
    print(i)
exit()


from typing import Final
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup, element, Tag
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 参考：https://qiita.com/hujuu/items/b0339404b8b0460087f9

URL: Final = "https://db.netkeiba.com/?pid=race_list&word=&track%5B%5D=1&start_year=2022&start_mon=none&end_year=2022&end_mon=none&jyo%5B%5D=01&jyo%5B%5D=02&jyo%5B%5D=03&jyo%5B%5D=04&jyo%5B%5D=05&jyo%5B%5D=06&jyo%5B%5D=07&jyo%5B%5D=08&jyo%5B%5D=09&jyo%5B%5D=10&kyori_min=&kyori_max=1300&sort=date&list=20"
CLS: Final = "nk_tb_common race_table_01"
FILE: Final = "race_data.csv"

# URLの指定
html = urlopen(url=URL)
bsObj = BeautifulSoup(html, "html.parser")

# テーブルを指定
table: Tag = bsObj.findAll("table", {"class":CLS})[0]
rows: list[Tag] = table.findAll("tr")

with open(FILE, "w", encoding='utf-8') as file:
    writer = csv.writer(file)
    for row in rows:
        csvRow: list[str] = []
        cell: Tag
        for cell in row.findAll(['td', 'th']):
            cell_text = cell.get_text().strip()
            csvRow.append(cell_text)
        writer.writerow(csvRow)
print('CSVファイルが作成されました。')
