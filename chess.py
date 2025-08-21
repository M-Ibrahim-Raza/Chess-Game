import os
from utils.custom_exceptions import InvalidInput, InvalidMove, InvalidPosition
from typing import Optional
from utils.custom_type_hints import POSITION_TYPE, MOVE_LIST_TYPE, PLAYERS_TYPE
from constants import NUM_ROW, NUM_COL, ALPHABET_COL, PLAYERS
from pieces.piece import Piece
from utils.pieces_type_hints import PIECE_TYPE, BOARD_TYPE
from pieces.pawn import Pawn
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.queen import Queen
from pieces.king import King
import customtkinter as ctk
from ui.app import App
import math


class Chess:
    """
    Class representing chess game


    Class Attributes
    ----------------

    CHESS_ALPHABET_MAPPING : dict
        Used to parse alphabatic position string input to valid position tuples
    """

    CHESS_ALPHABET_MAPPING = {
        "a": 1,
        "b": 2,
        "c": 3,
        "d": 4,
        "e": 5,
        "f": 6,
        "g": 7,
        "h": 8,
    }

    @staticmethod
    def is_valid_input(entered_input: str) -> bool:
        """
        Static method used to check if input is valid or not


        Parameters
        ----------
        entered_input : str
            e.g. a1 -> a = 1st col , 1 = 1st row


        Return
        ------
        bool
            True - If input valid
            False - If input Invalid
        """

        if type(entered_input) is not str:
            return False
        if len(entered_input) != 2:
            return False
        if type(entered_input[0]) is str and entered_input[0] not in ALPHABET_COL:
            return False
        if entered_input[1].isdigit() and int(entered_input[1]) not in NUM_ROW:
            return False
        return True

    @staticmethod
    def is_valid_position(position: POSITION_TYPE):
        """
        Static method used to check if position tuple is valid or not


        Parameters
        ----------
        position : POSITION_TYPE
            Tuple of position ( row_no , column_no )


        Return
        ------
        bool
            True - If position valid
            False - If position Invalid
        """

        if position[0] in NUM_ROW and position[1] in NUM_COL:
            return True
        else:
            return False

    @staticmethod
    def print_heading(heading: str) -> None:
        """
        Static method used to print heading at center


        Parameters
        ----------
        position : POSITION_TYPE
            Tuple of position ( row_no , column_no )


        Return
        ------
        None
        """

        length: int = len(heading)
        gap: int = 60 - length
        left_gap: int = math.floor(gap / 2)
        right_gap: int = math.ceil(gap / 2)
        print(f"{' '*left_gap}{heading}{' '*right_gap}")

    @staticmethod
    def print_piece(piece: Optional[PIECE_TYPE]) -> None:
        """
        Static method used to print piece symbol


        Parameters
        ----------
        piece : Optional[PIECE_TYPE]
            Child object of Piece class


        Return
        ------
        None
        """

        if piece is None:
            print("      ", end="")
        else:
            if type(piece) is str:
                length: int = len(piece)
            else:
                length: int = 1
            gap: int = 6 - length
            left_gap: int = math.floor(gap / 2)
            right_gap: int = math.ceil(gap / 2)
            print((f"{' '*left_gap}{piece}{' '*right_gap}"), end="")
        print(end="|")

    @staticmethod
    def get_alphabet(num: int):
        """
        Static method which returns corresponding alphabet of column number


        Parameters
        ----------
        num : int
            Column number


        Return
        ------
        Corresponding alphabet or False if invalid
        """

        for k, v in Chess.CHESS_ALPHABET_MAPPING.items():
            if v == num:
                return k
        return False

    @staticmethod
    def get_position_str(position: POSITION_TYPE):
        """
        Static method which returns alphabetic position string of position tuple


        Parameters
        ----------
        position : POSITION_TYPE
            Tuple of position ( row_no , column_no )


        Return
        ------
        Corresponding alphabetic string


        Example
        -------
        (1,1) -> a1
        """

        return f"{Chess.get_alphabet(position[1])+str(position[0])}"

    @staticmethod
    def get_tuple_position(position_str: str) -> POSITION_TYPE:
        """
        Static method which returns position tuple of alphabetic position string


        Parameters
        ----------
        position_str : str
            Alphabetic position string


        Return
        ------
        position : POSITION_TYPE
            Corresponding Tuple of position ( row_no , column_no )


        Example
        -------
        a1 -> (1,1)
        """

        return (int(position_str[1]), Chess.CHESS_ALPHABET_MAPPING[position_str[0]])

    def __init__(self):
        """
        Chess class constructor which initialize chess object


        Attributes
        ----------
        board : BOARD_TYPE
            Board data structure of chess
        """

        self.board = self.init_board()
        self.place_pieces()

    def is_piece(self, position: POSITION_TYPE) -> bool:
        """
        Instance method that takes position tuple and checks if there is any piece at that position


        Parameters
        ----------
        position : POSITION_TYPE
            Tuple of position ( row_no , column_no )


        Return
        ------
        bool
            True - If there is any piece at specified position
            False - If there is not any piece at specified position
        """

        position_value: Optional[PIECE_TYPE] = self.board[position[0]][position[1]]

        if position_value is None:
            return False
        elif isinstance(position_value, Piece):
            return True
        else:
            return False

    def is_player_piece(self, player: PLAYERS_TYPE, position: POSITION_TYPE) -> bool:
        """
        Instance method that takes position tuple and checks if there is player's piece at that position


        Parameters
        ----------
        position : POSITION_TYPE
            Tuple of position ( row_no , column_no )


        Return
        ------
        bool
            True - If there is any player's own piece at specified position
            False - If there is not any player's own piece at specified position
        """

        position_value: Optional[PIECE_TYPE] = self.board[position[0]][position[1]]

        if position_value is None:
            return False
        elif position_value.player == player:
            return True
        else:
            return False

    def print_piece_moves(
        self,
        position: POSITION_TYPE,
        possible_moves_list: MOVE_LIST_TYPE,
    ) -> None:
        """
        Instance method which prints all possible moves of a piece at current position


        Parameters
        ----------
        position : POSITION_TYPE
            Tuple of current position of piece ( row_no , column_no )

        possible_moves_list: MOVE_LIST_TYPE
            List of tuples of all possible move position


        Return
        ------
        None
        """

        piece = self.board[position[0]][position[1]]
        possible_moves_str = ""
        for pos in possible_moves_list:
            possible_moves_str += " | " + Chess.get_position_str(position=pos)
        print()
        if possible_moves_str == "":
            Chess.print_heading(
                f"{piece} ({Chess.get_position_str(position)}) Can Not Move. Please Change Piece"
            )
        else:
            Chess.print_heading(
                f"{piece} ({Chess.get_position_str(position)}) Can Move To {possible_moves_str} |"
            )

    def get_piece_movement_str(
        self, current_position: POSITION_TYPE, move_position: POSITION_TYPE
    ) -> str:
        """
        Instance method which return string of movement of piece at current position to move position


        Parameters
        ----------
        current_position : POSITION_TYPE
            Tuple of current position of piece ( row_no , column_no )

        move_position : POSITION_TYPE
            Tuple of move position of piece ( row_no , column_no )


        Return
        ------
        str
            String of movement of piece from current position to move position
        """

        piece = self.board[move_position[0]][move_position[1]]
        return f"{piece} has Moved from {Chess.get_position_str(current_position)} To {Chess.get_position_str(move_position)}"

    def get_possible_moves(self, position: POSITION_TYPE) -> MOVE_LIST_TYPE:
        """
        Instance method which returns list of all possible moves of piece at passed position tuple


        Parameters
        ----------
        position : POSITION_TYPE
            Tuple of position of piece ( row_no , column_no )


        Return
        ------
        possible_moves_list: MOVE_LIST_TYPE
            List of tuples of all possible move position
        """

        piece: PIECE_TYPE = self.board[position[0]][position[1]]
        get_possible_moves = piece.get_possible_moves_function()
        possible_moves_list: MOVE_LIST_TYPE = None
        if isinstance(piece, Pawn):
            possible_moves_list = get_possible_moves(
                position=position,
                is_valid_position=Chess.is_valid_position,
                is_piece=self.is_piece,
                is_player_piece=self.is_player_piece,
                board=self.board,
            )
        else:
            possible_moves_list = get_possible_moves(
                position=position,
                is_valid_position=Chess.is_valid_position,
                is_piece=self.is_piece,
                is_player_piece=self.is_player_piece,
            )
        return possible_moves_list

    def move_piece(
        self,
        current_position: POSITION_TYPE,
        move_position: POSITION_TYPE,
    ) -> None:
        """
        Instance method which moves a piece at current position to move position


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

        piece = self.board[current_position[0]][current_position[1]]
        if isinstance(piece, Pawn):
            pawn_move_piece = piece.get_move_piece_function()
            pawn_move_piece(
                board=self.board,
                current_position=current_position,
                move_position=move_position,
            )
        else:
            self.board[move_position[0]][move_position[1]] = self.board[
                current_position[0]
            ][current_position[1]]
            self.board[current_position[0]][current_position[1]] = None

    def place_pieces(self) -> None:
        """
        Instance method which place pieces on board at initialization of game
        """

        for player in PLAYERS:
            if player == "white":
                first_row = 1
                second_row = 2
            elif player == "black":
                first_row = 8
                second_row = 7

            for col in NUM_COL:

                # Placing Pawns
                self.board[second_row][col] = Pawn(player=player)

                # Placing Rook
                if col in (1, 8):
                    self.board[first_row][col] = Rook(player=player)

                # Placing Knight
                if col in (2, 7):
                    self.board[first_row][col] = Knight(player=player)

                # Placing Bishop
                if col in (3, 6):
                    self.board[first_row][col] = Bishop(player=player)

                # Placing Queen
                if col == 4:
                    self.board[first_row][col] = Queen(player=player)

                # Placing King
                if col == 5:
                    self.board[first_row][col] = King(player=player)

    def init_board(self) -> BOARD_TYPE:
        """
        Instance method which returns data structure of chess board

        
        Return
        ------
        board : BOARD_TYPE
            Data structure of chess board
        """

        return {x: {y: None for y in range(1, 9)} for x in range(8, 0, -1)}

    def display_board(self) -> None:
        """
        Instance method which prints chess board
        """

        print("------------------------------------------------------------")
        for row_no, row in self.board.items():
            print(row_no, end="|| ")
            for _, piece in row.items():
                Chess.print_piece(piece)
            print()
            if row_no == 1:
                print("============================================================")
            else:
                print("------------------------------------------------------------")

        print(" ", end="|| ")
        for alpha in ALPHABET_COL:
            Chess.print_piece(alpha)
        print(f"\n------------------------------------------------------------")

    def start_game(self) -> None:
        """
        Instance method which start game on command terminal
        """

        is_black_player = False
        is_quit = False
        previous_movement_str = ""

        while True:

            Chess.print_heading("| CHESS GAME |")
            print()
            Chess.print_heading(" Press Q to Quit")
            print()
            self.display_board()
            print(f"\n")
            Chess.print_heading(f" { PLAYERS[is_black_player].upper()} PLAYER TURN")
            print()
            if previous_movement_str:
                Chess.print_heading(previous_movement_str)

            print("", flush=True)

            while True:
                try:
                    entered_position = input("Enter Position of Piece to Move : ")
                    # Quit on pressing Q | q
                    if entered_position.upper() == "Q":
                        is_quit = True
                        break

                    # Checking input
                    if not Chess.is_valid_input(entered_input=entered_position):
                        raise InvalidInput()

                    # getting position tuple
                    position: POSITION_TYPE = Chess.get_tuple_position(
                        position_str=entered_position
                    )

                    # Checking if player selects his own piece
                    if not self.is_player_piece(
                        player=PLAYERS[is_black_player], position=position
                    ):
                        raise InvalidPosition(
                            f"Please Choose Position of {PLAYERS[is_black_player][0].upper()+PLAYERS[is_black_player][1:]} Piece"
                        )

                    # Getting possible moves of that piece
                    possible_moves_list: MOVE_LIST_TYPE = self.get_possible_moves(
                        position=position
                    )

                    # Printing possible moves
                    print()
                    Chess.print_heading(f"Press c to Change Piece")
                    self.print_piece_moves(
                        position=position, possible_moves_list=possible_moves_list
                    )

                    is_change_piece = False

                    while True:
                        print()
                        entered_move_position = input("Enter Position to Move : ")

                        if entered_move_position.upper() == "C":
                            is_change_piece = True
                            break

                        if entered_move_position.upper() == "Q":
                            is_quit = True
                            break

                        try:

                            # Checking input
                            if not Chess.is_valid_input(
                                entered_input=entered_move_position
                            ):
                                raise InvalidInput(
                                    "Invalid Move, Please Enter Valid Move"
                                )

                            # getting move position tuple
                            move_position: POSITION_TYPE = Chess.get_tuple_position(
                                position_str=entered_move_position
                            )

                            if move_position not in possible_moves_list:
                                raise InvalidMove()

                            # Moving piece
                            self.move_piece(
                                current_position=position, move_position=move_position
                            )

                            previous_movement_str = self.get_piece_movement_str(
                                current_position=position, move_position=move_position
                            )
                            print(previous_movement_str)

                            break

                        except InvalidInput as e:
                            print()
                            Chess.print_heading(f"{e}")

                        except InvalidMove as e:
                            print()
                            Chess.print_heading(f"{e}")

                    if is_change_piece:
                        continue

                    if is_quit:
                        break

                    break

                except InvalidInput as e:
                    print()
                    Chess.print_heading(f"{e}")
                    print()
                    continue

                except InvalidPosition as e:
                    print()
                    Chess.print_heading(f"{e}")
                    print()
                    continue

            # Quiting game
            if is_quit:
                print()
                Chess.print_heading("GAME IS FINSIHED")
                break

            is_black_player: bool = True if is_black_player == False else False

            os.system("clear")

    def start_ui_game(self):
        """
        Instance method which start game on tkinter GUI
        """

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("assets/theme.json")

        is_black_player = False

        app = App(
            self.board,
            is_black_player,
            self.get_possible_moves,
            self.move_piece,
        )

        app.mainloop()
