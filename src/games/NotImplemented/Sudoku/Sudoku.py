import copy
import random
from functools import cache

from src.resources.utils.Constants import Position


class Cell:

    def __init__(self, mother, position):
        self.mother = mother
        self.position = position
        self.value = None

    def set_value(self, val):
        self.value = val

    def __repr__(self):
        return f'{self.__class__.__name__} at {self.position.get_position()}, child of: {self.mother}'


class MotherCell:

    def __init__(self, mother_board, position, create_cells=False):
        self.mother_board = mother_board
        self.position = position
        self.values = []
        self.childs = [[None, None, None],
                       [None, None, None],
                       [None, None, None]]
        if create_cells:
            self.create_cells()

    def __repr__(self):
        return f'{self.__class__.__name__} at {self.position.get_position()}'

    def create_cells(self):
        for row in range(3):
            for column in range(3):
                # noinspection PyTypeChecker
                self.childs[row][column] = Cell(self, Position([column, row]))
        return True

    def get_cell(self, position):
        """Position as [ x, y ]"""
        return self.childs[position[1]][position[0]]


class MotherBoard:

    def __init__(self):
        self.childs = [[None, None, None],
                       [None, None, None],
                       [None, None, None]]

        self.row_values = [[0 for _ in range(9)] for _ in range(9)]
        self.row_possible_values = [[i for i in range(1, 10)] for _ in range(9)]
        self.board_values = [[0 for _ in range(9)] for _ in range(9)]
        self.column_possible_values = [[i for i in range(1, 10)] for _ in range(9)]

    def create_board(self):
        for row in range(3):
            for column in range(3):
                # noinspection PyTypeChecker
                self.childs[row][column] = MotherCell(self, Position([column, row]), True)
        return True

    def assign_values(self):
        # for offset, board_row in enumerate(self.childs):
        #     for cell_y in range(3):
        #         print(f'cell_y:{cell_y}')
        #         for mother in board_row:
        #             print(mother)
        #             if mother is None:
        #                 return False
        #             for cell_x in range(3):
        #                 print('row_values=', self.row_possible_values[cell_y + offset*3])
        #                 print(f'cell_x:{cell_x}')
        #                 for row1 in self.row_possible_values:
        #                     print(row1)
        #                 print('------------')
        #                 try:
        #                     x = random.randint(0, len(self.row_possible_values[cell_y + offset*3])-1)
        #                 except ValueError:
        #                     print(cell_y, cell_x)
        #                     continue
        #                 val = self.row_possible_values[cell_y + offset*3][x]
        #                 self.row_possible_values[cell_y + offset*3].remove(val)
        #                 self.row_values[cell_y + offset*3][x] = val
        #                 sleep(0.5)
        #                 print(f'value_set={self.row_values[cell_y + offset*3][x]}')
        #                 if val == 0 or self.row_values[cell_y + offset*3][x] == 0:
        #                     input(f'val={val}')
        #                 mother.get_cell([cell_x, cell_y]).set_value(val)
        # return True

        # for index, row in enumerate(self.row_possible_values):
        #     print('for loop', index)
        #     good = False
        #     random.shuffle(row)
        #     if index == 0:
        #         self.column_values[0] = copy.deepcopy(row)
        #     while not good:
        #         Break = False
        #         random.shuffle(row)
        #         next_column = []
        #         for col in range(len(self.column_values)):  ## implement in the right place
        #             for pile_size in range(1, index+1):
        #                 if row[col] == self.get_column_value(index-pile_size, col):
        #                     Break = True
        #                     break
        #             if not Break:
        #                 next_column.append(row[col])
        #         if not Break:
        #             print(next_column)
        #             for col in range(len(self.column_values)):  ## implement in the right place
        #                 self.column_values[index][col] = copy.deepcopy(next_column[col])
        #                 good = True
        #             print('good=True')
        # return self.column_values

        for index, row in enumerate(self.row_possible_values):
            for e in self.board_values:
                print(e)
            print('for loop', index)
            random.shuffle(row)
            if index == 0:
                print(row)
                self.board_values[0] = copy.deepcopy(row)
                for column in range(len(row)):
                    self.column_possible_values[column].remove(row[column])

            for column in range(0, 9):
                good = False
                while not good:
                    r_val = random.choice(copy.deepcopy(self.row_possible_values[index]))
                    if r_val in self.column_possible_values[column]:
                        good = True
                        # noinspection PyTypeChecker
                        self.board_values[index][column] = r_val
                        self.column_possible_values[column].remove(r_val)
                        self.row_possible_values[index].remove(r_val)
        return self.board_values

        #     while not good:
        #         Break = False
        #         random.shuffle(row)
        #         next_column = []
        #         for col in range(len(self.column_values)):
        #             for pile_size in range(1, index+1):
        #                 if row[col] == self.get_column_value(index-pile_size, col):
        #                     Break = True
        #                     break
        #             if not Break:
        #                 next_column.append(row[col])
        #         if not Break:
        #             print(next_column)
        #             for col in range(len(self.column_values)):  ## implement in the right place
        #                 self.column_values[index][col] = copy.deepcopy(next_column[col])
        #                 good = True
        #             print('good=True')
        # return self.column_values

    @cache
    def get_column_value(self, row, column):
        return self.board_values[row][column]

    def test_column_values(self):
        for column in range(9):
            line_used = []
            for row in range(9):
                if self.board_values[row][column] in line_used:
                    return False
                line_used.append(self.board_values[row][column])
        return True

    def print_value_board(self, type='row'):
        if type == 'row':
            for row in self.row_values:
                print(row)


if __name__ == '__main__':
    board = MotherBoard()
    print(board.create_board())
    board.assign_values()

    # board.print_value_board()
    for row1 in board.board_values:
        print(row1)
    print(board.test_column_values())

