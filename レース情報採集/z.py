from typing import Final, Callable, Any, Type
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup, element, Tag, NavigableString
from re import search
from math import ceil
from pathlib import Path
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

URL = "https://db.netkeiba.com/race/198206050809/"

def enforce_type[X](instance: Any, cond: Type[X]) -> X:
    if isinstance(instance, cond):
        return instance
    else:
        raise TypeError(f"検証インスタンスは{type(instance)}型、要求型は{cond}です。")


# def 新規関数[X](instance: Any, cond: Type[X]) -> X:
#     if isinstance(instance, cond):
#         return instance
#     elif not result:
#         TypeError(f"<{tag} class={class_name}>が存在しません。")
#     else:
#         TypeError(f"<{tag} class={class_name}>は{type(result)}インスタンスです。")

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