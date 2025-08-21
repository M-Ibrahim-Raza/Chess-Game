from utils.custom_type_hints import PLAYERS_TYPE, POSITION_TYPE, MOVE_LIST_TYPE
from typing import Callable
from pieces.piece import Piece


class King(Piece):

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
            possible_moves_list: MOVE_LIST_TYPE = []

            # For up
            move_position = (current_row + 1, current_col)
            if is_valid_position(move_position) and not is_player_piece(
                player=self.player, position=move_position
            ):
                possible_moves_list.append(move_position)

            # For down
            move_position = (current_row - 1, current_col)
            if is_valid_position(move_position) and not is_player_piece(
                player=self.player, position=move_position
            ):
                possible_moves_list.append(move_position)

            # For left
            move_position = (current_row, current_col - 1)
            if is_valid_position(move_position) and not is_player_piece(
                player=self.player, position=move_position
            ):
                possible_moves_list.append(move_position)

            # For right
            move_position = (current_row, current_col + 1)
            if is_valid_position(move_position) and not is_player_piece(
                player=self.player, position=move_position
            ):
                possible_moves_list.append(move_position)

            # For left upward
            move_position = (current_row + 1, current_col - 1)
            if is_valid_position(move_position) and not is_player_piece(
                player=self.player, position=move_position
            ):
                possible_moves_list.append(move_position)

            # For left downward
            move_position = (current_row - 1, current_col - 1)
            if is_valid_position(move_position) and not is_player_piece(
                player=self.player, position=move_position
            ):
                possible_moves_list.append(move_position)

            # For right upward
            move_position = (current_row + 1, current_col + 1)
            if is_valid_position(move_position) and not is_player_piece(
                player=self.player, position=move_position
            ):
                possible_moves_list.append(move_position)

            # For right downward
            move_position = (current_row - 1, current_col + 1)
            if is_valid_position(move_position) and not is_player_piece(
                player=self.player, position=move_position
            ):
                possible_moves_list.append(move_position)

            return possible_moves_list

        return get_possible_moves

    def get_image_path(self) -> str:
        return f"{self.player}/king.png"

    def __str__(self) -> str:
        if self.player == "white":
            return "♚"
        elif self.player == "black":
            return "♔"
