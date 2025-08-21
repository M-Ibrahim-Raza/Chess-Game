from chess import Chess


def main():
    game = Chess()
    
    inp = input("Press 1 for Terminal UI and 2 for Tkinter UI")
    if inp == 1:
        game.start_game()
    elif inp == 2:
        game.start_ui_game()


if __name__ == "__main__":
    main()
