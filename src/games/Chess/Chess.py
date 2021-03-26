from abc import ABC, abstractmethod


## POSITIONS OF PIECES ARE AS FOllOWS: [x, y] AND GO TOP-> BOTTOM   LEFT -> RIGHT /!\


class Board:

    def __init__(self):
        self.board = [
            [None, Knight('White', [1, 0]), None, None, None, None, Knight('White', [6, 0]), None],
            [Pawn('White', [i, 1]) for i in range(8)],
            [None, King('Black', [1, 2]), None, None, None, None, None, None],
            [None, None, Knight('White', [2, 3]), None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Pawn('Black', [i, 6]) for i in range(8)],
            [None, Knight('Black', [1, 7]), None, None, None, None, Knight('Black', [6, 7]), None]
            ]
        ## Do a dynamic board where instead of using a binary system to know if a piece is there just move the pieces in that list?
        ## Might be too hard tho....dk

    def move_piece_to(self, piece, new_position):
        if piece.move_to(new_position):
            self.board[new_position.y][new_position.x] = piece


class Position:

    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]

    def get_position(self):
        return self.x, self.y


class Chess_piece(ABC):

    def __init__(self, color, position, Type):
        self.color = color
        self.position = Position(position)
        self.type = Type

    def get_position(self, coordinates=False):
        return self.position if coordinates == False else self.position.get_position()

    def get_color(self):
        return self.color

    def get_type(self):
        return self.type

    def get_name(self):
        return f"{self.color.capitalize()} {self.type}"

    def move_to(self, new_position):
        """ Moves the piece to New position
        :param new_position: New position as [x, y]
        """
        if self.can_move_to(new_position):
            self.position = Position([new_position])
            return True
        else:
            return False

    def can_move_to(self, board, new_position):
        return new_position.get_position() in [pos.get_position() for pos in self.get_valid_positions(board)]

    @abstractmethod
    def checks(self):  ## Every subclass of this class will have to implement it
        """Checks if this piece puts the adversary king in check"""
        pass

    @abstractmethod
    def get_valid_positions(self, board):
        """Returns a list of valid positions to move the piece to"""
        pass


class Pawn(Chess_piece):

    def get_valid_positions(self, board):
        ## HOL' UP PAWNS CAN ONLY MOVE IN ONE DIRECTION
        side = 1 if self.color == 'White' else -1
        valid_positions = []
        if self.first_move:
            if board[self.position.y + (side * 2)][self.position.x] is None:
                valid_positions.append(Position([self.position.x, self.position.y + (side * 2)]))
        if board[self.position.y + side][self.position.x] is None:
            valid_positions.append(Position([self.position.x, self.position.y + side]))

        to_test = []
        offsets = (1, -1)
        for offset in offsets:
            try:
                to_test.append(board[self.position.y + side][self.position.x + offset])
                to_test.append([self.position.x + offset, self.position.y + side])
            except IndexError:
                pass
        for i in range(0, len(to_test), 2):
            if not (to_test[i] is None) and not (to_test[i].get_color() is self.color):
                valid_positions.append(Position(to_test[i+1]))

        # try:
        #     if not (board[self.position.y + side][self.position.x + 1].get_color() is self.color):
        #         valid_positions.append(Position([self.position.x + 1, self.position.y + side]))
        #     if not (board[self.position.y + side][self.position.x - 1].get_color() is self.color):
        #         valid_positions.append(Position([self.position.x - 1, self.position.y + side]))
        # except AttributeError:
        #     pass  ## No pieces in it's diagonal
        return valid_positions

    def checks(self):
        pass

    def __init__(self, color, position):
        super().__init__(color, position, 'Pawn')
        self.first_move = True  ## When you move for the first time, set this to false pretty please
        ## Useless just for a representation of how it can move  {might be useful actually}
        self.move_pattern = [[self.position.x, self.position.y + 1], [self.position.x - 1, self.position.y + 1],
                             [self.position.x + 1, self.position.y + 1]]


class Knight(Chess_piece):

    def get_valid_positions(self, board):
        ## THIS SHIT WORKED ON FIRST TRY
        ##  print('HAPPINESS LVL MAXIMUM')
        valid_positions = []
        to_test = []
        offsets = [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, -2], [1, 2], [-1, -2], [-1, 2]]
        for offset in offsets:
            try:
                to_test.append(board[self.position.y + offset[0]][self.position.x + offset[1]])
                to_test.append([self.position.x + offset[1], self.position.y + offset[0]])
            except IndexError:
                pass
        # to_test = [board[self.position.y + 2][self.position.x + 1], [self.position.x + 1, self.position.y + 2],
        #            board[self.position.y + 2][self.position.x - 1], [self.position.x - 1, self.position.y + 2],
        #            board[self.position.y - 2][self.position.x + 1], [self.position.x + 1, self.position.y - 2],
        #            board[self.position.y - 2][self.position.x - 1], [self.position.x - 1, self.position.y - 2],
        #            board[self.position.y + 1][self.position.x - 2], [self.position.x - 2, self.position.y + 1],
        #            board[self.position.y + 1][self.position.x + 2], [self.position.x + 2, self.position.y + 1],
        #            board[self.position.y - 1][self.position.x - 2], [self.position.x - 2, self.position.y - 1],
        #            board[self.position.y - 1][self.position.x + 2], [self.position.x + 2, self.position.y - 1]]

        for i in range(0, len(to_test), 2):
            try:
                if (to_test[i] is None) or not (to_test[i].get_color() is self.color):
                    valid_positions.append(Position(to_test[i + 1]))
            except AttributeError:
                pass

        # try:
        #     if (board[self.position.y + 2][self.position.x + 1] is None) or not (
        #             board[self.position.y + 2][self.position.x + 1].get_color() is self.color):
        #         valid_positions.append(Position([self.position.x + 1, self.position.y + 2]))
        #     if board[self.position.y + 2][self.position.x - 1] is None or not (
        #             board[self.position.y + 2][self.position.x - 1].get_color() is self.color):
        #         valid_positions.append(Position([self.position.x - 1, self.position.y + 2]))
        #     if board[self.position.y - 2][self.position.x + 1] is None or not (
        #             board[self.position.y - 2][self.position.x + 1].get_color() is self.color):
        #         valid_positions.append(Position([self.position.x + 1, self.position.y - 2]))
        #     if board[self.position.y - 2][self.position.x - 1] is None or not (
        #             board[self.position.y - 2][self.position.x - 1].get_color() is self.color):
        #         valid_positions.append(Position([self.position.x - 1, self.position.y - 2]))
        #     if board[self.position.y + 1][self.position.x - 2] is None or not (
        #             board[self.position.y + 1][self.position.x - 2].get_color() is self.color):
        #         valid_positions.append(Position([self.position.x - 2, self.position.y + 1]))
        #     if board[self.position.y + 1][self.position.x + 2] is None or not (
        #             board[self.position.y + 1][self.position.x + 2].get_color() is self.color):
        #         valid_positions.append(Position([self.position.x + 2, self.position.y + 1]))
        #     if board[self.position.y - 1][self.position.x - 2] is None or not (
        #             board[self.position.y - 1][self.position.x - 2].get_color() is self.color):
        #         valid_positions.append(Position([self.position.x - 2, self.position.y - 1]))
        #     if board[self.position.y - 1][self.position.x + 2] is None or not (
        #             board[self.position.y - 1][self.position.x + 2].get_color() is self.color):
        #         valid_positions.append(Position([self.position.x + 2, self.position.y - 1]))
        # except AttributeError:
        #     pass
        return valid_positions

    def checks(self):
        pass

    def __init__(self, color, position):
        super().__init__(color, position, 'Knight')
        ## Useless just for a representation of how it can move  {might be useful actually}
        self.move_pattern = [[self.position.x + 1, self.position.y + 2], [self.position.x - 1, self.position.y + 2],
                             [self.position.x + 1, self.position.y - 2], [self.position.x - 1, self.position.y - 2],
                             [self.position.x + 2, self.position.y + 1], [self.position.x + 2, self.position.y - 1],
                             [self.position.x - 2, self.position.y + 1], [self.position.x - 2, self.position.y - 1]]


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
                    top_right = True if board_position is not None else False
                    if (board_position is None) or not (board_position.get_color() is self.color):
                        valid_positions.append(Position([self.position.x + i, self.position.y + i]))
                except IndexError:
                    top_right = True
            if (not top_left) and (self.position.x - i >= 0):
                try:
                    board_position = board[self.position.y + i][self.position.x - i]
                    bottom_left = True if board_position is not None else False
                    if (board_position is None) or not (board_position.get_color() is self.color):
                        valid_positions.append(Position([self.position.x - i, self.position.y + i]))
                except IndexError:
                    top_left = True
            if (not bottom_left) and (self.position.y - i >= 0 and self.position.x - i >= 0):
                try:
                    board_position = board[self.position.y - i][self.position.x - i]
                    bottom_left = True if board_position is not None else False
                    if (board_position is None) or not (board_position.get_color() is self.color):
                        valid_positions.append(Position([self.position.x - i, self.position.y - i]))
                except IndexError:
                    bottom_left = True
            if (not bottom_right) and (self.position.y - i >= 0):
                try:
                    board_position = board[self.position.y - i][self.position.x + i]
                    bottom_right = True if board_position is not None else False
                    if (board_position is None) or not (board_position.get_color() is self.color):
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


class King(Chess_piece):

    def __init__(self, color, position):
        super().__init__(color, position, 'King')

    def checks(self):
        pass

    def get_valid_positions(self, board):
        pass

    def is_checked(self, board):
        ### MAYBE DO A REVERSE? LIKE, YOU CHECK FROM THE KING IF HE WERE SAID PIECE IF IT COULD GET TO HIM
        ### LIKE YOU CHECK DIAGONALLY FROM THE KING AND STUFF
        checkers = []
        for row in board:
            for piece in [p for p in row if (not (p is None) and p.get_color() != self.get_color())]:
                if piece.can_move_to(board, self.position):
                    checkers.append(piece)
        if checkers:
            print(f"{self.get_name()} is checked by:")
            for piece in checkers:
                print(f"- {piece.get_name()} in {piece.get_position(True)}")
            return True
        return False


class Tower(Chess_piece):

    def get_valid_positions(self, board):
        valid_positions = []
        top = False
        bottom = False
        left = False
        right = False
        for i in range(1, len(board)):
            if not top:
                try:
                    board_position = board[self.position.y + i][self.position.x]
                    top = True if board_position is not None else False
                    if (board_position is None) or not (board_position.get_color() is self.color):
                        valid_positions.append(Position([self.position.x, self.position.y + i]))
                except IndexError:
                    top = True
            if (not bottom) and (self.position.y - i >= 0):
                try:
                    board_position = board[self.position.y - i][self.position.x]
                    bottom = True if board_position is not None else False
                    if (board_position is None) or not (board_position.get_color() == self.color):
                        valid_positions.append(Position([self.position.x, self.position.y - i]))
                except IndexError:
                    bottom = True
            if (not left) and (self.position.x - i >= 0):
                try:
                    board_position = board[self.position.y][self.position.x - i]
                    left = True if board_position is not None else False
                    if (board_position is None) or not (board_position.get_color() is self.color):
                        valid_positions.append(Position([self.position.x - i, self.position.y]))
                except IndexError:
                    left = True
            if not right:
                try:
                    board_position = board[self.position.y][self.position.x + i]
                    right = True if board_position is not None else False
                    if (board_position is None) or not (board_position.get_color() is self.color):
                        valid_positions.append(Position([self.position.x + i, self.position.y]))
                except IndexError:
                    right = True
        return valid_positions

    def checks(self):
        pass

    def __init__(self, color, position):
        super().__init__(color, position, 'Tower')
        ## Useless just for a representation of how it can move  {might be useful actually}
        i = 0
        self.move_pattern = [[self.position.x + i, self.position.y], [self.position.x - i, self.position.y],
                             [self.position.x, self.position.y - i], [self.position.x, self.position.y + i]]


if __name__ == '__main__':
    b = Board()
    # for value in b.board:
    #     print(value)
    positions = []
    # for a in b.board[3][2].get_valid_positions(b.board):
    #     positions.append(a.get_position())
    # positions.sort()
    # for k in positions:
    #     print(k)
    print(b.board[2][1].is_checked(b.board))
    # print(b.board[3][2].get_valid_positions(b.board))
    # print(b.board[3][2].can_move_to(b.board, Position([2, 2])))
