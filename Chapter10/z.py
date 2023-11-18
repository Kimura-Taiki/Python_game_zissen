
BOARD = 120
BOARD_W1 = [0]*BOARD
BOARD_H1 = [0]*BOARD
for i in range(BOARD):
    BOARD_W1[i] = 10+(BOARD-i)*(BOARD-i)/12
    BOARD_H1[i] = 3.4*(BOARD-i)/BOARD
BOARD_W2 = [10 + (BOARD - i) * (BOARD - i) / 12 for i in range(BOARD)]
BOARD_H2 = [3.4 * (BOARD - i) / BOARD for i in range(BOARD)]
print(BOARD_W2[119], BOARD_H2[119])
print(BOARD_W2[0], BOARD_H2[0])

di = 0
board_x = [400 - BOARD_W[i]/2 + (di := di + curve[(car_y+i)%CMAX])/2 for i in range(BOARD)]


def process_input_events(move_forward: Callable[[], None]) -> None:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    key = pygame.key.get_pressed()
    if key[K_UP]:
        move_forward()

def main(): # メイン処理
    # 中略
    car_y = 0
    while True:
        def move_forward() -> None:
            nonlocal car_y, CMAX
            car_y = (car_y+1) % CMAX
        process_input_events(move_forward=move_forward)
        # 後略