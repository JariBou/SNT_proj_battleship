from abc import ABC, abstractmethod


class Board:

    def __init__(self):
        self.board = [
                      [None, Knight('White', [1, 0]), None, None, None, None, Knight('White', [6, 0]), None],
                      [Pawn('White', [i, 1]) for i in range(8)],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [None, None, None, None, None, None, None, None],
                      [Pawn('Black', [i, 6]) for i in range(8)],
                      [None, Knight('Black', [1, 7]), None, None, None, None, Knight('Black', [6, 7]), None]
                      ]
        ## Do a dynamic board where instead of using a binary system to know if a piece is there just move the pieces in that list?
        ## Might be too hard tho....dk


class Chess_piece(ABC):

    def __init__(self, color, position, Type):
        self.color = color
        self.position = position
        self.type = Type

    def get_position(self):
        return self.position

    def get_color(self):
        return self.color

    def get_type(self):
        return self.type

    @abstractmethod   ## Every subclass of this class will have to implement it
    def can_move_to(self, board, new_position):
        pass


class Pawn(Chess_piece):

    def __init__(self, color, position):
        super().__init__(color, position, 'Pawn')
        ## Useless just for a representation of how it can move
        self.move_pattern = [[self.position[0], self.position[1] + 1], [self.position[0] - 1, self.position[1] + 1],
                             [self.position[0] + 1, self.position[1] + 1]]

    def can_move_to(self, board, new_position):
        pass


class Knight(Chess_piece):

    def __init__(self, color, position):
        super().__init__(color, position, 'Knight')

    def can_move_to(self, board, new_position):
        pass
