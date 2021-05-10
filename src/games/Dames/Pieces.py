import copy

from src.resources.utils.Constants import Position


## POSITIONS OF PIECES ARE AS FOllOWS: [x, y] AND GO TOP-> BOTTOM   LEFT -> RIGHT /!\


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
        self.colors = ['White', 'Black']
        self.checks_list = {'White': False, 'Black': False}
        self.player = 0
        self.board = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
            ]


class Piece:

    def __init__(self, position: Position, color):
        self.position = position
        self.color = color
        self.board = None

    def pass_board(self, board):
        self.board = board

    def get_valid_positions(self):
        valid_pos = []
        self.check_diagonals(self.position)

    def check_diagonals(self, curr_pos: Position):
        pos = copy.deepcopy(curr_pos)
        pos = Position(pos)
        side = 1 if self.color == 'black' else -1
        visited = []
        to_test_1 = self.board[pos.y+1*side][pos.x+1]
        if [pos.x+1, pos.y+1*side] not in visited and (to_test_1 is not None and to_test_1.get_color() != self.color):
            if self.board[pos.y+2*side][pos.x+2] is None:
                visited.append([pos.x+1, pos.y+1*side])
                visited.append([pos.x+2, pos.y+2*side])
                self.check_diagonals(Position([pos.x+2, pos.y+2*side]))
            pass

        ## Recursive calling
        pass


class Queen:

    def __init__(self, position: Position, color):
        self.position = position
        self.color = color

