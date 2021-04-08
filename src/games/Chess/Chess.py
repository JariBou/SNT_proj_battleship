import copy
import tkinter as tk
from abc import ABC, abstractmethod

from src.resources.utils.Constants import Position

## POSITIONS OF PIECES ARE AS FOllOWS: [x, y] AND GO TOP-> BOTTOM   LEFT -> RIGHT /!\
from time import time


def get_flattened(seq):
    se = copy.deepcopy(seq)
    flattened_list = []
    for elt in se:
        t = type(elt)
        if t is tuple or t is list:
            for elt2 in get_flattened(elt):
                flattened_list.append(elt2)
        else:
            flattened_list.append(elt)
    return flattened_list


class Board:

    def __init__(self):
        ##TODO: implement system to force to get out of check
        self.colors = ['White', 'Black']
        self.checks_list = {'White': False, 'Black': False}
        self.player = 0
        self.board = [
            [Tower('White', [0, 0]), Knight('White', [1, 0]), Bishop('White', [2, 0]), Queen('White', [3, 0]),
             King('White', [4, 0]), Bishop('White', [5, 0]), Knight('White', [6, 0]), Tower('White', [7, 0])],
            [Pawn('White', [i, 1]) for i in range(8)],

            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,

            [Pawn('Black', [i, 6]) for i in range(8)],
            [Tower('Black', [0, 7]), Knight('Black', [1, 7]), Bishop('Black', [2, 7]), Queen('Black', [3, 7]),
             King('Black', [4, 7]), Bishop('Black', [5, 7]), Knight('Black', [6, 7]), Tower('Black', [7, 7])]
            ]
        ### Do a dynamic board where instead of using a binary system to know if a piece is there just move the pieces in that list?
        ### Might be too hard tho....dk
        ##  Actually super easy, Barely an inconveniance, shoulda used cell class for each cell tho....

    def get(self, x, y):
        print(f'getting at: {x, y}')
        return self.board[y][x]

    def move_piece_to(self, piece, new_position):
        """
        :param piece: ChessPiece class
        :param new_position: Position class
        """
        if piece.move_to(new_position):
            self.board[new_position.y][new_position.x] = piece
            print(f'Moved {piece.get_name()} to {piece.get_position(True)}')
            return True
        else:
            print(f'Error while moving piece: {piece} to {new_position}')
            return False

    def check_for_checks(self, color):
        """returns True if king of color is check"""

        kings_list = [piece for piece in [cell for cell in get_flattened(self.board) if cell is not None] if (piece.__class__ == King and piece.get_color == color)]

        for king in kings_list:
            print(king.get_name())
            print(king.get_position(True))
            return king.is_checked()

        # pieces_list = []
        # for row in range(len(self.board)):
        #     for column in range(len(self.board[0])):
        #         piece = self.board[row][column]
        #         if piece.__class__ == King:
        #             pieces_list.append(self.board[row][column])
        # for element in pieces_list:
        #     print(element.get_name())
        #
        #
        # row_list = [row for row in self.board]
        # pieces_list = [element for element in row_list]
        # for king in [kings for kings in [element for element in [self.board[i] for i in range(len(self.board))]] if kings.__class__ == King]:
        #     king.is_checked()

    def pass_board_to_pieces(self):
        for row in range(len(self.board)):
            for element in [e for e in self.board[row] if e is not None]:
                element.pass_new_board(self.board)

    def print_board(self):
        for row in self.board:
            string_row = ''
            for element in row:
                try:
                    string_row += element.get_name() + ', '
                except AttributeError:
                    string_row += 'None' + ', '
            print(string_row)

    def switch_player(self):
        self.player = 1 if self.player == 0 else 0

    def can_move_freely(self, player):
        return not self.check_for_checks(self.colors[player])

    def return_board(self):
        return self.board

    def set_board(self, board):
        self.board = board


class ChessPiece(ABC):

    def __init__(self, color, position, Type):
        self.color = color
        self.position = position if isinstance(position, Position) else Position(position)
        self.type = Type
        self.board = None

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.get_name()}, position={self.position.get_position(True)}'

    def get_position(self, coordinates=False):
        return self.position if not coordinates else self.position.get_position()

    def get_color(self):
        return self.color

    def get_type(self):
        return self.type

    def get_name(self):
        return f"{self.color.capitalize()} {self.type}"

    def force_move_to(self, new_position):
        self.board[self.position.y][self.position.x] = None
        self.position = new_position
        self.board[new_position.y][new_position.x] = self
        return True

    def move_to(self, new_position):
        """ Moves the piece to New position
        :param new_position: New position as a Position class
        :return: True if success, False if fail
        """
        if not self.can_move_to(new_position):
            return False
        # print('Can move')
        # print(new_position.get_position())
        logic_board = copy.deepcopy(self.board)
        logic_board[self.position.y][self.position.x] = None
        logic_piece = copy.deepcopy(self)
        logic_piece.position = new_position
        logic_board[new_position.y][new_position.x] = logic_piece
        b_class = Board()

        b_class.set_board(logic_board)

        b_class.pass_board_to_pieces()

        player = 0 if self.color == 'White' else 1
        # print('------logic board-------')
        # b_class.print_board()
        # print('------------------------')
        # if isinstance(logic_piece, King):
        #     print(logic_piece.is_checked(next_board=logic_board, next_position=new_position))
        # print('------------------------')

        if not b_class.can_move_freely(player):
            print('FFFFFFF')
            return False

        self.board[self.position.y][self.position.x] = None
        self.position = new_position
        self.board[new_position.y][new_position.x] = self
        return True

    def can_move_to(self, new_position):
        return new_position.get_position() in [pos.get_position() for pos in self.get_valid_positions()]

    def pass_new_board(self, board):
        self.board = board

    @abstractmethod
    def checks(self):  ## USELESS??? MAYBE REMOVE IT DUMBASS??
        """Checks if this piece puts the adversary king in check"""
        pass

    @abstractmethod
    def get_valid_positions(self):   ## Every subclass of this class will have to implement it
        """Returns a list of valid positions to move the piece to"""
        pass


class Pawn(ChessPiece):

    def __init__(self, color, position):
        super().__init__(color, position, 'Pawn')
        self.first_move = True  ## When you move for the first time, set this to false pretty please
        self.over = False
        self.w = None

    def get_valid_positions(self):
        ## HOL' UP PAWNS CAN ONLY MOVE IN ONE DIRECTION, na its good fam, done it
        side = 1 if self.color == 'White' else -1
        valid_positions = []
        if self.first_move:
            if self.board[self.position.y + (side * 2)][self.position.x] is None:
                valid_positions.append(Position([self.position.x, self.position.y + (side * 2)]))

        side_max = 7 if self.color == 'White' else 0
        if self.position.y == side_max:
            return []

        if self.board[self.position.y + side][self.position.x] is None:
            valid_positions.append(Position([self.position.x, self.position.y + side]))

        to_test = []
        offsets = (1, -1)
        for offset in offsets:
            try:  ##TODO: FIX THIS SHIT MOTHERFUCKER LIKE RN, MOVE YA ASS BOIIII
                ##TODO: YOU FCKING LAZY PERSON, MOVE YA ASSSSSSS
                to_test.append(self.board[self.position.y + side][self.position.x + offset])
                to_test.append([self.position.x + offset, self.position.y + side])
            except IndexError:
                pass
        for i in range(0, len(to_test), 2):
            if not (to_test[i] is None) and not (to_test[i].get_color() is self.color):
                valid_positions.append(Position(to_test[i + 1]))

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

    def move_to(self, new_position):
        if super().move_to(new_position):
            self.first_move = False
            side_max = 7 if self.color == 'White' else 0
            if self.position.y == side_max:
                self.over = True
            return True
        return False

    def reached_end(self):
        return self.over

    def transform(self):
        self.w = tk.Tk()
        self.w.title('Trasform into:')
        bishop = tk.Button(self.w, text='Bishop', command=lambda: self.t_intp(Bishop))
        bishop.grid(row=0, column=0)
        tower = tk.Button(self.w, text='Tower', command=lambda: self.t_intp(Tower))
        tower.grid(row=0, column=1)
        queen = tk.Button(self.w, text='Queen', command=lambda: self.t_intp(Queen))
        queen.grid(row=1, column=0)
        knight = tk.Button(self.w, text='Knight', command=lambda: self.t_intp(Knight))
        knight.grid(row=1, column=1)
        self.w.mainloop()

    def t_intp(self, piece_type):
        print(piece_type)
        self.board[self.position.y][self.position.x] = piece_type(self.color, self.position)
        self.w.destroy()
        self.w.quit()


class Knight(ChessPiece):

    def __init__(self, color, position):
        super().__init__(color, position, 'Knight')

    def get_valid_positions(self):
        ## THIS SHIT WORKED ON FIRST TRY
        ##  print('HAPPINESS LVL MAXIMUM')
        valid_positions = []
        to_test = []
        offsets = [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, -2], [1, 2], [-1, -2], [-1, 2]]
        for offset in offsets:
            try:
                to_test.append(self.board[self.position.y + offset[0]][self.position.x + offset[1]])
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


class Bishop(ChessPiece):

    def __init__(self, color, position):
        super().__init__(color, position, 'Bishop')

    def get_valid_positions(self):
        valid_positions = []
        top_right = False
        top_left = False
        bottom_right = False
        bottom_left = False

        for i in range(1, len(self.board)):
            if not top_right:
                try:
                    board_position = self.board[self.position.y + i][self.position.x + i]
                    top_right = True if board_position is not None else False
                    if (board_position is None) or not (board_position.get_color() is self.color):
                        valid_positions.append(Position([self.position.x + i, self.position.y + i]))
                except IndexError:
                    top_right = True
            if (not top_left) and (self.position.x - i >= 0):
                try:
                    board_position = self.board[self.position.y + i][self.position.x - i]
                    bottom_left = True if board_position is not None else False
                    if (board_position is None) or not (board_position.get_color() is self.color):
                        valid_positions.append(Position([self.position.x - i, self.position.y + i]))
                except IndexError:
                    top_left = True
            if (not bottom_left) and (self.position.y - i >= 0 and self.position.x - i >= 0):
                try:
                    board_position = self.board[self.position.y - i][self.position.x - i]
                    bottom_left = True if board_position is not None else False
                    if (board_position is None) or not (board_position.get_color() is self.color):
                        valid_positions.append(Position([self.position.x - i, self.position.y - i]))
                except IndexError:
                    bottom_left = True
            if (not bottom_right) and (self.position.y - i >= 0):
                try:
                    board_position = self.board[self.position.y - i][self.position.x + i]
                    bottom_right = True if board_position is not None else False
                    if (board_position is None) or not (board_position.get_color() is self.color):
                        valid_positions.append(Position([self.position.x + i, self.position.y - i]))
                except IndexError:
                    bottom_right = True
        return valid_positions

    def checks(self):
        pass


class King(ChessPiece):

    ##TODO: Fix bishop not detecting pawns for check and king not being able to move while in check

    def __init__(self, color, position):
        super().__init__(color, position, 'King')
        self.first_move = True
        self.ruck_pos_tower = []   ## [ [Position, Tower], [Position, Tower ]
        self.ruck_pos_king = []

    def checks(self):
        pass  ## Useless to check for check because it cannot do dat

    def get_valid_positions(self):
        offsets = [[1, -1], [1, 0], [1, 1], [0, 1]]
        valid_positions = []
        x = self.position.x
        y = self.position.y

        try:
            # print(self, self.first_move)
            if self.first_move:
                self.ruck_pos_tower = []
                self.ruck_pos_king = []
                for i, k in zip([1, -1], [3, -4]):  ## Problem????????
                    position_1off = self.board[y][x + 1 * i]
                    Position_1off = Position([x + 1 * i, y])
                    position_2off = self.board[y][x + 2 * i]
                    Position_2off = Position([x + 2 * i, y])

                    if position_1off is not None or position_2off is not None:
                        # print('continue 1')
                        continue
                    if self.ruck_check_test(Position_1off, Position_2off):
                        # print('continue2.5')
                        continue

                    possible_tower = self.board[y][x + k]
                    if not isinstance(possible_tower, Tower):
                        # print('continue 3')
                        continue

                    if possible_tower.first_move:
                        possible_tower_position = Position([x + k, y])
                        possible_position = Position([x + 2 * i, y])
                        print(possible_position.get_position())
                        valid_positions.append(possible_position)
                        self.ruck_pos_tower.append([Position([x + 1 * i, y]), possible_tower_position])
                        self.ruck_pos_king.append(Position([x + 2 * i, y]))
        except IndexError:   ##when getting valid positions right before rucking
            pass

        for i in [1, -1]:
            for offset in offsets:
                try:
                    position = self.board[y + offset[0] * i][x + offset[1] * i]
                    if (position is None) or (position.get_color() != self.color):
                        valid_positions.append(
                            Position([x + offset[1] * i, y + offset[0] * i]))
                except IndexError:
                    pass
        return valid_positions

    def ruck_check_test(self, Position_1off, Position_2off):
        b_class = Board()

        player = 0 if self.color == 'White' else 1

        logic_piece = copy.deepcopy(self)
        for position in [Position_1off, Position_2off]:
            logic_board = copy.deepcopy(self.board)
            b_class.set_board(logic_board)
            b_class.pass_board_to_pieces()
            logic_board[self.position.y][self.position.x] = None
            logic_piece.position = position
            logic_board[position.y][position.x] = logic_piece

            try:
                if not b_class.can_move_freely(player):
                    return True
            except IndexError:
                pass

    def is_checked(self, next_board=None, next_position=None):
        ### MAYBE DO A REVERSE? LIKE, YOU CHECK FROM THE KING IF HE WERE SAID PIECE IF IT COULD GET TO HIM
        ### LIKE YOU CHECK DIAGONALLY FROM THE KING AND STUFF
        ## Na we good fam
        ### Use this to check if a move prevents the check
        board = self.board if next_board is None else next_board
        checkers = []   
        position = self.position if next_position is None else next_position
        for row in board:
            for piece in [p for p in row if (not (p is None) and p.get_color() != self.get_color())]:
                if piece.can_move_to(position):
                    checkers.append(piece)
        if checkers:
            # print(f"{self.get_name()} in {self.get_position(True)} is checked by:")
            # for piece in checkers:
            #     print(f"- {piece.get_name()} in {piece.get_position(True)}  --  {[pos.get_position() for pos in piece.get_valid_positions()]}")
            return True
        return False

    def gets_checked(self, new_position):
        next_board = copy.deepcopy(self.board)
        next_board[self.position.y][self.position.x] = None
        next_board[new_position.y][new_position.x] = self
        if self.is_checked(next_board, new_position):
            return False
        return True

    def can_move_to(self, new_position):
        if not self.gets_checked(new_position):
            return False
        else:
            return new_position.get_position() in [pos.get_position() for pos in self.get_valid_positions()]

    def move_to(self, new_position):
        if super().move_to(new_position):
            if self.ruck_pos_tower:  # if it is != []
                # print('list not None')
                for i in range(len(self.ruck_pos_tower)):
                    # print(f'new_position: {new_position.get_position()}  -  king_pos: {self.ruck_pos_king[i].get_position()}')
                    # print(f'Tower_test={self.board[self.ruck_pos_tower[i][1].y][self.ruck_pos_tower[i][1].x]}')
                    # print(f'Tower_position={self.ruck_pos_tower[i][0].get_position()}')
                    if new_position.get_position() == self.ruck_pos_king[i].get_position():
                        # print('inside if condition')
                        self.board[self.ruck_pos_tower[i][1].y][self.ruck_pos_tower[i][1].x].force_move_to(self.ruck_pos_tower[i][0])
            self.first_move = False
            return True
        return False

    def is_mat(self):  ##TODO: implement this
        pass


class Tower(ChessPiece):

    def __init__(self, color, position):
        super().__init__(color, position, 'Tower')
        self.first_move = True

    def get_valid_positions(self):
        valid_positions = []
        top = False
        bottom = False
        left = False
        right = False
        for i in range(1, len(self.board)):
            if not top:
                try:
                    board_position = self.board[self.position.y + i][self.position.x]
                    top = True if board_position is not None else False
                    if (board_position is None) or not (board_position.get_color() is self.color):
                        valid_positions.append(Position([self.position.x, self.position.y + i]))
                except IndexError:
                    top = True
            if (not bottom) and (self.position.y - i >= 0):
                try:
                    board_position = self.board[self.position.y - i][self.position.x]
                    bottom = True if board_position is not None else False
                    if (board_position is None) or not (board_position.get_color() == self.color):
                        valid_positions.append(Position([self.position.x, self.position.y - i]))
                except IndexError:
                    bottom = True
            if (not left) and (self.position.x - i >= 0):
                try:
                    board_position = self.board[self.position.y][self.position.x - i]
                    left = True if board_position is not None else False
                    if (board_position is None) or not (board_position.get_color() is self.color):
                        valid_positions.append(Position([self.position.x - i, self.position.y]))
                except IndexError:
                    left = True
            if not right:
                try:
                    board_position = self.board[self.position.y][self.position.x + i]
                    right = True if board_position is not None else False
                    if (board_position is None) or not (board_position.get_color() is self.color):
                        valid_positions.append(Position([self.position.x + i, self.position.y]))
                except IndexError:
                    right = True
        return valid_positions

    def checks(self):
        pass

    def move_to(self, new_position):
        if super().move_to(new_position):
            self.first_move = False
            return True
        return False


class Queen(ChessPiece):

    def __init__(self, color, position):
        super().__init__(color, position, 'Queen')

    def checks(self):
        pass

    # noinspection PyTypeChecker
    def get_valid_positions(self):
        logic_board = copy.deepcopy(self.board)
        positions_list = []
        for Type in [Bishop, Tower]:
            piece = Type(self.color, self.position)
            logic_board[self.position.y][self.position.x] = piece
            piece.pass_new_board(logic_board)
            # print(f'Queen-side: {{{Type}}}={[pos.get_position() for pos in piece.get_valid_positions()]}')
            positions_list += piece.get_valid_positions()
        return positions_list


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
    b.pass_board_to_pieces()
    b.print_board()
    print(b.board[1][1])
    # print(b.board[2][1].is_checked(b.board))
    # print(b.board[3][2].get_valid_positions(b.board))
    # print(b.board[3][2].can_move_to(b.board, Position([2, 2])))
