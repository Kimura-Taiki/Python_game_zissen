モジュール間のデータの受け渡しで直接変数を操作しない方が良いと指摘を頂きました。
すなわち、Conflictクラスならば以下のように依存性の注入用のクラスメソッドを作り、それを用いてmain側では命令を注入するという事でしょうか。

# mod.conflictモジュール
class Conflict():
    # 中略
    def __nie_shoot_down() -> None: raise NotImplementedError("敵機撃墜時の命令が設定されていません")
    def __nie_damaged() -> None: raise NotImplementedError("自機被弾時の命令が設定されていません")
    shoot_down_func: Callable[[], None] = __nie_shoot_down
    damaged_func: Callable[[], None] = __nie_damaged

    @classmethod
    def inject_funcs(inject_shoot_down_func: Callable[[], None], inject_damaged_func: Callable[[], None]) -> None:
        shoot_down_func = inject_shoot_down_func
        damaged_func = inject_damaged_func


# 本体のmainモジュール
x = 0
    # 中略
    Conflict.inject_funcs(inject_shoot_down_func=shot_down_enemy, inject_damaged_func=damaged_func)
