from mod.racer_game import RacerGame


def main() -> None:
    '''メイン処理'''
    game = RacerGame()
    while True:
        game.mainloop()


if __name__ == '__main__':
    main()
