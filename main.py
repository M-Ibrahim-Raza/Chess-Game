from chess import Chess


def main():
    """
    Main function which start the chess game
    """

    game = Chess()
    # inp = input("Press 1 for Terminal UI and 2 for Tkinter UI\n")

    # if int(inp) == 1:
    #     game.start_game()
    # elif int(inp) == 2:
    game.start_ui_game()


if __name__ == "__main__":
    main()
