
行数を増やして構造化するか、行数を減らして軽量化するか、どちらが良いでしょうか。


1️⃣ 行数を減らしてスマートに書く
for i in range(BOARD-1, 0, -1):
    if int(self.car_y+i)%10 <= 4: # 左右の黄色線
        pygame.draw.polygon(surface=self.screen, color=YELLOW,
                            points=[[board_lx[i  ],                   board_by[i  ]], [board_lx[i  ]+BOARD_W[i]*0.02, board_by[i  ]],
                                    [board_lx[i-1]+BOARD_W[i-1]*0.02, board_by[i-1]], [board_lx[i-1],                 board_by[i-1]]])


2️⃣ 行数を増やしてpygame.draw.polygon(points=)の中身を短くする
def trapezoid_points(i: int, lf: Callable[[int], float], rf: Callable[[int], float], bf: Callable[[int], float]) -> tuple[
    tuple[float, float], tuple[float, float], tuple[float, float], tuple[float, float]]:
    return ((lf(i), bf(i)), (rf(i), bf(i)), (rf(i-1), bf(i-1)), (lf(i-1), bf(i-1)))
for i in range(BOARD-1, 0, -1):
    if int(self.car_y+i)%10 <= 4: # 左右の黄色線
        pygame.draw.polygon(surface=self.screen, color=YELLOW, points=trapezoid_points
                            (i=i, lf=lambda i: board_lx[i], rf=lambda i: board_lx[i]+BOARD_W[i]*0.02, bf=lambda i: board_by[i]))
