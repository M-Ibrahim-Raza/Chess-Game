from utils.custom_type_hints import PLAYERS_TYPE, POSITION_TYPE, MOVE_LIST_TYPE
from typing import Callable
from pieces.piece import Piece


class Rook(Piece):

    def __init__(self, player: PLAYERS_TYPE):
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
            current_row: int = position[0]
            current_col: int = position[1]
            enemy_player: PLAYERS_TYPE = "white" if self.player == "black" else "black"
            possible_moves_list: MOVE_LIST_TYPE = []

            # For vertical moves

            # For forward moves
            for row in range(current_row + 1, 9):
                move_position = (row, current_col)
                if is_piece(move_position):
                    if is_player_piece(player=enemy_player, position=move_position):
                        possible_moves_list.append(move_position)
                    break
                possible_moves_list.append(move_position)

            # For backward moves
            for row in range(current_row - 1, 0, -1):
                move_position = (row, current_col)

                if is_piece(move_position):
                    if is_player_piece(player=enemy_player, position=move_position):
                        possible_moves_list.append(move_position)
                    break
                possible_moves_list.append(move_position)

            # For horizontal moves

            # For right moves
            for col in range(current_col + 1, 9):
                move_position = (current_row, col)
                if is_piece(move_position):
                    if is_player_piece(player=enemy_player, position=move_position):
                        possible_moves_list.append(move_position)
                    break
                possible_moves_list.append(move_position)

            # For left moves
            for col in range(current_col - 1, 0, -1):
                move_position = (current_row, col)
                if is_piece(move_position):
                    if is_player_piece(player=enemy_player, position=move_position):
                        possible_moves_list.append(move_position)
                    break
                possible_moves_list.append(move_position)

            return possible_moves_list

        return get_possible_moves

    def get_image_path(self) -> str:
        return f"{self.player}/rook.png"

    def __str__(self) -> str:
        if self.player == "white":
            return "♜"
        elif self.player == "black":
            return "♖"
