from customtkinter import CTk, CTkImage
from PIL import Image
from ui.square import Square
from constants import PLAYERS
from utils.pieces_type_hints import BOARD_TYPE, PIECE_TYPE
from utils.custom_type_hints import (
    MOVE_LIST_TYPE,
    POSITION_TYPE,
    UI_POSITION_TYPE,
    PLAYERS_TYPE,
)
from typing import Optional, Callable


class App(CTk):
    """
    TKinter root class which represents the main window
    """

    @staticmethod
    def is_even(n: int) -> bool:
        """
        Static method which checks if a number is even or not


        Parameters
        ----------
        n : int


        Returns
        -------
        bool
            True - even
            False - odd
        """

        if int(n) % 2 == 0:
            return True
        else:
            return False

    @staticmethod
    def get_square_color(n) -> PLAYERS_TYPE:
        """
        Static method which returns square color based on row+column


        Parameters
        ----------
        n : int


        Returns
        -------
        PLAYERS_TYPE
            black - even
            white - odd
        """

        if App.is_even(n):
            return "black"
        else:
            return "white"

    @staticmethod
    def get_ui_position(position: POSITION_TYPE) -> UI_POSITION_TYPE:
        """
        Static method which returns the position tuple of tkinter UI squares


        Parameters
        ----------
        position : POSITION_TYPE
            Tuple of current position of piece ( row_no , column_no )


        Returns
        -------
        Position tuple of tkinter UI squares : UI_POSITION_TYPE


        Example
        -------
        (8,1) -> (0,0)
        """

        return (abs(position[0] - 8), abs(position[1] - 1))

    def __init__(
        self,
        board: BOARD_TYPE,
        is_black_player: bool,
        get_possible_moves: Callable[[POSITION_TYPE], MOVE_LIST_TYPE],
        move_piece: Callable[[POSITION_TYPE, POSITION_TYPE], None],
    ):
        """
        TKinter main window class constructor which initialize the root window


        Attributes
        ----------
        board : BOARD_TYPE
            Data structure of chess board

        is_black_player : bool
            Used by game to swap turns

        get_possible_moves : Callable[[POSITION_TYPE], MOVE_LIST_TYPE]
            Method which returns list of all possible moves of piece at passed position tuple

        move_piece: Callable[[POSITION_TYPE, POSITION_TYPE], None]
            Method which moves a piece at current position to move position

        sqaures : UI_POSITION_TYPE
            8 x 8 table containing Tkinter UI Square Buttons starting from 0 index
        """

        # Call parent constructor
        super().__init__()

        # Set screen size
        self.center_screen(959, 887)

        # Set windows title
        self.title("Chess")

        # Set attributes
        self.board: BOARD_TYPE = board
        self.is_black_player: bool = is_black_player
        self.get_possible_moves: Callable[[POSITION_TYPE], MOVE_LIST_TYPE] = (
            get_possible_moves
        )
        self.move_piece: Callable[[POSITION_TYPE], MOVE_LIST_TYPE] = move_piece
        self.squares: UI_POSITION_TYPE = [[None for _ in range(8)] for _ in range(8)]

        # Build UI
        self.build_ui()

    def build_ui(self):
        """
        Method that builds starting UI
        """

        player_turn: PLAYERS_TYPE = PLAYERS[self.is_black_player]

        for row_no, row in self.board.items():

            for col_no, piece in row.items():

                # Make position tuple
                position: POSITION_TYPE = (row_no, col_no)

                # Set color of square
                square_color: str = self.get_square_color(row_no + col_no)

                # Get piece at position
                piece: Optional[PIECE_TYPE] = self.board[row_no][col_no]

                # Set command and state of square button
                square_command = None
                square_state: str = "disabled"
                if piece is not None and piece.player == player_turn:
                    square_state = "normal"
                    square_command = (
                        lambda position=position: self.update_possible_moves_ui(
                            position
                        )
                    )

                # Set image object of piece
                image_path: Optional[str] = None
                if piece is not None:
                    image_path = f"assets/pieces/{piece.get_image_path()}"

                image_obj = None
                if image_path:
                    image_obj = CTkImage(
                        light_image=Image.open(image_path), size=(60, 106)
                    )

                # Get corresponding position tuple of UI square board
                (ui_row, ui_col) = self.get_ui_position(position)

                # Create UI square button
                self.squares[ui_row][ui_col] = Square(
                    master=self,
                    color=square_color,
                    state=square_state,
                    command=square_command,
                    image=image_obj,
                )

                # Add UI square button to screen
                self.squares[ui_row][ui_col].grid(row=ui_row, column=ui_col)

    def update_possible_moves_ui(self, position: POSITION_TYPE):
        """
        Method which updates UI by enabling UI square buttons where clicked piece can be moved
        Runs after clicking a piece to move


        Parameters
        ----------
        position : POSITION_TYPE
            Tuple of current position of piece ( row_no , column_no )


        Return
        ------
        None
        """

        # Disables all UI square buttons
        self.disable_all()

        # Get position of piece corresponding to UI squares
        (curr_ui_row, curr_ui_col) = self.get_ui_position(position)

        # Configure current position with command to switch piece to move
        self.squares[curr_ui_row][curr_ui_col].configure(
            state="normal", command=self.update_turn
        )

        # Get all possible moves list of piece at current position
        moves_list = self.get_possible_moves(position)

        # Configure move position with command to update move
        for move in moves_list:
            (ui_row, ui_col) = self.get_ui_position(move)
            self.squares[ui_row][ui_col].configure(
                state="normal",
                command=lambda curr_pos=position, move_pos=move: self.update_move(
                    curr_pos, move_pos
                ),
            )

    def update_move(self, curr_pos, move_pos):
        """
        Method which moves a piece from current position to move position and update turn
        Runs after clicking a UI square button for move


        Parameters
        ----------
        current_position : POSITION_TYPE
            Tuple of current position of piece ( row_no , column_no )

        move_position : POSITION_TYPE
            Tuple of move position of piece ( row_no , column_no )


        Return
        ------
        None
        """

        # Move Piece
        self.move_piece(curr_pos, move_pos)

        # Change player turn
        self.is_black_player = not self.is_black_player

        # Update UI for
        self.update_turn()

    def update_turn(self):
        """
        Method which update UI for next move
        Runs on completion of move
        """

        # Get player turn
        player_turn = PLAYERS[self.is_black_player]

        for row_no, row in self.board.items():

            for col_no, piece in row.items():

                # Make position tuple
                position: POSITION_TYPE = (row_no, col_no)

                # Get piece at position
                piece: Optional[PIECE_TYPE] = self.board[row_no][col_no]

                # Set command and state of square buttons
                square_command = None
                square_state: str = "disabled"
                if piece is not None and piece.player == player_turn:
                    square_state = "normal"
                    square_command = (
                        lambda position=position: self.update_possible_moves_ui(
                            position
                        )
                    )

                # Set image object of piece
                image_path: Optional[str] = None
                if piece is not None:
                    image_path = f"assets/pieces/{piece.get_image_path()}"

                image_obj = None
                if image_path:
                    image_obj = CTkImage(
                        light_image=Image.open(image_path), size=(60, 106)
                    )

                # Get corresponding position tuple of UI square board
                (ui_row, ui_col) = self.get_ui_position(position)

                # Configure UI square button
                self.squares[ui_row][ui_col].configure(
                    state=square_state, command=square_command, image=image_obj
                )

    def disable_all(self):
        """
        Method which disables all UI square buttons from clicking
        """

        for i in range(8):
            for j in range(8):
                self.squares[i][j].configure(state="disabled")
        # pass

    def center_screen(self, width, height):
        """
        Method which centers the root window screen
        """

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
