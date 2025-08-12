from abc import ABC, abstractmethod
from typing import TypeVar
from custom_type_hints import PLAYERS_TYPE

class Piece(ABC):

    def __init__(self, player: PLAYERS_TYPE):
        self.player: PLAYERS_TYPE = player

    # @abstractmethod
    # def possible_moves(self,current_position:Tuple[NUM_COL_TYPE,NUM_ROW_TYPE]):
    #     pass

    @abstractmethod
    def __str__(self) -> str:
        pass

PIECE_TYPE = TypeVar("Piece", bound=Piece)