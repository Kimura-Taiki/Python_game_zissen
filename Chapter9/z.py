# import pickle
# from typing import Optional, BinaryIO

# class MyClass:
#     def __init__(self, value: int) -> None:
#         self.value = value
#         self.reference: Optional['MyClass'] = None

# class AnotherClass(MyClass):
#     hey: str = "ヘレン"

# # オブジェクトの作成
# obj1 = AnotherClass(42)
# obj2 = MyClass(99)

# # 相互に参照を持つ
# obj1.reference = obj2
# obj2.reference = obj1

# # シリアライズ
# with open('data.pkl', 'wb') as f:
#     pickle.dump(obj1, f)

# # デシリアライズ
# with open('data.pkl', 'rb') as f2:  # ここで型を明示的に指定
#     print(type(f2))
#     loaded_obj1: AnotherClass = pickle.load(f2)

# # デシリアライズ
# with open('data.pkl', 'rb') as f3:  # ここで型を明示的に指定
#     print(type(f3))
#     loaded_obj01: AnotherClass = pickle.load(f3)

# obj2.value = 334
# obj1.hey = "ヒャッハー"
# loaded_obj01.hey = "にょわー"

# # 復元されたオブジェクトの確認
# print(loaded_obj1.value)  # 42
# print(type(loaded_obj1))
# if loaded_obj1.reference: print(loaded_obj1.reference.value)  # 99
# print(loaded_obj1.hey)

# # 参照：同名クラスを生成する関数
# from typing import Any
# def make_class(aisatu: str) -> Any:
#     class Cls:
#         def hallo():
#             print(aisatu)
#     return Cls
# c1 = make_class(aisatu="おはよう")
# c2 = make_class(aisatu="Good morning")
# c3 = make_class(aisatu="좋은 아침")

# class Veg():
#     classification = "野菜"
#     nutrition = {"カロリー": "低い", "ビタミン": "高い"}

#     def __init__(self, name) -> None:
#         self.name = name

#     def instructions(self) -> str:
#         return "{}は{}で、{}です".format(self.name, self.classification, "".join("{}が{}、".format(k, v) for k, v in self.nutrition.items()))

# tomato = Veg(name="トマト")
# ninjin = Veg(name="人参")
# print("{}\n{}\n".format(tomato.instructions(), ninjin.instructions()))

class Veg():
    classification = "野菜"
    nutrition = {"カロリー": "低い", "ビタミン": "高い"}

    def __init__(self, name) -> None:
        self.name = name

    def instructions(self) -> str:
        return f"{self.name}は{self.classification}で、{', '.join(f'{k}が{v}' for k, v in self.nutrition.items())}です"

tomato = Veg(name="トマト")
jagaimo = Veg(name="ジャガイモ")
# print(f"{tomato.instructions()}\n{jagaimo.instructions()}\n")
# tomato.classification = "草本性食用植物"
# print(f"{tomato.instructions()}\n{jagaimo.instructions()}\n")
# jagaimo.nutrition["カロリー"] = "普通に主食級"
# print(f"{tomato.instructions()}\n{jagaimo.instructions()}\n")
type(tomato).classification = "チーズ焼きの材料"
print(f"{tomato.instructions()}\n{jagaimo.instructions()}\n")

# print(tomato.classification, ninjin.classification, tomato.nutrition)
# tomato.classification = "草本性食用植物"
# print(tomato.classification, ninjin.classification)
