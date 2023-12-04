import requests
from requests import Response
from bs4 import BeautifulSoup, Tag
from typing import Any, Type
from urllib.request import urlopen
from urllib.parse import urljoin
from login_info import ACCOUNT_LOGIN_ID, ACCOUNT_PSWD, LOGIN_URL
from re import search

# 参考:https://qiita.com/syunyo/items/36af8bcb501baf8c7014

ARIMA_URL = 'https://db.netkeiba.com/race/198206050809/'

def enforce_type[X](instance: Any, cond: Type[X]) -> X:
    if isinstance(instance, cond):
        return instance
    else:
        raise TypeError(f"検証インスタンスは{type(instance)}型、要求型は{cond}です。")

def find_element[X](bsObj: BeautifulSoup, tag: str="div", class_name: str="", type: Type[X]=Tag, num: int=0) -> X:
    if num == 0:
        result = bsObj.find(tag, {"class":class_name}) if class_name != "" else bsObj.find(tag)
    else:
        result = bsObj.find_all(tag, {"class":class_name})[num] if class_name != "" else bsObj.find_all(tag)[num]
    return enforce_type(result, type)

# def get_agelimit(smalltxt: str, year: int) -> str:
#     if year <= 2000:
#         if search(r"５歳以上", smalltxt) or search(r"5歳以上", smalltxt):
#             return "4:４歳以上"
#         elif search(r"４歳以上", smalltxt) or search(r"4歳以上", smalltxt):
#             return "3:３歳以上"
#         elif search(r"４歳", smalltxt) or search(r"4歳", smalltxt):
#             return "2:３歳"
#         elif search(r"３歳", smalltxt) or search(r"3歳", smalltxt):
#             return "1:２歳"
#     else:
#         if search(r"４歳以上", smalltxt) or search(r"4歳以上", smalltxt):
#             return "4:４歳以上"
#         elif search(r"３歳以上", smalltxt) or search(r"3歳以上", smalltxt):
#             return "3:３歳以上"
#         elif search(r"３歳", smalltxt) or search(r"3歳", smalltxt):
#             return "2:３歳"
#         elif search(r"２歳", smalltxt) or search(r"2歳", smalltxt):
#             return "1:２歳"
#     return f"0:NoClass {smalltxt}"

AGE_LIMITS = [
    [(r"５歳以上|5歳以上", "4:４歳以上"), (r"４歳以上|4歳以上", "3:３歳以上"), (r"４歳|4歳", "2:３歳"), (r"３歳|3歳", "1:２歳"),],
    [(r"４歳以上|4歳以上", "4:４歳以上"), (r"３歳以上|3歳以上", "3:３歳以上"), (r"３歳|3歳", "2:３歳"), (r"２歳|2歳", "1:２歳"),],]
def get_agelimit(smalltxt: str, year: int) -> str:
    limits = AGE_LIMITS[0] if year <= 2000 else AGE_LIMITS[1]
    for pattern, result in limits:
        if search(pattern, smalltxt):
            return result
    return f"0:NoClass {smalltxt}"

exit(get_agelimit(smalltxt="2歳未勝利", year=2022))

# セッションを開始
session = requests.session()

# ログインが必要な情報
login_info = {
    "login_id":ACCOUNT_LOGIN_ID,
    "pswd":ACCOUNT_PSWD,
    "pid":"login",
    "action":"auth",
}

# BeautifulSoupインスタンスを取得
res = session.post(LOGIN_URL, data=login_info)
res.raise_for_status() # エラーならここで例外を発生させる
arima = session.get(ARIMA_URL)
bsObj = BeautifulSoup(arima.content, "html.parser")

# <table>ブロックを取得
table = find_element(bsObj=bsObj, class_name="race_table_01", tag="table")
tr5 = find_element(bsObj=table, tag="tr", num=5)
td13 = find_element(bsObj=tr5, tag="td", num=13)
prize = float(td13.get_text().strip())*10
print(prize)
smalltxt = find_element(bsObj=bsObj, class_name="smalltxt", tag="p").get_text().strip().split()[2]
exit(get_agelimit(smalltxt, 1982))

# セッションを開始してログイン
with requests.Session() as session:
    login_url = 'https://regist.netkeiba.com/account/?pid=login'  # ログインページのURLに置き換える
    session.post(login_url, data=login_payload)

    # ログイン後のページにアクセス
    target_url = 'https://db.netkeiba.com/race/198206050809/'  # 取得したいページのURLに置き換える
    # response = session.get(target_url)

    # ログイン後のページのHTMLをBeautifulSoupで解析
    # exit(urlopen(target_url))
    bsObj = BeautifulSoup(urlopen(target_url), "html.parser")
    # bsObj = BeautifulSoup(response.text, 'html.parser')
    # bsObj = BeautifulSoup(response.text, 'html.parser')

    # 以降、bsObjを使用してログイン後のページの情報を取得できる
    table = find_element(bsObj=bsObj, class_name="race_table_01", tag="table", num=0)
    print(table)