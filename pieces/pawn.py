from utils.custom_type_hints import (
    PLAYERS_TYPE,
    POSITION_TYPE,
    MOVE_LIST_TYPE,
)
from utils.pieces_type_hints import BOARD_TYPE
from typing import Callable, Optional
from pieces.piece import Piece


class Pawn(Piece):
    """
    Class representing pawn piece

    - Inherits Piece base abstract class
    """

    def __init__(self, player: PLAYERS_TYPE):
        """
        Pawn class constructor which initialize the Pawn object


        Attributes
        ----------
        is_first_move : bool
            checks if first move

        is_en_passant : bool
            checks if en passant move is valid or not
        """

        self.is_first_move: bool = True
        self.is_en_passant: bool = False
        super().__init__(player=player)

    def direction(self, step: int):
        """
        Returns vertical step size based on player
            Positive direction for white ( bottom to top )
            Negative direction for black ( top to bottom )


        Parameters
        ----------
        step : int
            vertical step size


        Return
        ------
        step : int
            vertical step size based on player
        """

        if self.player == "white":
            return step
        elif self.player == "black":
            return -step

    def opponent_player(self):
        """
        Returns team of opponent player
        """

        if self.player == "white":
            return "black"
        elif self.player == "black":
            return "white"

    def get_possible_moves_function(self) -> Callable[
        [
            POSITION_TYPE,
            Callable[[POSITION_TYPE], bool],
            Callable[[POSITION_TYPE], bool],
            Callable[[str, POSITION_TYPE], bool],
            Optional[BOARD_TYPE],
        ],
        MOVE_LIST_TYPE,
    ]:
        """
        Returns get possible move function
        """

        def get_possible_moves(
            position: POSITION_TYPE,
            is_valid_position: Callable[[POSITION_TYPE], bool],
            is_piece: Callable[[POSITION_TYPE], bool],
            is_player_piece: Callable[[PLAYERS_TYPE, POSITION_TYPE], bool],
            board: BOARD_TYPE = None,
        ) -> MOVE_LIST_TYPE:
            """
            Returns list of possible moves of pawn piece based on its position


            Parameters
            ----------
            position : POSITION_TYPE
                Tuple of position ( row_no , column_no )

            is_valid_position : Callable[[POSITION_TYPE], bool]
                A method that takes position tuple and checks if position is valid or not

            is_piece : Callable[[POSITION_TYPE], bool]
                A method that takes position tuple and checks if there is any piece at that position

            is_player_piece : Callable[[POSITION_TYPE], bool]
                A method that takes position tuple and checks if there is any piece of certain player at that position

            board : BOARD_TYPE
                Board data structure of chess


            Return
            ------
            possible_moves_list : MOVE_LIST_TYPE
                List of all possible moves tuples of pawn
            """

            possible_moves_list: MOVE_LIST_TYPE = []
            dir = self.direction
            opp = self.opponent_player

            # For first move
            if self.is_first_move:
                move_position = (position[0] + dir(2), position[1])
                if is_valid_position(move_position) and not is_piece(move_position):
                    possible_moves_list.append(move_position)

            # For normal move
            move_position = (position[0] + dir(1), position[1])
            if is_valid_position(move_position) and not is_piece(move_position):
                possible_moves_list.append(move_position)

            # For left forward kill
            move_position = (position[0] + dir(1), position[1] - 1)
            if is_valid_position(move_position) and is_player_piece(
                player=opp(), position=move_position
            ):
                possible_moves_list.append(move_position)

            # For right forward kill
            move_position = (position[0] + dir(1), position[1] + 1)
            if is_valid_position(move_position) and is_player_piece(
                player=opp(), position=move_position
            ):
                possible_moves_list.append(move_position)

            # For left en passant
            piece_to_kill_position = (position[0], position[1] - 1)
            if is_valid_position(piece_to_kill_position) and is_player_piece(
                player=opp(), position=piece_to_kill_position
            ):
                piece_to_kill = board[position[0]][position[1] - 1]
                if isinstance(piece_to_kill, Pawn) and piece_to_kill.is_en_passant:
                    move_position = (position[0] + dir(1), position[1] - 1)
                    possible_moves_list.append(move_position)
                    piece_to_kill.is_en_passant = False

            # For right en passant
            piece_to_kill_position = (position[0], position[1] + 1)
            if is_valid_position(piece_to_kill_position) and is_player_piece(
                player=opp(), position=piece_to_kill_position
            ):
                piece_to_kill = board[position[0]][position[1] + 1]
                if isinstance(piece_to_kill, Pawn) and piece_to_kill.is_en_passant:
                    move_position = (position[0] + dir(1), position[1] + 1)
                    possible_moves_list.append(move_position)
                    piece_to_kill.is_en_passant = False

            return possible_moves_list

        return get_possible_moves

    def get_move_piece_function(
        self,
    ) -> Callable[[BOARD_TYPE, POSITION_TYPE, POSITION_TYPE], None]:
        """
        Returns move piece function
        """

        def move_piece(
            board: BOARD_TYPE,
            current_position: POSITION_TYPE,
            move_position: POSITION_TYPE,
        ):
            """
            Move pawn from current position to move position


            Parameters
            ----------
            board : BOARD_TYPE
                Board data structure of chess

            current_position : POSITION_TYPE
                Tuple of current position ( row_no , column_no )

            move_position : POSITION_TYPE
                Tuple of move position ( row_no , column_no )


            Return
            ------
            None
            """

            # Disallow en passant kill on second move
            if self.is_en_passant == True:
                self.is_en_passant = False

            if self.is_first_move:
                self.is_first_move = False

                # Allow en passant kill on first move with 2 steps
                if (abs(move_position[0] - current_position[0])) == 2:
                    self.is_en_passant = True

            # If kill move and killing position is empty (en-passant condition)
            if (abs(move_position[1] - current_position[1])) == 1:
                if board[move_position[0]][move_position[1]] is None:
                    # Killing pawn at previous position
                    if (
                        board[current_position[0]][current_position[1]].player
                        == "white"
                    ):
                        board[move_position[0] - 1][move_position[1]] = None
                    else:
                        board[move_position[0] + 1][move_position[1]] = None

            board[move_position[0]][move_position[1]] = board[current_position[0]][
                current_position[1]
            ]

            board[current_position[0]][current_position[1]] = None

        return move_piece

    def get_image_path(self) -> str:
        """
        Returns path string of pawn.png image
        """

        return f"{self.player}/pawn.png"

    def __str__(self) -> str:
        """
        Returns symbol of pawn
        """

        if self.player == "white":
            return "♟"
        elif self.player == "black":
            return "♙"
