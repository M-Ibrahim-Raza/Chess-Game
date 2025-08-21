from typing import Literal, Tuple, List

ALPHABET_COL_TYPE = Literal["a", "b", "c", "d", "e", "f", "g", "h"]
NUM_COL_TYPE = Literal[1, 2, 3, 4, 5, 6, 7, 8]
NUM_ROW_TYPE = Literal[1, 2, 3, 4, 5, 6, 7, 8]
UI_NUM_COL_TYPE = Literal[0, 1, 2, 3, 4, 5, 6, 7]
UI_NUM_ROW_TYPE = Literal[0, 2, 3, 4, 5, 6, 7, 8]
POSITION_TYPE = Tuple[NUM_ROW_TYPE, NUM_COL_TYPE]
UI_POSITION_TYPE = Tuple[UI_NUM_ROW_TYPE, UI_NUM_COL_TYPE]
MOVE_LIST_TYPE = List[Tuple[NUM_ROW_TYPE, NUM_COL_TYPE]]
PLAYERS_TYPE = Literal["white", "black"]
