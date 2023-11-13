from typing import Callable

class Zenon():
    def _nie(self) -> None:
        raise NotImplementedError

    call: Callable[['Zenon'], None] = _nie

    def __init__(self, text: str) -> None:
        self.text = text

    def call_method(self) -> None:
        self.call()
        print(self.text)

z = Zenon(text="Alpha")
def hey(z: Zenon) -> None:
    print("へーい")
Zenon.call = hey
z.call_method()