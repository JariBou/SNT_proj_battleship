import tkinter as tk
from PIL import Image, ImageTk
from time import sleep, time

from src.resources.utils.Constants import Constants as Ct
path = Ct.get_path()
#button_load = Image.open(path.joinpath('resources\\images\\Chess\\taskbar.png'))


class Board:

    def __init__(self):
        self.board = Ct.new_board()


class Game:

    def __init__(self):
        self.b_class = Board()
        self.board = self.b_class.board

    def get_class(self):
        return self.b_class


if __name__ == '__main__':
    g = Game()
    g.board[0][0] = 1
    for element in g.get_class().board:
        print(element)
    print('---------')
    for element in g.board:
        print(element)
