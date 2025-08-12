# --------------------| Invalid Input Custom Exception |
class InvalidInput(Exception):
    def __init__(self, message="Invalid Input Enter, Please Try Again"):
        self.message = message
        super().__init__(self.message)


# --------------------| Invalid Position Custom Exception |
class InvalidPosition(Exception):
    def __init__(self, message="Invalid Position Enter, Please Choose Your Piece Only"):
        self.message = message
        super().__init__(self.message)


# --------------------| Invalid Move Custom Exception |
class InvalidMove(Exception):
    def __init__(self, message="Invalid Move Enter, Please Enter Valid Move"):
        self.message = message
        super().__init__(self.message)
