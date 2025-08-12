from utils.custom_type_hints import (
    PLAYERS_TYPE,
    POSITION_TYPE,
    MOVE_LIST_TYPE,
)
from utils.pieces_type_hints import BOARD_TYPE
from typing import Callable
from pieces.piece import Piece


class Pawn(Piece):

    def __init__(self, player: PLAYERS_TYPE):
        self.is_first_move: bool = True
        super().__init__(player=player)

    def get_possible_moves_function(self) -> Callable[
        [
            POSITION_TYPE,
            Callable[[POSITION_TYPE], bool],
            Callable[[POSITION_TYPE], bool],
            Callable[[str, POSITION_TYPE], bool],
        ],
        MOVE_LIST_TYPE,
    ]:

        def get_possible_moves(
            position: POSITION_TYPE,
            is_valid_position: Callable[[POSITION_TYPE], bool],
            is_piece: Callable[[POSITION_TYPE], bool],
            is_player_piece: Callable[[POSITION_TYPE], bool],
        ):
            possible_moves_list: MOVE_LIST_TYPE = []
            if self.player == "white":
                # For first move
                if self.is_first_move:
                    move_position = (position[0] + 2, position[1])
                    if is_valid_position(move_position) and not is_piece(move_position):
                        possible_moves_list.append(move_position)
                # For normal move
                move_position = (position[0] + 1, position[1])
                if is_valid_position(move_position) and not is_piece(move_position):
                    possible_moves_list.append(move_position)
                # For left forward kill
                move_position = (position[0] + 1, position[1] - 1)
                if is_valid_position(move_position) and is_player_piece(
                    player="black", position=move_position
                ):
                    possible_moves_list.append(move_position)
                # For right forward kill
                move_position = (position[0] + 1, position[1] + 1)
                if is_valid_position(move_position) and is_player_piece(
                    player="black", position=move_position
                ):
                    possible_moves_list.append(move_position)
            elif self.player == "black":
                # For first move
                if self.is_first_move:
                    move_position = (position[0] - 2, position[1])
                    if is_valid_position(move_position) and not is_piece(move_position):
                        possible_moves_list.append(move_position)
                # For normal move
                move_position = (position[0] - 1, position[1])
                if is_valid_position(move_position) and not is_piece(move_position):
                    possible_moves_list.append(move_position)
                # For left forward kill
                move_position = (position[0] - 1, position[1] - 1)
                if is_valid_position(move_position) and is_player_piece(
                    player="white", position=move_position
                ):
                    possible_moves_list.append(move_position)
                # For right forward kill
                move_position = (position[0] - 1, position[1] + 1)
                if is_valid_position(move_position) and is_player_piece(
                    player="white", position=move_position
                ):
                    possible_moves_list.append(move_position)

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
            if self.is_first_move:
                self.is_first_move = False
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
