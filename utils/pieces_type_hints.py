from typing import Optional, Dict, TypeVar
from pieces.piece import Piece
from utils.custom_type_hints import NUM_ROW_TYPE, NUM_COL_TYPE

PIECE_TYPE = TypeVar("Piece", bound=Piece)
BOARD_TYPE = Dict[NUM_ROW_TYPE, Dict[NUM_COL_TYPE, Optional[PIECE_TYPE]]]
