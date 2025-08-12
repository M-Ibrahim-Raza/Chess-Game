from custom_type_hints import PLAYERS_TYPE, POSITION_TYPE,MOVE_LIST_TYPE
from piece import Piece

class Bishop(Piece):

    def __init__(self, player: PLAYERS_TYPE):
        super().__init__(player=player)

    def get_possible_moves_function(self):

        def get_possible_moves(
            position: POSITION_TYPE,
            is_valid_position,
            is_piece,
            is_player_piece,
        ):
            current_row = position[0]
            current_col = position[1]
            enemy_player = "white" if self.player == "black" else "black"
            possible_moves_list: MOVE_LIST_TYPE = []

            # For left moves

            # For left upward moves
            row = current_row + 1
            col = current_col - 1
            move_position = (row, col)
            while is_valid_position(move_position):
                if is_piece(move_position):
                    if is_player_piece(player=enemy_player, position=move_position):
                        possible_moves_list.append(move_position)
                    break
                possible_moves_list.append(move_position)
                row += 1
                col -= 1
                move_position = (row, col)

            # For left downward moves
            row = current_row - 1
            col = current_col - 1
            move_position = (row, col)
            while is_valid_position(move_position):
                if is_piece(move_position):
                    if is_player_piece(player=enemy_player, position=move_position):
                        possible_moves_list.append(move_position)
                    break
                possible_moves_list.append(move_position)
                row -= 1
                col -= 1
                move_position = (row, col)

            # For right moves

            # For right upward moves
            row = current_row + 1
            col = current_col + 1
            move_position = (row, col)
            while is_valid_position(move_position):
                if is_piece(move_position):
                    if is_player_piece(player=enemy_player, position=move_position):
                        possible_moves_list.append(move_position)
                    break
                possible_moves_list.append(move_position)
                row += 1
                col += 1
                move_position = (row, col)

            # For right downward moves
            row = current_row - 1
            col = current_col + 1
            move_position = (row, col)
            while is_valid_position(move_position):
                if is_piece(move_position):
                    if is_player_piece(player=enemy_player, position=move_position):
                        possible_moves_list.append(move_position)
                    break
                possible_moves_list.append(move_position)
                row -= 1
                col += 1
                move_position = (row, col)

            return possible_moves_list

        return get_possible_moves

    def __str__(self) -> str:
        if self.player == "white":
            return "♝"
        elif self.player == "black":
            return "♗"