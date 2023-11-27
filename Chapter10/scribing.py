from typing import Final, Callable, Any
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup, element, Tag
from re import search
from math import ceil
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 参考：https://qiita.com/hujuu/items/b0339404b8b0460087f9

URL: Final = "https://db.netkeiba.com/?pid=race_list&word=&track%5B%5D=1&start_year=2014&start_mon=none&end_year=2014&end_mon=none&jyo%5B%5D=01&jyo%5B%5D=02&jyo%5B%5D=03&jyo%5B%5D=04&jyo%5B%5D=05&jyo%5B%5D=06&jyo%5B%5D=07&jyo%5B%5D=08&jyo%5B%5D=09&jyo%5B%5D=10&grade%5B%5D=4&kyori_min=&kyori_max=&sort=date&list=20"
'''URLの指定'''
CLS: Final = "nk_tb_common race_table_01"
FILE: Final[Callable[[int], str]] = lambda num: "OP一覧/races{}.csv".format(str(num).zfill(3))

_tag: Tag | None

html = urlopen(url=URL)
bsObj = BeautifulSoup(html, "html.parser")
'''BeautifulSoupインスタンス(Tagインスタンスのlist木構造)に変換されたWebページ'''

pager = _tag.get_text().strip() if (_tag := bsObj.find("div", {"class":"pager"})) else exit("<div class=""pager"">が見つかりませんでした。")
'''<div class="pager">ブロックの中身'''

total_races = int(match.group()) if (match := search(r'\d+', pager)) else exit("数字が見つかりませんでした。")
'''正規表現で抽出した総レース数'''

# 抽出すべき総ページ数を算出
total_pages = ceil(total_races/20)
'''繰り返し処理すべき総頁数'''

for page in range(1, total_pages+1):
    bsObj = BeautifulSoup(urlopen(url="{}&page={}".format(URL, page)), features="html.parser")
    table: Any = _tag if (_tag := bsObj.find("table", {"class":CLS})) else exit("<table class={}>が見つかりませんでした。".format(CLS))
    rows: list[Tag] = table.findAll("tr")
    with open(FILE(page), "w", encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in rows:
            csvRow: list[str] = []
            cell: Tag
            for cell in row.findAll(['td', 'th']):
                cell_text = cell.get_text().strip()
                csvRow.append(cell_text)
            writer.writerow(csvRow)
    print('{}が作成されました。'.format(FILE(page)))
print("全ての競争を記録しました。EoF")
