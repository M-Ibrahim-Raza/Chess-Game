from utils.custom_type_hints import (
    PLAYERS_TYPE,
    POSITION_TYPE,
    MOVE_LIST_TYPE,
)
from utils.pieces_type_hints import BOARD_TYPE
from typing import Callable, Optional
from pieces.piece import Piece


class Pawn(Piece):

    def __init__(self, player: PLAYERS_TYPE):
        self.is_first_move: bool = True
        self.is_en_passant: bool = False
        super().__init__(player=player)

    def direction(self, step):
        if self.player == "white":
            return step
        elif self.player == "black":
            return -step

    def opponent_player(self):
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

        def get_possible_moves(
            position: POSITION_TYPE,
            is_valid_position: Callable[[POSITION_TYPE], bool],
            is_piece: Callable[[POSITION_TYPE], bool],
            is_player_piece: Callable[[PLAYERS_TYPE, POSITION_TYPE], bool],
            board: BOARD_TYPE = None,
        ):
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

        def move_piece(
            board: BOARD_TYPE,
            current_position: POSITION_TYPE,
            move_position: POSITION_TYPE,
        ):

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

    def __str__(self) -> str:
        if self.player == "white":
            return "♟"
        elif self.player == "black":
            return "♙"
