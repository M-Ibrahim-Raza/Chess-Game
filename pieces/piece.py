from abc import ABC, abstractmethod
from typing import Callable
from utils.custom_type_hints import PLAYERS_TYPE, POSITION_TYPE, MOVE_LIST_TYPE


class Piece(ABC):

    def __init__(self, player: PLAYERS_TYPE):
        self.player: PLAYERS_TYPE = player

    @abstractmethod
    def get_possible_moves_function(self) -> Callable[
        [
            POSITION_TYPE,
            Callable[[POSITION_TYPE], bool],
            Callable[[POSITION_TYPE], bool],
            Callable[[str, POSITION_TYPE], bool],
        ],
        MOVE_LIST_TYPE,
    ]:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass
