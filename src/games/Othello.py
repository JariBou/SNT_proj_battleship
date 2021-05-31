import copy
import ctypes
import sys as system
import tkinter as tk
from time import sleep
from tkinter import messagebox
from typing import Optional, Union

from src.resources.utils.Constants import Constants as Ct, Position

from src import run_main

##### 3Hours challenge COMPLETE!!!!!


#####          STATIC METHODS          ####
# noinspection SpellCheckingInspection
def about():
    """ Used to display an about messageBox """
    messagebox.showinfo(title="About", message="Made by: Jari\n "
                                               "Version: Alpha V1.0")


def g_help():
    messagebox.showinfo(title="Help", message="Each piece played must be laid adjacent to an opponent's piece so that "
                                              "the opponent's piece or a row of opponent's pieces is flanked by the new "
                                              "piece and another piece of the player's colour. All of the opponent's pieces "
                                              "between these two pieces are 'captured' and turned over to match the player's colour.")

####                                  ####


class Game:

    def __init__(self):
        self.board_size = {'x': 8, 'y': 8}
        self.root = tk.Tk()
        self.root.title("Othello - Alpha V1.0")
        self.root.protocol("WM_DELETE_WINDOW", self.exit_game)
        ## Add Icon
        myappid = 'mjcorp.othello.alphav1.0'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.path = Ct.get_path()
        self.root.iconbitmap(self.path.joinpath('resources\\images\\Othello\\taskbar_ico.ico'))
        self.root.resizable(width=False, height=False)

        ## Create a Menubar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        self.create_menubar(menubar)

        self.b_class = Board()
        self.b_class.pass_board_to_pieces()
        board = self.b_class.board
        self.buttons_list = []
        self.player = 0
        self.colors = ['white', 'black']

        self.images = {'white': Ct.get_img(self.path.joinpath('resources\\images\\Othello\\othello_white.png'), size=35),
                       'black': Ct.get_img(self.path.joinpath('resources\\images\\Othello\\othello_black.png'), size=35)}

        for row in range(0, self.board_size['y']):
            self.root.rowconfigure(row, minsize=50)
            self.root.columnconfigure(row, minsize=50)
            for column in range(0, self.board_size['x']):
                print(row, column)
                a = tk.Button(self.root, bg='green', activebackground='lightblue')
                piece = board[row][column]
                print(piece)
                try:
                    a['image'] = self.images.get(piece.get_color())
                except AttributeError:
                    pass
                a["command"] = lambda a1=a: self.clicked(a1)
                a.grid(row=row, column=column, sticky='nsew')
                self.buttons_list.append(a)

        self.player_label = tk.Label(self.root, text='Player: 1 (white)')
        self.player_label.grid(row=0, column=self.board_size['x'])
        tk.Button(self.root, text='print_board', command=self.b_class.print_board).grid(row=1, column=self.board_size['x'])

        self.t1 = None
        self.playing = True

        Ct.center(self.root)
        self.root.mainloop()

    def clicked(self, button: tk.Button):
        curr_pos: Position = Position([button.grid_info()['column'], button.grid_info()['row']])
        positions = self.b_class.get_possible_places(self.colors[self.player])
        print(positions)
        if [button.grid_info()['column'], button.grid_info()['row']] in positions:
            self.b_class.place_piece(curr_pos, self.colors[self.player])
            self.switch_player()
            self.update_board()
        self.check_end()

    def check_end(self):
        positions = self.b_class.get_possible_places(self.colors[self.player])
        if not positions or self.b_class.is_full():
            self.over()

    def update_board(self):
        board: list[list[Optional[Piece]]] = self.b_class.return_board()
        for button in Ct.all_children(self.root, 'Button'):
            b = button.grid_info()
            if b['column'] > self.board_size['x'] - 1:
                return
            piece: Optional[Piece] = board[b['row']][b['column']]
            button['image'] = ''
            button['bg'] = 'green'
            if piece is not None:
                button['image'] = self.images.get(piece.get_color())

    def switch_player(self):
        self.player = abs(self.player-1)
        self.player_label.config(text=f'Player: {self.player + 1} ({self.colors[self.player]})')

    def exit_game(self):
        self.playing = False
        try:
            if self.t1 is not None:
                self.t1.join()
        except AttributeError:
            pass
        sleep(0.5)
        system.exit('User cancelation')

    def create_menubar(self, menubar: tk.Menu):
        menubar.add_command(label="Help", command=g_help)
        menubar.add_command(label="About", command=about)
        menubar.add_command(label='Play again', command=lambda: (self.root.destroy(), Game()))
        menubar.add_command(label="Game Select Menu", command=lambda: [self.root.destroy(), run_main.run_main()])

    def over(self):
        winner = self.colors.index(self.b_class.get_highest_color())
        messagebox.showinfo(f'Player {winner+1} won!', f'Player {winner+1} won! (the one that played {self.colors[winner]})')
        for button in Ct.all_children(self.root, 'Button'):
            b = button.grid_info()
            if b['column'] == self.board_size['x']:
                return
            button['command'] = ''


class Piece:

    def __init__(self, color: str, position: Union[list[int, int], Position]):
        self.color = color
        self.position = position if isinstance(position, Position) else Position(position)
        self.board: list[list[Optional['Piece']]] = []

    def __repr__(self):
        return f'{self.__class__.__name__}(color={self.color}, position={self.position.get_position()}'

    def get_position(self, coordinates=False) -> Union[Position, list[int, int]]:
        """If coordinates is True returns a list[int, int] of the position instead of the <Position> class"""
        return self.position if not coordinates else self.position.get_position()

    def get_color(self) -> str:
        return self.color

    def pass_new_board(self, board: list[list[Optional['Piece']]]):
        self.board = board

    def turn_pieces(self):
        print('turning pieces')
        offsets = [[1, -1], [1, 0], [1, 1], [0, 1]]
        x, y = self.position.get_position()
        for i in [1, -1]:
            for offset in offsets:
                try:
                    pos = self.board[y + offset[0] * i][x + offset[1] * i]
                    if isinstance(pos, Piece) and pos.get_color() != self.get_color():
                        pos_2 = self.board[y + offset[0] * i * 2][x + offset[1] * i * 2]
                        if isinstance(pos_2, Piece) and pos_2.get_color() == self.get_color():
                            self.board[y + offset[0] * i][x + offset[1] * i] = Piece(self.get_color(), copy.deepcopy(pos.get_position()))
                except IndexError:
                    pass

    def get_turning_spots(self) -> list[list[int, int]]:
        offsets = [[1, -1], [1, 0], [1, 1], [0, 1]]
        x, y = self.position.get_position()
        possible_spots = []
        for i in [1, -1]:
            for offset in offsets:
                try:
                    pos = self.board[y + (offset[0] * i)][x + (offset[1] * i)]
                    if isinstance(pos, Piece) and pos.get_color() != self.get_color() and y + (offset[0] * i) >= 0 and x + (offset[1] * i) >= 0:
                        pos_2 = self.board[y + (offset[0] * i) * 2][x + (offset[1] * i) * 2]
                        if pos_2 is None and x + (offset[1] * i) * 2 >= 0 and y + (offset[0] * i) * 2 >= 0:
                            possible_spots.append([x + (offset[1] * i) * 2, y + (offset[0] * i) * 2])
                except IndexError:
                    continue
        return possible_spots


class Board:

    def __init__(self):
        self.colors = ['White', 'Black']
        self.checks_list = {'White': False, 'Black': False}
        self.player = 0
        self.board: list[list[Optional[Piece]]] = [[None]*8,
                                                   [None]*8,
                                                   [None]*8,
                                                   [None, None, None, Piece('white', [3, 3]), Piece('black', [4, 3]), None, None, None],
                                                   [None, None, None, Piece('black', [3, 4]), Piece('white', [4, 4]), None, None, None],
                                                   [None]*8,
                                                   [None]*8,
                                                   [None]*8]

    def get(self, x: int, y: int) -> Optional['Piece']:
        print(f'getting at: {x, y}    -  element: {self.board[y][x]}')
        return self.board[y][x]

    def pass_board_to_pieces(self):
        for row in range(len(self.board)):
            for element in [e for e in self.board[row] if e is not None]:
                element.pass_new_board(self.board)

    def switch_player(self):
        self.player = 1 if self.player == 0 else 0

    def return_board(self) -> list[list[Optional['Piece']]]:
        return self.board

    def set_board(self, board: list[list[Optional['Piece']]]):
        self.board = board

    def place_piece(self, position: Union[Position, list[int, int]], color: str) -> bool:
        print('Trying to place piece')
        if self.board[position.y][position.x] is not None:
            return False
        else:
            piece = Piece(color, copy.deepcopy(position))
            self.board[position.y][position.x] = piece
            piece.pass_new_board(self.board)
            piece.turn_pieces()
            self.pass_board_to_pieces()
            return True

    def get_pieces(self, color: str):
        pieces = []
        for element in Ct.get_flattened(self.board):
            if element is not None and element.get_color() == color:
                pieces.append(element)
        return pieces

    def print_board(self):
        for row in self.board:
            print(row)

    def get_possible_places(self, color: str) -> list[list[int, int]]:
        pieces = self.get_pieces(color)
        places = []
        for piece in pieces:
            spots = piece.get_turning_spots()
            if spots:
                places += spots
        Ct.remove_duplicates(places)
        return places if places != [] else False

    def get_highest_color(self) -> str:
        colors_dict = {'white': 0, 'black': 0}
        for element in [piece for piece in Ct.get_flattened(self.board) if piece is not None]:
            colors_dict[element.get_color()] += 1
        colors_dict = {key: value for key, value in sorted(colors_dict.items(), key=lambda item: item[1], reverse=True)}
        return [key for key in colors_dict.keys()][0]

    def is_full(self):
        return not Ct.get_flattened(self.board).__contains__(None)


if __name__ == '__main__':
    Game()
