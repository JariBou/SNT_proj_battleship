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


def remove_void_lists(List: list):
    for e in List:
        if not e:
            List.remove(e)


class Board:

    def __init__(self):
        self.colors = ['White', 'Black']
        self.checks_list = {'White': False, 'Black': False}
        self.player = 0
        self.board = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, Piece(Position([2, 2]), 'White'), None, Piece(Position([4, 2]), 'White'), None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, Piece(Position([2, 4]), 'White'), None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, Piece(Position([2, 6]), 'White'), None, None, None, None, None],
            [None, None, None, Piece(Position([3, 7]), 'Black', name='test piece'), None, None, None, None],
            ]

    def pass_board_to_pieces(self):
        for row in range(len(self.board)):
            for element in [e for e in self.board[row] if e is not None]:
                # noinspection PyUnresolvedReferences
                element.pass_board(self.board)

    def move_piece_to(self, piece, pos: Position):
        piece.move_to(pos)

    def force_move_to(self, piece, pos: Position):
        piece.force_move_to(pos)


class Piece:

    def __init__(self, position: Position, color, name=''):
        self.position = position
        self.color = color
        self.board = None
        self.visited = []
        self.valid_paths = []
        self.valid_positions = []
        self.curr_path = []
        self.name = name

    def __repr__(self):
        return f'Piece at {self.position.get_position()}, color={self.color}{f", name={self.name}" if self.name != "" else ""}, has_board={bool(self.board)}'

    def pass_board(self, board):
        self.board = board

    def print_name(self):
        print(self.name)

    def get_color(self) -> str:
        return self.color

    def get_valid_paths(self) -> list:
        self.valid_positions = []
        self.check_diagonals(self.position)

        return self.get_longest_paths()

        #USELESS# remove_void_lists(self.valid_paths)

    def check_diagonals(self, curr_pos: Position):
        ## Bottom Right diagonal
        print(curr_pos.y+2, '--', len(self.board))
        if curr_pos.y+2 <= len(self.board) and curr_pos.x+2 <= len(self.board[0]):
            print('bottom_right')
            target1 = self.board[curr_pos.y+1][curr_pos.x+1] if [curr_pos.x+1, curr_pos.y+1] not in self.visited else None
            if target1 is not None and target1.get_color() != self.color:
                print('valif target1\n')
                target2 = self.board[curr_pos.y+2][curr_pos.x+2]
                if target2 is None and [curr_pos.x+2, curr_pos.y+2] not in self.curr_path:
                    print('valif target2\n')
                    self.visited.append([curr_pos.x+1, curr_pos.y+1])
                    self.curr_path.append([[curr_pos.x+1, curr_pos.y+1], [curr_pos.x+2, curr_pos.y+2]])
                    self.check_diagonals(Position([curr_pos.x+2, curr_pos.y+2]))

        ## Top Right diagonal
        if curr_pos.y - 2 >= 0 and curr_pos.x + 2 <= len(self.board[0]):
            print('top_right')
            target1 = self.board[curr_pos.y-1][curr_pos.x+1] if [curr_pos.x+1, curr_pos.y-1] not in self.visited else None
            if target1 is not None and target1.get_color() != self.color:
                print('valif target1\n')
                target2 = self.board[curr_pos.y - 2][curr_pos.x + 2]
                if target2 is None and [curr_pos.x + 2, curr_pos.y - 2] not in self.curr_path:
                    print('valif target2\n')
                    self.visited.append([curr_pos.x+1, curr_pos.y-1])
                    self.curr_path.append([[curr_pos.x + 1, curr_pos.y - 1], [curr_pos.x + 2, curr_pos.y - 2]])
                    self.check_diagonals(Position([curr_pos.x + 2, curr_pos.y - 2]))

        ## Top Left diagonal
        if curr_pos.y - 2 >= 0 and curr_pos.x - 2 >= 0:
            print('top_left')
            target1 = self.board[curr_pos.y-1][curr_pos.x-1] if [curr_pos.x-1, curr_pos.y-1] not in self.visited else None
            if target1 is not None and target1.get_color() != self.color:
                print('valif target1\n')
                target2 = self.board[curr_pos.y - 2][curr_pos.x - 2]
                if target2 is None and [curr_pos.x - 2, curr_pos.y - 2] not in self.curr_path:
                    print('valif target2\n')
                    self.visited.append([curr_pos.x-1, curr_pos.y-1])
                    self.curr_path.append([[curr_pos.x - 1, curr_pos.y - 1], [curr_pos.x - 2, curr_pos.y - 2]])
                    self.check_diagonals(Position([curr_pos.x - 2, curr_pos.y - 2]))

        ## Bottom Left diagonal
        if curr_pos.y + 2 <= len(self.board) and curr_pos.x - 2 >= 0:
            print('bottom_left')
            target1 = self.board[curr_pos.y+1][curr_pos.x-1] if [curr_pos.x-1, curr_pos.y+1] not in self.visited else None
            if target1 is not None and target1.get_color() != self.color:
                print('valif target1\n')
                target2 = self.board[curr_pos.y + 2][curr_pos.x - 2]
                if target2 is None and [curr_pos.x - 2, curr_pos.y + 2] not in self.curr_path:
                    print('valif target2\n')
                    self.visited.append([curr_pos.x-1, curr_pos.y+1])
                    self.curr_path.append([[curr_pos.x - 1, curr_pos.y + 1], [curr_pos.x - 2, curr_pos.y + 2]])
                    self.check_diagonals(Position([curr_pos.x - 2, curr_pos.y + 2]))

        #print(f'non-tupled: {copy.deepcopy(self.curr_path)}\ntupled: {tuple(copy.deepcopy(self.curr_path))}')
        if self.curr_path and self.visited:
            self.visited.pop()
            self.valid_paths.append(copy.deepcopy(self.curr_path))
            self.curr_path.pop()

    def get_longest_paths(self) -> list:
        if not self.valid_paths:
            return []
        self.valid_paths.sort(key=len, reverse=True)
        possible_paths = []
        max_size = len(self.valid_paths[0])
        for e in self.valid_paths:
            if len(e) < max_size:
                return possible_paths
            possible_paths.append(copy.deepcopy(e))
        return possible_paths

    def move_to(self, pos: Position):
        ## Actually put this on gui side stick with an easy move_to()
        ## Easier to track number of moves
        possible_paths = self.get_longest_paths()
        if not possible_paths:
            side = -1 if self.color == 'Black' else 1
            for x_off in [1, -1]:
                try:
                    if self.board[self.position.y + 1 * side][self.position.x + x_off]:
                        self.valid_paths.append(
                            [[self.position.x, self.position.y], [self.position.x + x_off, self.position.y + 1 * side]])
                except IndexError:
                    pass
            if [pos.x, pos.y] in possible_paths:
                self.board[pos.y][pos.x] = self
                self.board[self.position.y][self.position.x] = None
        else:
            pass
        ## for eating stuff do smth like this:
        ## The player moves one by one, u just check that he his taking a good path like with like a for loop to
        ## check for position in self.valid_paths[a][nb_of_moves][1]  -> returns the position in path nb a after nb_of_moves moves
        ## Then to eat all necessary pieces you just have to record the path taken by the player, match it with a valid one
        ## and eat all pieces that need to be and that are defines in the path

    def move_on_path(self, next_pos: Position, move_number: int):
        for index, path in enumerate(self.valid_paths):
            if next_pos.get_position() != self.valid_paths[index][move_number][1]:
                self.valid_paths.remove(path)
        pass

    def force_move_to(self, pos: Position):
        self.board[self.position.y][self.position.x] = None
        self.board[pos.y][pos.x] = self
        self.position = Position([pos.x, pos.y])


class Queen:

    def __init__(self, position: Position, color):
        self.position = position
        self.color = color


if __name__ == '__main__':
    board = Board()
    board.pass_board_to_pieces()
    print(board.board[7][3])
    print('>>', str(board.board[7][3].get_valid_paths())[1:-1])


