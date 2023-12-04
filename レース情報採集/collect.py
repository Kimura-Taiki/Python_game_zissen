from typing import Final, Callable, Any, Type
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup, element, Tag
from re import search
from math import ceil
from pathlib import Path
from requests import Session
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from login_info import ACCOUNT_LOGIN_ID, ACCOUNT_PSWD, LOGIN_URL

# 参考：https://qiita.com/hujuu/items/b0339404b8b0460087f9

URL: Final[Callable[[int, int], str]] = lambda year, page: "https://db.netkeiba.com/?pid=race_list&word=&start_year={}&start_mon=none&end_year={}&end_mon=none&jyo%5B%5D=01&jyo%5B%5D=02&jyo%5B%5D=03&jyo%5B%5D=04&jyo%5B%5D=05&jyo%5B%5D=06&jyo%5B%5D=07&jyo%5B%5D=08&jyo%5B%5D=09&jyo%5B%5D=10&kyori_min=&kyori_max=&sort=date&list=20&page={}".format(year, year, page)
'''URLの指定'''
CLS: Final = "nk_tb_common race_table_01"
PATH: Final[Callable[[int], str]] = lambda year: "競争一覧/{}".format(year)
FILE: Final[Callable[[int, int], str]] = lambda year, page: "競争一覧/{}/races{}.csv".format(year, str(page).zfill(3))

AGE_LIMITS = [
    [(r"５歳以上|5歳以上", "4:４歳以上"), (r"４歳以上|4歳以上", "3:３歳以上"), (r"４歳|4歳", "2:３歳"), (r"３歳|3歳", "1:２歳")],
    [(r"４歳以上|4歳以上", "4:４歳以上"), (r"３歳以上|3歳以上", "3:３歳以上"), (r"３歳|3歳", "2:３歳"), (r"２歳|2歳", "1:２歳"),],]

def get_agelimit(smalltxt: str, year: int) -> str:
    limits = AGE_LIMITS[0] if year <= 2000 else AGE_LIMITS[1]
    for pattern, result in limits:
        if search(pattern, smalltxt):
            return result
    return f"0:NoClass {smalltxt}"

def first_prize(bsObj: BeautifulSoup) -> float:
    table = find_element(bsObj=bsObj, class_name="race_table_01", tag="table")
    tr5 = find_element(bsObj=table, tag="tr", num=5)
    tdm1 = find_element(bsObj=tr5, tag="td", num=-1)
    return float(tdm1.get_text().strip())*10
    # td13 = find_element(bsObj=tr5, tag="td", num=13)
    # return float(td13.get_text().strip())*10

def enforce_type[X](instance: Any, cond: Type[X]) -> X:
    if isinstance(instance, cond):
        return instance
    else:
        raise TypeError(f"検証インスタンスは{type(instance)}型、要求型は{cond}です。")

def find_element[X](bsObj: BeautifulSoup, tag: str="div", class_name: str="", type: Type[X]=Tag, num: int=0) -> X:
    if num == 0:
        result = bsObj.find(tag, {"class":class_name}) if class_name != "" else bsObj.find(tag)
    else:
        # result = bsObj.find_all(tag, {"class":class_name})[num] if class_name != "" else bsObj.find_all(tag)[num]
        find_list = bsObj.find_all(tag, {"class":class_name}) if class_name != "" else bsObj.find_all(tag)
        find_len = len(find_list)
        result = find_list[(num+find_len) % find_len]
    return enforce_type(result, type)

def total_pages(year: int) -> int:
    _tag: Tag | None
    html = urlopen(url=URL(year=year, page=1))
    bsObj = BeautifulSoup(html, "html.parser")
    pager = _tag.get_text().strip() if (_tag := bsObj.find("div", {"class":"pager"})) else exit("<div class=""pager"">が見つかりませんでした。")
    total_races = int(match.group().replace(',', '')) if (match := search(r'\d{1,3}(,\d{3})*', pager)) else exit("数字が見つかりませんでした。")
    return ceil(total_races/20)

def netkeiba_session() -> Session:
    session = Session()
    login_info = {
        "login_id":ACCOUNT_LOGIN_ID,
        "pswd":ACCOUNT_PSWD,
        "pid":"login",
        "action":"auth",
    }
    res = session.post(LOGIN_URL, data=login_info)
    res.raise_for_status() # エラーならここで例外を発生させる
    return session

def main() -> None:
    # for year in range(1980, 2022+1, 1):
    session = netkeiba_session()
    for year in range(2022, 2022+1, 1):
        make_year(year=year, session=session)
    print("全ての競争を記録しました。EoF")

def make_year(year: int, session: Session, start: int=1) -> None:
    for page in range(start, total_pages(year=year)+1):
        html = urlopen(url=URL(year=year, page=page))
        bsObj = BeautifulSoup(html, features="html.parser")
        table: Any = _tag if (_tag := bsObj.find("table", {"class":CLS})) else exit("<table class={}>が見つかりませんでした。".format(CLS))
        make_races(path=PATH(year=year), file_name=FILE(year=year, page=page), table=table, session=session)
    print("{}年度の全ての競争を記録しました。".format(year))

def make_races(path: str, file_name: str, table: list[Tag], session: Session) -> None:
    rows: list[Tag] = table.findAll("tr")
    Path(path).mkdir(parents=True, exist_ok=True)
    with open(file_name, "w", encoding='utf-8') as file:
        writer = csv.writer(file)
        for i, row in enumerate(rows):
            writer.writerow(csvrow_from_tablerow(row=row, is_th=(i==0), session=session))
    print('{}が作成されました。'.format(file_name))

def csvrow_from_tablerow(row: Tag, is_th: bool, session: Session) -> str:
    csvRow: list[str] = []
    cell: Tag
    for cell in row.findAll(['td', 'th']):
        cell_text = cell.get_text().strip()
        csvRow.append(cell_text)
    if is_th:
        csvRow.append("年齢制限")
        csvRow.append("一着賞金")
    else:
        bsObj = race_bsObj(row=row, session=session)
        formatted_html = bsObj.prettify()
        with open("output.html", "w", encoding="utf-8") as file:
            file.write(formatted_html)
        print("HTML をファイルに保存しました。")
        exit(first_prize(bsObj=bsObj))
        csvRow.append(first_prize(bsObj=bsObj))
        smalltxt = find_element(bsObj=bsObj, class_name="smalltxt", tag="p").get_text().strip().split()[2]
        exit(get_agelimit(smalltxt, 1982))
        exit(bsObj)
    return csvRow

def race_bsObj(row: Tag, session: Session) -> BeautifulSoup:
    race_td = find_element(bsObj=row, tag="td", num=4)
    race_a = find_element(bsObj=race_td, tag="a")
    race_href = race_a.get("href")
    race_response = session.get(url=f"https://db.netkeiba.com{race_href}")
    return BeautifulSoup(race_response.content, "html.parser")


main()
exit()