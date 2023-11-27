from typing import Final, Callable, Any
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup, element, Tag
from re import search
from math import ceil
from pathlib import Path
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 参考：https://qiita.com/hujuu/items/b0339404b8b0460087f9
URL: Final[Callable[[int, int], str]] = lambda year, page: "https://db.netkeiba.com/?pid=race_list&word=&start_year={}&start_mon=none&end_year={}&end_mon=none&jyo%5B%5D=01&jyo%5B%5D=02&jyo%5B%5D=03&jyo%5B%5D=04&jyo%5B%5D=05&jyo%5B%5D=06&jyo%5B%5D=07&jyo%5B%5D=08&jyo%5B%5D=09&jyo%5B%5D=10&kyori_min=&kyori_max=&sort=date&list=20&page={}".format(year, year, page)
'''URLの指定'''
CLS: Final = "nk_tb_common race_table_01"
PATH: Final[Callable[[int], str]] = lambda year: "競争一覧/{}".format(year)
FILE: Final[Callable[[int, int], str]] = lambda year, page: "競争一覧/{}/races{}.csv".format(year, str(page).zfill(3))

_tag: Tag | None

html = urlopen(url=URL(year=1975, page=1))
bsObj = BeautifulSoup(html, "html.parser")
'''BeautifulSoupインスタンス(Tagインスタンスのlist木構造)に変換されたWebページ'''

pager = _tag.get_text().strip() if (_tag := bsObj.find("div", {"class":"pager"})) else exit("<div class=""pager"">が見つかりませんでした。")
'''<div class="pager">ブロックの中身'''

total_races = int(match.group().replace(',', '')) if (match := search(r'\d{1,3}(,\d{3})*', pager)) else exit("数字が見つかりませんでした。")
'''正規表現で抽出した総レース数'''

# 抽出すべき総ページ数を算出
total_pages = ceil(total_races/20)
'''繰り返し処理すべき総頁数'''

for page in range(1, total_pages+1):
    html = urlopen(url=URL(year=1975, page=page))
    bsObj = BeautifulSoup(html, features="html.parser")
    table: Any = _tag if (_tag := bsObj.find("table", {"class":CLS})) else exit("<table class={}>が見つかりませんでした。".format(CLS))
    rows: list[Tag] = table.findAll("tr")
    Path(PATH(year=1975)).mkdir(parents=True, exist_ok=True)
    with open(FILE(year=1975, page=page), "w", encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in rows:
            csvRow: list[str] = []
            cell: Tag
            for cell in row.findAll(['td', 'th']):
                cell_text = cell.get_text().strip()
                csvRow.append(cell_text)
            writer.writerow(csvRow)
    print('{}が作成されました。'.format(FILE(year=1975, page=page)))
print("全ての競争を記録しました。EoF")

exit()

# ディレクトリのパス
directory_path = '/path/to/directory'

# ディレクトリを作成
Path(directory_path).mkdir(parents=True, exist_ok=True)

