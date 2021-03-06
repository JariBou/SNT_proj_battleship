## Code Cleaned Up ##

import copy
import tkinter as tk
from abc import ABC, abstractmethod
from typing import Optional, Union

from src.resources.utils.Constants import Position
from src.resources.utils.Constants import Constants as Ct


## POSITIONS OF PIECES ARE AS FOllOWS: [x, y] AND GO TOP-> BOTTOM   LEFT -> RIGHT /!\


#####          STATIC METHODS          ####
def get_board(board_size: list[int, int], variant_name: str) -> list[list[Optional['ChessPiece']]]:
    if board_size == [8, 8]:
        return [
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

    elif board_size == [5, 6]:
        if variant_name == 'Chess attack':
            return [
                [Tower('White', [0, 0]), Knight('White', [1, 0]), Bishop('White', [2, 0]), Queen('White', [3, 0]),
                 King('White', [4, 0])],
                [Pawn('White', [i, 1]) for i in range(5)],

                [None] * 8,
                [None] * 8,

                [Pawn('Black', [i, 4]) for i in range(5)],
                [Tower('Black', [0, 5]), Knight('Black', [1, 5]), Bishop('Black', [2, 5]), Queen('Black', [3, 5]),
                 King('Black', [4, 5])]
                ]
        elif variant_name == 'Speed chess':
            return [
                [Queen('White', [0, 0]), King('White', [1, 0]), Bishop('White', [2, 0]), Knight('White', [3, 0]),
                 Tower('White', [4, 0])],
                [Pawn('White', [i, 1]) for i in range(5)],

                [None] * 8,
                [None] * 8,

                [Pawn('Black', [i, 4]) for i in range(5)],
                [Tower('Black', [0, 5]), Knight('Black', [1, 5]), Bishop('Black', [2, 5]), King('Black', [3, 5]),
                 Queen('Black', [4, 5])]
                ]
        elif variant_name == 'Elena chess':
            return [
                [Tower('White', [0, 0]), Bishop('White', [1, 0]), King('White', [2, 0]), Queen('White', [3, 0]),
                 Knight('White', [4, 0])],
                [Pawn('White', [i, 1]) for i in range(5)],

                [None] * 8,
                [None] * 8,

                [Pawn('Black', [i, 4]) for i in range(5)],
                [Knight('Black', [0, 5]), Queen('Black', [1, 5]), King('Black', [2, 5]), Bishop('Black', [3, 5]),
                 Tower('Black', [4, 5])]
                ]

    elif board_size == [4, 5]:
        if variant_name == 'Microchess':
            return [
                [King('White', [0, 0]), Knight('White', [1, 0]), Bishop('White', [2, 0]), Tower('White', [3, 0])],
                [Pawn('White', [0, 1]), None, None, None],

                [None] * 4,

                [None, None, None, Pawn('Black', [3, 3])],
                [Tower('Black', [0, 4]), Bishop('Black', [1, 4]), Knight('Black', [2, 4]),
                 King('Black', [3, 4])]
                ]
        elif variant_name == 'Silverman 4??5':
            return [
                [Tower('White', [0, 0]), Queen('White', [1, 0]), King('White', [2, 0]), Tower('White', [3, 0])],
                [Pawn('White', [i, 1]) for i in range(4)],

                [None] * 4,

                [Pawn('Black', [i, 3]) for i in range(4)],
                [Tower('Black', [0, 4]), Queen('Black', [1, 4]), King('Black', [2, 4]),
                 Tower('Black', [3, 4])]
                ]

    elif board_size == [5, 5]:
        if variant_name == 'Baby chess':
            return [
                [King('White', [0, 0]), Queen('White', [1, 0]), Bishop('White', [2, 0]), Knight('White', [3, 0]),
                 Tower('White', [4, 0])],
                [Pawn('White', [i, 1]) for i in range(5)],

                [None] * 8,

                [Pawn('Black', [i, 3]) for i in range(5)],
                [Tower('Black', [0, 4]), Knight('Black', [1, 4]), Bishop('Black', [2, 4]),
                 Queen('Black', [3, 4]), King('Black', [4, 4])]
                ]
        elif variant_name == 'Jacobs???Meirovitz':
            return [
                [Bishop('White', [0, 0]), Knight('White', [1, 0]), Tower('White', [2, 0]), Queen('White', [3, 0]),
                 King('White', [4, 0])],
                [Pawn('White', [i, 1]) for i in range(5)],

                [None] * 8,

                [Pawn('Black', [i, 3]) for i in range(5)],
                [King('Black', [0, 4]), Queen('Black', [1, 4]), Tower('Black', [2, 4]),
                 Knight('Black', [3, 4]), Bishop('Black', [4, 4])]
                ]
        elif variant_name == 'Gardner':
            return [
                [Tower('White', [0, 0]), Knight('White', [1, 0]), Bishop('White', [2, 0]), Queen('White', [3, 0]),
                 King('White', [4, 0])],
                [Pawn('White', [i, 1]) for i in range(5)],

                [None] * 8,

                [Pawn('Black', [i, 3]) for i in range(5)],
                [Tower('Black', [0, 4]), Knight('Black', [1, 4]), Bishop('Black', [2, 4]),
                 Queen('Black', [3, 4]), King('Black', [4, 4])]
                ]

    elif board_size == [6, 6]:
        return [
            [Tower('White', [0, 0]), Knight('White', [1, 0]), Queen('White', [2, 0]), King('White', [3, 0]),
             Knight('White', [4, 0]), Tower('White', [5, 0])],
            [Pawn('White', [i, 1]) for i in range(6)],

            [None] * 8,
            [None] * 8,

            [Pawn('Black', [i, 4]) for i in range(6)],
            [Tower('Black', [0, 5]), Knight('Black', [1, 5]), Queen('Black', [2, 5]), King('Black', [3, 5]),
             Knight('Black', [4, 5]), Tower('Black', [5, 5])]
            ]
####                                  ####


class Board:

    def __init__(self, board_size=None, variant_name=''):
        if board_size is None:
            board_size = [8, 8]
        self.colors = ['White', 'Black']
        self.checks_list = {'White': False, 'Black': False}
        self.player = 0
        self.board: list[list[Optional[ChessPiece]]] = get_board(board_size, variant_name)
        ### Do a dynamic board where instead of using a binary system to know if a piece is there just move the pieces in that list?
        ### Might be too hard tho....dk
        ##  Actually super easy, Barely an inconvenience, shoulda used cell class for each cell tho....
        ## Jk it's trash using a class for each cell

    def get(self, x: int, y: int) -> Optional['ChessPiece']:
        print(f'getting at: {x, y}    -  element: {self.board[y][x]}')
        return self.board[y][x]

    def move_piece_to(self, piece: 'ChessPiece', new_position: Position) -> bool:
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

    def get_king(self, color: str) -> 'King':
        piece: King    ## Just so that Pycharm gives me a break, it isn't actually True, in the end it is but actually not
        kings_list: list[King] = [piece for piece in Ct.get_flattened(self.board) if
                                  piece.__class__ == King and piece.get_color() == color]
        if not kings_list:  ##Should never be an error since you should always have a king
            raise AttributeError('ERROR: KING LIST EMPTY')
        return kings_list[0]

    def hkdnjcheck_for_checks(self, color: Union[str, int]) -> bool:
        """returns True if king of color is check"""
        if not isinstance(color, str):
            color = self.colors[color]
        print('\nchecking for checks for:')
        king = self.get_king(color)
        print(f'-{king.get_name()} at {king.get_position(True)}\n')
        return king.is_checked()

    def check_over(self, player: int) -> bool:
        """Checks if game is over"""
        color = self.colors[player]
        piece_list = [piece for piece in [cell for cell in Ct.get_flattened(self.board) if cell is not None] if
                      piece.get_color() == color]
        if not piece_list:
            print("ERROR 'check_over', 'piece_list' EMPTY")
        for piece in piece_list:
            valid_positions = piece.get_valid_positions()
            for position in valid_positions:
                if piece.able_to_move(position):
                    print(f'hello==={piece, position}')
                    return False
        return True

    def pass_board_to_pieces(self):
        for row in range(len(self.board)):
            for element in [e for e in self.board[row] if e is not None]:
                element.pass_new_board(self.board)

    def print_board(self):   # For debuging
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

    def can_move_freely(self, player) -> bool:
        return not self.check_for_checks(self.colors[player])

    def return_board(self) -> list[list[Optional['ChessPiece']]]:
        return self.board

    def set_board(self, board: list[list[Optional['ChessPiece']]]):
        self.board = board


class ChessPiece(ABC):

    def __init__(self, color: str, position, Type: str):
        self.color = color
        self.position = position if isinstance(position, Position) else Position(position)
        self.type = Type
        self.board: Optional[list[list[Optional['ChessPiece']]]] = None

    def __repr__(self):
        return f'{self.__class__.__name__}(name={self.get_name()}, position={self.position.get_position()}'

    def get_position(self, coordinates=False) -> Union[Position, list[int, int]]:
        """If coordinates is True returns a list[int, int] of the position instead of the <Position> class"""
        return self.position if not coordinates else self.position.get_position()

    def get_color(self) -> str:
        return self.color

    def get_type(self) -> str:
        return self.type

    def get_name(self) -> str:
        return f"{self.color.capitalize()} {self.type}"

    def force_move_to(self, new_position: Position) -> bool:
        """Moves a piece even if normally wouldn't be able to"""
        self.board[self.position.y][self.position.x] = None
        self.position = new_position
        self.board[new_position.y][new_position.x] = self
        return True

    def move_to(self, new_position: Position) -> bool:
        """ Moves the piece to New position
        :param new_position: New position as a Position class
        :return: True if success, False if fail
        """
        if not self.can_move_to(new_position):
            return False
        logic_board: list[list[Optional[ChessPiece]]] = copy.deepcopy(self.board)
        logic_board[self.position.y][self.position.x] = None
        logic_piece: ChessPiece = copy.deepcopy(self)
        logic_piece.position = new_position
        logic_board[new_position.y][new_position.x] = logic_piece
        b_class = Board()

        b_class.set_board(logic_board)
        b_class.pass_board_to_pieces()

        player = 0 if self.color == 'White' else 1
        if not b_class.can_move_freely(player):
            print('cannot_move_freely')
            return False
        if self.board[new_position.y][new_position.x] is not None:
            print(f'{self} eats {self.board[new_position.y][new_position.x]}')
        self.board[self.position.y][self.position.x] = None
        self.position = new_position
        self.board[new_position.y][new_position.x] = self
        return True

    def can_move_to(self, new_position: Position) -> bool:
        return new_position.get_position() in [pos.get_position() for pos in self.get_valid_positions()]

    def able_to_move(self, new_position: Position) -> bool:
        """Just checks if a piece as a valid position that gets the player out of check"""
        logic_board: list[list[Optional[ChessPiece]]] = copy.deepcopy(self.board)
        logic_board[self.position.y][self.position.x] = None
        logic_piece: ChessPiece = copy.deepcopy(self)
        logic_piece.position = new_position
        logic_board[new_position.y][new_position.x] = logic_piece
        b_class = Board()
        b_class.set_board(logic_board)
        b_class.pass_board_to_pieces()
        player = 0 if self.color == 'White' else 1
        if not b_class.can_move_freely(player):
            return False
        return True

    def pass_new_board(self, board: list[list[Optional['ChessPiece']]]):
        self.board = board

    @abstractmethod
    def get_valid_positions(self) -> list[Optional[Position]]:  ## Every subclass of this class will have to implement it
        """Returns a list of valid positions to move the piece to"""
        pass


class Pawn(ChessPiece):

    def __init__(self, color: str, position):
        super().__init__(color, position, 'Pawn')
        self.first_move = True  ## When you move for the first time, set this to false pretty please
        self.over = False
        self.w: Optional[tk.Tk] = None

    def get_valid_positions(self) -> list[Optional[Position]]:  ## HOL' UP PAWNS CAN ONLY MOVE IN ONE DIRECTION, na its good fam, done it
        side = 1 if self.color == 'White' else -1
        valid_positions: list[Position] = []
        if self.first_move:
            try:
                if self.board[self.position.y + (side * 2)][self.position.x] is None and \
                        self.board[self.position.y + side][self.position.x] is None:
                    valid_positions.append(Position([self.position.x, self.position.y + (side * 2)]))
            except IndexError:  ## On small boards the check check goes outside of boundaries
                pass
        side_max = (len(self.board) - 1) if self.color == 'White' else 0
        if self.position.y == side_max:
            return []

        if self.board[self.position.y + side][self.position.x] is None:
            valid_positions.append(Position([self.position.x, self.position.y + side]))

        offsets = (1, -1)
        for offset in offsets:
            try:
                target: Optional[ChessPiece] = self.board[self.position.y + side][self.position.x + offset]
                if not (target is None) and not (target.get_color() is self.color):
                    valid_positions.append(Position([self.position.x + offset, self.position.y + side]))
            except IndexError:
                pass
        return valid_positions

    def move_to(self, new_position: Position) -> bool:
        if super().move_to(new_position):
            self.first_move = False
            side_max = (len(self.board) - 1) if self.color == 'White' else 0
            if self.position.y == side_max:
                self.over = True
            return True
        return False

    def reached_end(self) -> bool:
        return self.over

    def transform(self):
        self.w = tk.Tk(screenName='hello')
        self.w.title('Trasform into:')
        for name, typ, index in zip(['Bishop', 'Tower', 'Queen', 'Knight'], [Bishop, Tower, Queen, Knight],
                                    list(range(4))):
            tk.Button(self.w, text=name, command=lambda t=typ: self.t_into(t)).grid(row=index // 2,
                                                                                    column=index % 2)
        self.w.mainloop()

    def t_into(self, piece_type):
        print(piece_type)
        self.board[self.position.y][self.position.x] = piece_type(self.color, self.position)
        self.w.destroy()
        self.w.quit()


class Knight(ChessPiece):

    def __init__(self, color: str, position):
        super().__init__(color, position, 'Knight')

    def get_valid_positions(self) -> list[Optional[Position]]:
        valid_positions: list[Position] = []  ## THIS SHIT WORKED ON FIRST TRY
        offsets = [[2, 1], [2, -1], [-2, 1], [-2, -1], [1, -2], [1, 2], [-1, -2],
                   [-1, 2]]  ##  print('HAPPINESS LVL MAXIMUM')
        for offset in offsets:
            try:
                target: Optional[ChessPiece] = self.board[self.position.y + offset[0]][self.position.x + offset[1]]
                if (target is None) or not (target.get_color() is self.color):
                    valid_positions.append(Position([self.position.x + offset[1], self.position.y + offset[0]]))
            except IndexError:
                pass
        return valid_positions


class Bishop(ChessPiece):

    def __init__(self, color: str, position):
        super().__init__(color, position, 'Bishop')

    def get_valid_positions(self) -> list[Optional[Position]]:
        valid_positions: list[Position] = []
        top_right = top_left = bottom_right = bottom_left = False

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
                    top_left = True if board_position is not None else False
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


class King(ChessPiece):

    def __init__(self, color: str, position):
        super().__init__(color, position, 'King')
        self.first_move = True
        self.ruck_pos_tower: list[list[Position, 'Tower']] = []  ## [ [Position, Tower], [Position, Tower ]
        self.ruck_pos_king: list[Position] = []

    def get_valid_positions(self) -> list[Optional[Position]]:
        offsets = [[1, -1], [1, 0], [1, 1], [0, 1]]
        valid_positions: list[Position] = []
        x = self.position.x
        y = self.position.y

        try:
            if self.first_move:
                self.ruck_pos_tower = []
                self.ruck_pos_king = []
                for i, k in zip([1, -1], [3, -4]):  ## Problem????????  na we good
                    position_1off = self.board[y][x + 1 * i]
                    Position_1off = Position([x + 1 * i, y])
                    position_2off = self.board[y][x + 2 * i]
                    Position_2off = Position([x + 2 * i, y])

                    if position_1off is not None or position_2off is not None:
                        continue
                    if self.ruck_check_test(Position_1off, Position_2off):
                        continue

                    possible_tower = self.board[y][x + k]
                    if not isinstance(possible_tower, Tower):
                        continue

                    if possible_tower.first_move:
                        possible_tower_position = Position([x + k, y])
                        possible_position = Position([x + 2 * i, y])
                        valid_positions.append(possible_position)
                        self.ruck_pos_tower.append([Position([x + 1 * i, y]), possible_tower_position])
                        self.ruck_pos_king.append(Position([x + 2 * i, y]))
        except IndexError:  ##when getting valid positions right before rucking
            pass

        for i in [1, -1]:
            for offset in offsets:
                try:
                    position = self.board[y + offset[0] * i][x + offset[1] * i]
                    if y + offset[0] * i < 0 or x + offset[1] * i < 0:
                        continue
                    if (position is None) or (position.get_color() != self.color):
                        valid_positions.append(
                            Position([x + offset[1] * i, y + offset[0] * i]))
                except IndexError:
                    pass
        return valid_positions

    def ruck_check_test(self, Position_1off: Position, Position_2off: Position) -> bool:
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
        return False

    def is_checked(self, next_board: list = None, next_position: Position = None) -> bool:
        ### MAYBE DO A REVERSE? LIKE, YOU CHECK FROM THE KING IF HE WERE SAID PIECE IF IT COULD GET TO HIM
        ### LIKE YOU CHECK DIAGONALLY FROM THE KING AND STUFF
        ## Na we good fam, would be slightly better but would give out too long code that wouldn't be pythonic, might
        ## implement it later though, as an option to choose from idk
        ### Use this to check if a move prevents the check
        board: list[list[Optional[ChessPiece]]] = self.board if next_board is None else next_board
        position: Position = self.position if next_position is None else next_position
        for row in board:
            for piece in [p for p in row if ((p is not None) and p.get_color() != self.get_color())]:
                if piece.can_move_to(position):
                    return True
        return False

    def gets_checked(self, new_position: Position) -> bool:
        next_board = copy.deepcopy(self.board)
        next_board[self.position.y][self.position.x] = None
        next_board[new_position.y][new_position.x] = self
        if self.is_checked(next_board, new_position):
            return False
        return True

    def can_move_to(self, new_position: Position) -> bool:
        if not self.gets_checked(new_position):
            return False
        else:
            return new_position.get_position() in [pos.get_position() for pos in self.get_valid_positions()]

    def move_to(self, new_position: Position) -> bool:
        if super().move_to(new_position):
            if self.ruck_pos_tower:
                for i in range(len(self.ruck_pos_tower)):
                    if new_position.get_position() == self.ruck_pos_king[i].get_position():
                        self.board[self.ruck_pos_tower[i][1].y][self.ruck_pos_tower[i][1].x].force_move_to(
                            self.ruck_pos_tower[i][0])
            self.first_move = False
            return True
        return False


class Tower(ChessPiece):

    def __init__(self, color: str, position):
        super().__init__(color, position, 'Tower')
        self.first_move = True

    def get_valid_positions(self) -> list[Optional[Position]]:
        valid_positions: list[Position] = []
        top = bottom = left = right = False
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

    def move_to(self, new_position: Position) -> bool:
        if super().move_to(new_position):
            self.first_move = False
            return True
        return False


class Queen(ChessPiece):

    def __init__(self, color: str, position):
        super().__init__(color, position, 'Queen')

    # noinspection PyTypeChecker
    def get_valid_positions(self) -> list[Optional[Position]]:
        logic_board: list[list[Optional[ChessPiece]]] = copy.deepcopy(self.board)
        positions_list: list[Position] = []
        for Type in [Bishop, Tower]:  ##A Queen's movement can be defined as the combination of a Bishop and a Tower
            piece: ChessPiece = Type(self.color, self.position)
            logic_board[self.position.y][self.position.x] = piece
            piece.pass_new_board(logic_board)
            positions_list += piece.get_valid_positions()
        return positions_list
