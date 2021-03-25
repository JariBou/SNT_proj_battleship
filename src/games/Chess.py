from abc import ABC, abstractmethod


## POSITIONS OF PIECES ARE AS FOllOWS: [x, y] AND GO TOP-> BOTTOM   LEFT -> RIGHT /!\


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


class Position:

    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]


class Chess_piece(ABC):

    def __init__(self, color, position, Type):
        self.color = color
        self.position = Position(position)
        self.type = Type

    def get_position(self):
        return self.position

    def get_color(self):
        return self.color

    def get_type(self):
        return self.type

    @abstractmethod  ## Every subclass of this class will have to implement it
    def can_move_to(self, board, new_position):
        pass

    @abstractmethod
    def checks(self):
        """Checks if this piece puts the adversary king in check"""
        pass

    @abstractmethod
    def get_valid_positions(self, board):
        """Returns a list of valid positions to move the piece to"""
        pass


class Pawn(Chess_piece):

    def get_valid_positions(self, board):
        pass

    def checks(self):
        pass

    def __init__(self, color, position):
        super().__init__(color, position, 'Pawn')
        ## Useless just for a representation of how it can move  {might be useful actually}
        self.move_pattern = [[self.position.x, self.position.y + 1], [self.position.x - 1, self.position.y + 1],
                             [self.position.x + 1, self.position.y + 1]]

    def can_move_to(self, board, new_position):
        pass


class Knight(Chess_piece):

    def get_valid_positions(self, board):
        pass

    def checks(self):
        pass

    def __init__(self, color, position):
        super().__init__(color, position, 'Knight')
        ## Useless just for a representation of how it can move  {might be useful actually}
        self.move_pattern = [[self.position.x + 1, self.position.y + 2], [self.position.x - 1, self.position.y + 2],
                             [self.position.x + 1, self.position.y - 2], [self.position.x - 1, self.position.y - 2],
                             [self.position.x + 2, self.position.y + 1], [self.position.x + 2, self.position.y - 1],
                             [self.position.x - 2, self.position.y + 1], [self.position.x - 2, self.position.y - 1]]

    def can_move_to(self, board, new_position):
        pass


class Bishop(Chess_piece):

    def get_valid_positions(self, board):
        valid_positions = []
        top_right = False
        top_left = False
        bottom_right = False
        bottom_left = False
        for i in range(1, len(board)):
            if not top_right:
                try:
                    board_position = board[self.position.y + i][self.position.x + i]
                    if (board_position is None) or (board.get_color is not self.get_color()):
                        valid_positions.append(Position([self.position.x + i, self.position.y + i]))
                except IndexError:
                    top_right = True
            if not top_left:
                try:
                    board_position = board[self.position.y + i][self.position.x - i]
                    if (board_position is None) or (board.get_color is not self.get_color()):
                        valid_positions.append(Position([self.position.x - i, self.position.y + i]))
                except IndexError:
                    top_left = True
            if not bottom_left:
                try:
                    board_position = board[self.position.y - i][self.position.x - i]
                    if (board_position is None) or (board.get_color is not self.get_color()):
                        valid_positions.append(Position([self.position.x - i, self.position.y - i]))
                except IndexError:
                    bottom_left = True
            if not bottom_right:
                try:
                    board_position = board[self.position.y - i][self.position.x + i]
                    if (board_position is None) or (board.get_color is not self.get_color()):
                        valid_positions.append(Position([self.position.x + i, self.position.y - i]))
                except IndexError:
                    bottom_right = True
        return valid_positions

    def checks(self):
        pass

    def __init__(self, color, position):
        super().__init__(color, position, 'Bishop')
        ## Useless just for a representation of how it can move  {might be useful actually}
        i = 0
        self.move_pattern = [[self.position.x + i, self.position.y + i], [self.position.x - i, self.position.y + i],
                             [self.position.x + i, self.position.y - i], [self.position.x - i, self.position.y - i]]

    def can_move_to(self, board, new_position):
        pass


class King(Chess_piece):

    def can_move_to(self, board, new_position):
        pass

    def checks(self):
        pass

    def get_valid_positions(self, board):
        pass