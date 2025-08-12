from custom_type_hints import PLAYERS_TYPE, POSITION_TYPE,MOVE_LIST_TYPE
from piece import Piece

class King(Piece):

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
            possible_moves_list: MOVE_LIST_TYPE = []

            # For up
            move_position = (current_row+1,current_col)
            if is_valid_position(move_position) and not is_player_piece(player=self.player, position=move_position):
                possible_moves_list.append(move_position)

            # For down
            move_position = (current_row-1,current_col)
            if is_valid_position(move_position) and not is_player_piece(player=self.player, position=move_position):
                possible_moves_list.append(move_position)

            # For left
            move_position = (current_row,current_col-1)
            if is_valid_position(move_position) and not is_player_piece(player=self.player, position=move_position):
                possible_moves_list.append(move_position)

            # For right
            move_position = (current_row,current_col+1)
            if is_valid_position(move_position) and not is_player_piece(player=self.player, position=move_position):
                possible_moves_list.append(move_position)

            # For left upward
            move_position = (current_row+1,current_col-1)
            if is_valid_position(move_position) and not is_player_piece(player=self.player, position=move_position):
                possible_moves_list.append(move_position)

            # For left downward
            move_position = (current_row-1,current_col-1)
            if is_valid_position(move_position) and not is_player_piece(player=self.player, position=move_position):
                possible_moves_list.append(move_position)

            # For right upward
            move_position = (current_row+1,current_col+1)
            if is_valid_position(move_position) and not is_player_piece(player=self.player, position=move_position):
                possible_moves_list.append(move_position)

            # For right downward
            move_position = (current_row-1,current_col+1)
            if is_valid_position(move_position) and not is_player_piece(player=self.player, position=move_position):
                possible_moves_list.append(move_position)

            return possible_moves_list

        return get_possible_moves

    def __str__(self) -> str:
        if self.player == "white":
            return "♚"
        elif self.player == "black":
            return "♔"