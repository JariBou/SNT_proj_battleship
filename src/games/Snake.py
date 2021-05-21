import ctypes
import threading
import time
import tkinter as tk
import sys as system
from random import randint, random

import pygame as pg

from src import run_main
from src.resources.utils.Constants import Constants as Ct
from tkinter import messagebox


#####          STATIC METHODS          ####


def g_help():
    messagebox.showinfo(title="Help & Rules", message="Cliquer sur une case de la grille révèle:\n\n"
                                                      "- Une zone ne contenant aucune mine\n"
                                                      "- Une case bordée par 1, 2, 3 ou 4 mines dans un rayon d'1\n"
                                                      "  case (verticalement, horizontalement, diagonalement\n")   ##TODO: change help func


def about():
    """ Used to display an about messageBox """
    messagebox.showinfo(title="About", message="Made by: Jari \n "
                                               "Version: Alpha 1.0")


####                                  ####

def create_menu(menubar: tk.Menu):
    menubar.add_command(label="Help", command=g_help)
    menubar.add_command(label="About", command=about)
    # menubar.add_command(label="Stats", command=self.stats)
    #menubar.add_command(label="Game Select Menu", command=lambda: [self.root.destroy(), run_main.run_main()])


class Game:

    def __init__(self):
        self.GREY = pg.Color(100, 100, 100)

        self.cpt = 0
        self.nb_columns = 20
        self.nb_lines = 20
        self.square_dim = 10
        self.square_size = (self.square_dim, self.square_dim)
        self.square_surface = pg.Surface(self.square_size)
        self.root = pg.Surface((self.nb_columns * self.square_dim, self.nb_lines * self.square_dim))
        self.screen = pg.display.set_mode((self.nb_columns * self.square_dim, self.nb_lines * self.square_dim))
        pg.display.set_caption('Snake')
        pg.display.flip()
        root = tk.Tk()
        root.title('Select size')
        self.change_size_menu(root, True)
        Ct.center(root)
        root.mainloop()
        pg.init()

        self.t1 = None
        self.playing = False

        self.WHITE = pg.Color(255, 255, 255)
        self.RED = pg.Color(255, 0, 0)
        self.BCOL = pg.Color(255, 0, 255)
        self.pos: list[int, int] = [20, 20]

        self.apple: list[int, int] = [0, 0]
        self.bapple: list[int, int] = [0, 0]
        self.snake: list[list[int, int]] = [[9, 5], [8, 5], [7, 5], [6, 5], [5, 5], [4, 5]]

        running = True
        self.time = 0.075
        self.down = False
        self.up = False
        self.left = False
        self.right = True
        self.has_apple = False
        self.has_bapple = False
        self.walls: dict = {}

        self.init_lvl()

        self.draw_snake()

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.playing = True if not self.playing else False
                        print('playing now enabled' if self.playing else 'playing now disabled')
                        if self.playing:
                            threading.Thread(target=self.round).start()
                    if event.key == pg.K_h:
                        self.settings()
                    if event.key == pg.K_DOWN:
                        self.switch_direction('down')
                    if event.key == pg.K_UP:
                        self.switch_direction('up')
                    if event.key == pg.K_RIGHT:
                        self.switch_direction('right')
                    if event.key == pg.K_LEFT:
                        self.switch_direction('left')
            #if self.playing:
            #    threading.Thread(target=self.round).start()
                #self.round()   # Put in a separated thread do avoid problems with reaction speed
            pg.display.update()

    def set_time(self, x: float):
        self.time = x

    def init_lvl(self):
        self.apple = [randint(0, self.nb_columns), randint(0, self.nb_lines)]

        surface = pg.Surface((self.nb_columns*self.square_dim, self.nb_lines*self.square_dim))
        pg.draw.rect(surface, self.GREY, surface.get_rect())
        self.screen.blit(surface, (0, 0))

    def switch_direction(self, direction):
        if direction == 'right' and not self.left:
            self.up, self.down, self.left, self.right = False, False, False, True
        elif direction == 'left' and not self.right:
            self.up, self.down, self.left, self.right = False, False, True, False
        elif direction == 'up' and not self.down:
            self.up, self.down, self.left, self.right = True, False, False, False
        elif direction == 'down' and not self.up:
            self.up, self.down, self.left, self.right = False, True, False, False

    def place_apple(self):
        x = randint(1, self.nb_columns)
        y = randint(1, self.nb_columns)
        if [x, y] in self.snake:
            self.place_apple()
        else:
            self.apple = [x, y]
            line = (y - 1) * self.square_dim
            col = (x - 1) * self.square_dim
            self.draw_rect((col, line), self.RED)
            self.has_apple = True

    def place_bad_apple(self):
        x = randint(1, self.nb_columns)
        y = randint(1, self.nb_columns)
        if [x, y] in self.snake:
            self.place_bad_apple()
        else:
            self.bapple = [x, y]
            line = (y - 1) * self.square_dim
            col = (x - 1) * self.square_dim
            self.draw_rect((col, line), self.BCOL)
            self.has_bapple = True

    def draw_snake(self):
        for position in self.snake:
            col = (position[0] - 1) * self.square_dim
            line = (position[1] - 1) * self.square_dim
            self.draw_rect((col, line), self.WHITE)

    def draw_next_snake(self, next_pos):
        if next_pos in self.snake:
            self.playing = False
            return
        if next_pos == self.bapple:
            old = self.snake.pop()
            self.has_bapple = False
            col = (old[0] - 1) * self.square_dim
            line = (old[1] - 1) * self.square_dim
            self.draw_rect((col, line), self.GREY)
        if next_pos == self.apple:
            self.cpt += 1
            if self.cpt == 1:
                print(f'{self.cpt} apple eaten')
            else:
                print(f'{self.cpt} apples grallées')
            self.has_apple = False
            if self.time >= 0.0075:
                self.time -= 0.0075
        if next_pos != self.apple:
            old = self.snake.pop()
            col = (old[0] - 1) * self.square_dim
            line = (old[1] - 1) * self.square_dim
            self.draw_rect((col, line), self.GREY)
        self.snake.insert(0, next_pos)
        for position in self.snake:
            col = (position[0] - 1) * self.square_dim
            line = (position[1] - 1) * self.square_dim
            self.draw_rect((col, line), self.WHITE)

    def clear_board(self):
        for x in range(1, self.nb_columns+1):
            for y in range(1, self.nb_lines+1):
                self.draw_rect(((x - 1) * self.square_dim, (y - 1) * self.square_dim), self.GREY)

    def place_wall(self):
        size = randint(1, 7)
        #          east    north    west    south
        facing = [[1, 0], [0, 1], [-1, 0], [0, -1]][randint(0, 5)]
        for i in range(size):
            x = randint(1, self.nb_columns+1)
            y = randint(1, self.nb_lines+1)
        #self.walls

    def round(self):
        while self.playing:
            if not self.has_apple:
                self.place_apple()
            if not self.has_bapple:
                self.place_bad_apple()
            x_off = 1 if self.right else (-1 if self.left else 0)
            y_off = -1 if self.up else (1 if self.down else 0)
            x = self.snake[0][0] + x_off
            y = self.snake[0][1] + y_off
            # if x == 0:
            #     x = self.nb_columns
            # elif x == self.nb_columns+1:
            #     x = 1
            #
            # if y == 0:
            #     y = self.nb_lines
            # elif y == self.nb_lines+1:
            #     y = 1

            if x == 0 or x == self.nb_columns + 1:
                x = (self.nb_columns if x == 0 else 1)
            if y == 0 or y == self.nb_lines + 1:
                y = (self.nb_lines if y == 0 else 1)
            self.draw_next_snake([x, y])
            time.sleep(self.time)

    def exit_game(self):
        self.playing = False
        if self.t1 is not None:
            self.t1.join()
        time.sleep(1)
        system.exit('User cancelation')

    def draw_rect(self, position: tuple[int, int], color: pg.Color):
        pg.draw.rect(self.square_surface, color, self.square_surface.get_rect())
        self.screen.blit(self.square_surface, position)

    def change_sizes(self, nCol: int, nLine: int, square_dim: int):
        self.clear_board()
        self.nb_columns = nCol
        self.nb_lines = nLine
        self.square_dim = square_dim
        self.square_size = (self.square_dim, self.square_dim)
        self.square_surface = pg.Surface(self.square_size)
        self.root = pg.Surface((self.nb_columns * self.square_dim, self.nb_lines * self.square_dim))
        self.screen = pg.display.set_mode((self.nb_columns * self.square_dim, self.nb_lines * self.square_dim))
        pg.display.set_caption('Snake')
        pg.display.flip()
        self.init_lvl()

    def change_size_menu(self, window, start=False):
        tk.Label(window, text="Enter new dimensions as nColxnLine+squareSide").pack()
        tk.Label(window, text=f"Current size: {self.nb_columns}x{self.nb_lines}+{self.square_dim}").pack()
        entry = tk.Entry(window)
        entry.pack()
        if not start:
            tk.Button(window, text="Confirm", command=lambda: self.change_size_val(entry)).pack()
        else:
            tk.Button(window, text="Confirm", command=lambda: self.change_size_val(entry, window, True)).pack()

    def change_size_val(self, entry: tk.Entry, window=None, first=False):
        string = entry.get()
        vals = string.split('+')
        squareDim = int(vals.pop())
        nCol, nLine = vals[0].split('x')
        self.change_sizes(int(nCol), int(nLine), squareDim)
        window.destroy()
        if not first:
            self.settings()

    def settings(self):
        root = tk.Tk()
        root.title('Help')
        self.change_size_menu(root)
        tk.Button(root, text='Done', command=lambda: root.destroy()).pack()
        Ct.center(root)
        root.mainloop()


if __name__ == '__main__':
    Game()
