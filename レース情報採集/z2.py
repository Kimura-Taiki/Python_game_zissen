import requests
from requests import Response
from bs4 import BeautifulSoup, Tag
from typing import Any, Type
from urllib.request import urlopen
from urllib.parse import urljoin
from login_info import ACCOUNT_LOGIN_ID, ACCOUNT_PSWD, LOGIN_URL

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
exit(prize)

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