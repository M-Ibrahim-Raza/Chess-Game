from abc import ABC, abstractmethod
from typing import Callable
from utils.custom_type_hints import PLAYERS_TYPE, POSITION_TYPE, MOVE_LIST_TYPE


class Piece(ABC):
    """
    Abstract Class representing chess piece
    """

    def __init__(self, player: PLAYERS_TYPE):
        """
        Piece class constructor which will be called in child class constructor


        Attributes
        ----------
        player : PLAYERS_TYPE
            black or white
        """

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
        """
        Abstract method which will return get possible move function
        """

        pass

    @abstractmethod
    def get_image_path(self) -> str:
        """
        Abstract method which will return path string of piece image
        """

        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Abstract method which will return symbol of peice
        """

        pass
