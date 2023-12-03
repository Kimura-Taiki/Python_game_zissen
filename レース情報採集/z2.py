import requests
from bs4 import BeautifulSoup, Tag
from typing import Any, Type
from urllib.request import urlopen
from urllib.parse import urljoin

ACCOUNT_LOGIN_ID = 'akari15_5ngo@icloud.com'
ACCOUNT_PSWD = '1kei24ba8'
LOGIN_URL = 'https://regist.netkeiba.com/account/?pid=login'
ARIMA_URL = 'https://db.netkeiba.com/race/198206050809/'


# セッションを開始
session = requests.session()

# ログインが必要な情報
login_info = {
    "login_id":ACCOUNT_LOGIN_ID,
    "pswd":ACCOUNT_PSWD,
    "pid":"login",
    "action":"auth",
    # "return_url2":ARIMA_URL
}

# action
res = session.post(LOGIN_URL, data=login_info)
res.raise_for_status() # エラーならここで例外を発生させる
arima = session.get(ARIMA_URL)
with open('logged_in_page.txt', 'wb') as file:
    file.write(res.content)
with open('arima_page.txt', 'wb') as file:
    file.write(arima.content)
exit("終了！")


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