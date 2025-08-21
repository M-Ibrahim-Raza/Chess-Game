from customtkinter import CTkButton, CTkImage
from PIL import Image


class Square(CTkButton):
    """
    TKinter button class which represents a square cell in chess board
    """

    def __init__(
        self, master, color, state="enabled", image=None, command=None, **kwargs
    ):

        self.image = image

        # Color of Square
        if color == "black":
            fg_color = "#000000"
            border_color = "#ffffff"
        elif color == "white":
            fg_color = "#ffffff"
            border_color = "#000000"

        # Call CTkButton constructor
        super().__init__(
            master,
            image=self.image,
            text="",
            width=120,
            height=110,
            state=state,
            fg_color=fg_color,
            border_color=border_color,
            command=command,
            **kwargs
        )
