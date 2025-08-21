from customtkinter import CTk, CTkImage
from PIL import Image
from ui.square import Square
from constants import PLAYERS
from utils.pieces_type_hints import BOARD_TYPE, PIECE_TYPE
from typing import Optional


class App(CTk):

    @staticmethod
    def is_even(n):
        if int(n) % 2 == 0:
            return True
        else:
            return False

    @staticmethod
    def get_square_color(n):
        if App.is_even(n):
            return "black"
        else:
            return "white"

    @staticmethod
    def get_ui_position(row, col):
        return (abs(row - 8), abs(col - 1))

    def __init__(
        self,
        board: BOARD_TYPE,
        is_black_player: bool,
        get_possible_moves,
        move_piece,
        display_board,
    ):

        super().__init__()
        self.center_screen(959, 887)
        self.title("Chess")
        self.board = board
        self.is_black_player = is_black_player
        self.get_possible_moves = get_possible_moves
        self.display_board = display_board
        self.move_piece = move_piece
        self.squares = [[None for _ in range(8)] for _ in range(8)]

        self.build_ui()

    def build_ui(self):

        self.display_board()

        player_turn = PLAYERS[self.is_black_player]

        for row_no, row in self.board.items():

            for col_no, piece in row.items():

                square_color: str = self.get_square_color(row_no + col_no)

                piece: Optional[PIECE_TYPE] = self.board[row_no][col_no]

                square_command = None
                square_state: str = "disabled"
                if piece is not None and piece.player == player_turn:
                    square_state = "normal"
                    square_command = (
                        lambda r=row_no, c=col_no: self.update_possible_moves_ui(r, c)
                    )

                (ui_row, ui_col) = self.get_ui_position(row_no, col_no)
                image_path: Optional[str] = None
                if piece is not None:
                    image_path = f"assets/pieces/{piece.get_image_path()}"

                image_obj = None
                if image_path:
                    image_obj = CTkImage(
                        light_image=Image.open(image_path), size=(60, 106)
                    )

                self.squares[ui_row][ui_col] = Square(
                    master=self,
                    color=square_color,
                    state=square_state,
                    command=square_command,
                    image=image_obj,
                )
                self.squares[ui_row][ui_col].grid(row=ui_row, column=ui_col)

    def update_possible_moves_ui(self, row, col):

        self.disable_all()

        (curr_ui_row, curr_ui_col) = self.get_ui_position(row, col)
        self.squares[curr_ui_row][curr_ui_col].configure(
            state="normal", command=self.update_turn
        )
        moves_list = self.get_possible_moves((row, col))
        print(moves_list)
        for move in moves_list:
            (ui_row, ui_col) = self.get_ui_position(move[0], move[1])
            self.squares[ui_row][ui_col].configure(
                state="normal",
                command=lambda curr_pos=(row, col), move_pos=move: self.update_move(
                    curr_pos, move_pos
                ),
            )

    def update_move(self, curr_pos, move_pos):

        self.move_piece(curr_pos, move_pos)
        self.is_black_player = not self.is_black_player
        self.display_board()
        self.update_turn()

    def update_turn(self):
        player_turn = PLAYERS[self.is_black_player]

        for row_no, row in self.board.items():

            for col_no, piece in row.items():

                piece: Optional[PIECE_TYPE] = self.board[row_no][col_no]
                square_command = None
                square_state: str = "disabled"
                if piece is not None and piece.player == player_turn:
                    square_state = "normal"
                    square_command = (
                        lambda r=row_no, c=col_no: self.update_possible_moves_ui(r, c)
                    )
                image_path: Optional[str] = None
                if piece is not None:
                    image_path = f"assets/pieces/{piece.get_image_path()}"

                image_obj = None
                if image_path:
                    image_obj = CTkImage(
                        light_image=Image.open(image_path), size=(60, 106)
                    )

                (ui_row, ui_col) = self.get_ui_position(row_no, col_no)
                self.squares[ui_row][ui_col].configure(
                    state=square_state,
                    command=square_command,
                    image=image_obj
                )

    def disable_all(self):
        for i in range(8):
            for j in range(8):
                self.squares[i][j].configure(state="disabled")
        # pass

    def center_screen(self, width, height):
        # Set window size
        window_width = width
        window_height = height

        # Get screen size
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate position
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Set window size + position
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
