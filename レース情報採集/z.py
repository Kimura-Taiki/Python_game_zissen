from typing import Final, Callable, Any, Type
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup, element, Tag, NavigableString
from re import search
from math import ceil
from pathlib import Path
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from login_info import ACCOUNT_LOGIN_ID, ACCOUNT_PSWD, LOGIN_URL


URL = "https://db.netkeiba.com/race/198206050809/"

AGE_LIMITS = [
    [(r"５歳以上|5歳以上", "4:４歳以上"), (r"４歳以上|4歳以上", "3:３歳以上"), (r"４歳|4歳", "2:３歳"), (r"３歳|3歳", "1:２歳")],
    [(r"４歳以上|4歳以上", "4:４歳以上"), (r"３歳以上|3歳以上", "3:３歳以上"), (r"３歳|3歳", "2:３歳"), (r"２歳|2歳", "1:２歳"),],]
def get_agelimit(smalltxt: str, year: int) -> str:
    limits = AGE_LIMITS[0] if year <= 2000 else AGE_LIMITS[1]
    for pattern, result in limits:
        if search(pattern, smalltxt):
            return result
    return f"0:NoClass {smalltxt}"

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

def find_tag(bsObj: BeautifulSoup, class_name: str, tag: str="div") -> Tag:
    result = bsObj.find(tag, {"class":class_name})
    if isinstance(result, Tag):
        return result
    elif not result:
        TypeError(f"<{tag} class={class_name}>が存在しません。")
    else:
        TypeError(f"<{tag} class={class_name}>は{type(result)}インスタンスです。")

def find_navigable_string(bsObj: BeautifulSoup, class_name: str, tag: str="div") -> NavigableString:
    result = bsObj.find(tag, {"class":class_name})
    if isinstance(result, NavigableString):
        return result
    elif not result:
        TypeError(f"<{tag} class={class_name}>が存在しません。")
    else:
        TypeError(f"<{tag} class={class_name}>は{type(result)}インスタンスです。")

html = urlopen(URL)
bsObj = BeautifulSoup(html, "html.parser")
age_limit = find_tag(bsObj=bsObj, class_name="smalltxt", tag="p").getText().split()[2]
print(age_limit)
# table = find_tag(bsObj=bsObj, class_name="race_table_01", tag="table")
table = find_element(bsObj=bsObj, class_name="race_table_01", tag="table", num=1)
print(bsObj)