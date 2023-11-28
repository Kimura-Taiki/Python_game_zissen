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

def total_pages(year: int) -> int:
    _tag: Tag | None
    html = urlopen(url=URL(year=year, page=1))
    bsObj = BeautifulSoup(html, "html.parser")
    pager = _tag.get_text().strip() if (_tag := bsObj.find("div", {"class":"pager"})) else exit("<div class=""pager"">が見つかりませんでした。")
    total_races = int(match.group().replace(',', '')) if (match := search(r'\d{1,3}(,\d{3})*', pager)) else exit("数字が見つかりませんでした。")
    return ceil(total_races/20)

def make_year(year: int) -> None:
    for page in range(1, total_pages(year=year)+1):
        html = urlopen(url=URL(year=year, page=page))
        bsObj = BeautifulSoup(html, features="html.parser")
        table: Any = _tag if (_tag := bsObj.find("table", {"class":CLS})) else exit("<table class={}>が見つかりませんでした。".format(CLS))
        make_races(path=PATH(year=year), file=FILE(year=year, page=page), table=table)
    print("{}年度の全ての競争を記録しました。".format(year))

def csvrow_from_tablerow(row: list[Tag]) -> str:
    csvRow: list[str] = []
    cell: Tag
    for cell in row.findAll(['td', 'th']):
        cell_text = cell.get_text().strip()
        csvRow.append(cell_text)
    return csvRow

def make_races(path: str, file_name: str, table: list[Tag]) -> None:
    rows: list[Tag] = table.findAll("tr")
    Path(path).mkdir(parents=True, exist_ok=True)
    with open(file_name, "w", encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(csvrow_from_tablerow(row=row))
    print('{}が作成されました。'.format(file_name))

def main() -> None:
    make_year(year=1976)
    print("全ての競争を記録しました。EoF")


main()
exit()