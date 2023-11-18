from math import sin, radians

BOARD = 120
WX = 800
BOARD_W = [10+(BOARD-i)**2/12 for i in range(BOARD)]
BOARD_H = [3.4*(BOARD-i)/BOARD for i in range(BOARD)]
curve = [5*sin(radians(i-120)) if i > 120 else 0 for i in range(480)]

di: float = 400.0
# board_by = [0.0]*(BOARD)+[400.0]
board_by: list[float] = [(di := di+3.4*i/BOARD) for i in range(BOARD)][::-1]
di: float = 0.0
board_lx: list[float] = [WX/2-BOARD_W[i]/2+(di := di+curve[(i) % 480])/2 for i in range(BOARD)]
# board_lx: list[float] = [WX/2+(di := di+curve[(i) % 480])/2 for i in range(BOARD)]
di: float = 0.0
board_rx: list[float] = [WX/2+BOARD_W[i]/2+(di := di+curve[(i) % 480])/2 for i in range(BOARD)]

for i in range(12):
    print(int(BOARD_W[i*10]), int(BOARD_H[i*10]*100)/100, int(curve[i*10]*100)/100, int(board_lx[i*10]), int(board_rx[i*10]), int(board_by[i*10]))