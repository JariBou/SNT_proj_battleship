import time
import tkinter as tk
import sys as system
from random import randint

import pygame as pg

from src import run_main
from src.resources.utils.Constants import Constants as Ct
from tkinter import messagebox

##TODO: add settings panel to switch game
#####          STATIC METHODS          ####


def g_help():
    messagebox.showinfo(title="Help & Rules", message="Cliquer sur une case de la grille révèle:\n\n"
                                                      "- Une zone ne contenant aucune mine\n"
                                                      "- Une case bordée par 1, 2, 3 ou 4 mines dans un rayon d'1\n"
                                                      "  case (verticalement, horizontalement, diagonalement\n")


def about():
    """ Used to display an about messageBox """
    messagebox.showinfo(title="About", message="Made by: Jari \n "
                                               "Version: Alpha 3.0")


####                                  ####

def create_menu(menubar: tk.Menu):
    menubar.add_command(label="Help", command=g_help)
    menubar.add_command(label="About", command=about)
    # menubar.add_command(label="Stats", command=self.stats)
    #menubar.add_command(label="Game Select Menu", command=lambda: [self.root.destroy(), run_main.run_main()])


class Game:

    def __init__(self):
        self.alive: dict = {}
        self.GREY = pg.Color(100, 100, 100)

        self.nb_columns = 20
        self.nb_lines = 20
        self.square_dim = 10
        self.square_size = (self.square_dim, self.square_dim)
        self.square_surface = pg.Surface(self.square_size)
        self.root = pg.Surface((self.nb_columns * self.square_dim, self.nb_lines * self.square_dim))
        self.screen = pg.display.set_mode((self.nb_columns * self.square_dim, self.nb_lines * self.square_dim))
        pg.display.set_caption('Game Of Life V3 - idle')
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
        self.pos: list[int, int] = [20, 20]

        self.test_dict: dict = {}
        self.to_kill: dict = {}
        self.to_born: dict = {}

        running = True
        self.time = 0.05
        self.percentage = 10

        self.init_lvl()

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.playing = True if not self.playing else False
                        print('playing now enabled' if self.playing else 'playing now disabled')
                        pg.display.set_caption(f'Game Of Life V3 - {"running" if self.playing else "idle"}')
                    if event.key == pg.K_r:
                        self.randomize()
                    if event.key == pg.K_c:
                        self.clear_board()
                    if event.key == pg.K_a:
                        self.time = 0
                    if event.key == pg.K_z:
                        self.time = 0.025
                    if event.key == pg.K_e:
                        self.time = 0.05
                    if event.key == pg.K_q:
                        self.time = 0.1
                    if event.key == pg.K_h:
                        self.settings()
                elif event.type == pg.MOUSEBUTTONUP:
                    self.place(pg.mouse.get_pos())
            if self.playing:
                self.round()
            pg.display.update()

    def set_time(self, x: float):
        self.time = x

    def init_lvl(self):
        self.to_born = {}
        self.to_kill = {}
        self.alive = {}

        surface = pg.Surface((self.nb_columns*self.square_dim, self.nb_lines*self.square_dim))
        pg.draw.rect(surface, self.GREY, surface.get_rect())
        self.screen.blit(surface, (0, 0))

        for y in range(1, self.nb_lines + 1):
            for x in range(1, self.nb_columns + 1):
                self.alive[x, y] = 0

    def place(self, pos):
        nCol = (pos[0]+1) // self.square_dim + 1
        nLine = (pos[1]+1) // self.square_dim + 1
        col = (nCol - 1) * self.square_dim
        line = (nLine - 1) * self.square_dim
        if self.alive[nCol, nLine] == 0:
            self.alive[nCol, nLine] = 1
            self.draw_rect((col, line), self.WHITE)
        else:
            self.alive[nCol, nLine] = 0
            self.draw_rect((col, line), self.GREY)

    def randomize(self):
        print('randomizing')
        for x in range(1, self.nb_columns+1):
            for y in range(1, self.nb_lines+1):
                rand = randint(0, 100)
                if rand <= self.percentage:
                    self.alive[x, y] = 1
                    self.draw_rect(((x - 1) * self.square_dim, (y - 1) * self.square_dim), self.WHITE)
        print('done')

    def clear_board(self):
        print('playing now disabled - clearing...')
        self.playing = False
        pg.display.set_caption(f'Game Of Life V3 - idle')
        for x in range(1, self.nb_columns+1):
            for y in range(1, self.nb_lines+1):
                self.alive[x, y] = 0
                self.draw_rect(((x - 1) * self.square_dim, (y - 1) * self.square_dim), self.GREY)
        print('>done')

    def get_neighbours(self, col: int, line: int) -> int:
        min_column = col - 1 if col > 1 else col
        max_column = col + 1 if col < self.nb_columns else col

        min_line = line - 1 if line > 1 else line
        max_line = line + 1 if line < self.nb_lines else line

        ans = -1 if self.alive[col, line] == 1 else 0
        for col in range(min_column, max_column + 1):
            for line in range(min_line, max_line + 1):
                if self.alive[col, line] == 1:
                    ans += 1
        return ans

    def update_dicts(self):
        for key in self.test_dict.keys():
            is_born = True if (self.test_dict.get(key) == 3 and (self.alive[key] == 0)) else False
            if is_born:
                self.draw_rect(((key[0] - 1) * self.square_dim, (key[1] - 1) * self.square_dim), self.WHITE)
            dies = False if (self.test_dict.get(key) in [2, 3]) or (self.alive[key] == 0) else True
            self.alive[key] = 1 if (is_born or ((self.test_dict.get(key) in [2, 3]) and self.alive[key] == 1)) else 0
            if dies:
                self.draw_rect(((key[0] - 1) * self.square_dim, (key[1] - 1) * self.square_dim), self.GREY)

    def round(self):
        for y in range(1, self.nb_lines + 1):
            for x in range(1, self.nb_columns + 1):
                self.test_dict[x, y] = self.get_neighbours(x, y)
        self.update_dicts()
        time.sleep(self.time)

    def update_gui(self):
        for place in self.to_born.keys():
            self.draw_rect(((place[0] - 1) * self.square_dim, (place[1] - 1) * self.square_dim), self.WHITE)
        for place in self.to_kill.keys():
            self.draw_rect(((place[0] - 1) * self.square_dim, (place[1] - 1) * self.square_dim), self.GREY)

    def exit_game(self):
        self.playing = False
        if self.t1 is not None:
            self.t1.join()
        time.sleep(1)
        system.exit('User cancelation')

    def draw_rect(self, position: tuple[int, int], color: pg.Color):
        pg.draw.rect(self.square_surface, color, self.square_surface.get_rect())
        self.screen.blit(self.square_surface, position)

    def change_rand_menu(self, window: tk.Tk):
        tk.Label(window, text=f"Enter a percentage between 1 and 99 included: (curr: {self.percentage})").pack()
        entry = tk.Entry(window)
        entry.pack()
        tk.Button(window, text="Confirm", command=lambda: self.change_rand_val(entry, window)).pack()

    def change_rand_val(self, entry: tk.Entry, w: tk.Tk):
        val = entry.get()
        entry.delete(0, len(val))
        if not (0 < int(val) < 100):
            entry.insert(0, 'wrong range')
            return
        entry.insert(0, f'Updated to: {val}')
        self.percentage = int(val)
        w.destroy()
        self.settings()

    def change_sizes(self, nCol: int, nLine: int, square_dim: int):
        self.clear_board()
        self.nb_columns = nCol
        self.nb_lines = nLine
        self.square_dim = square_dim
        self.square_size = (self.square_dim, self.square_dim)
        self.square_surface = pg.Surface(self.square_size)
        self.root = pg.Surface((self.nb_columns * self.square_dim, self.nb_lines * self.square_dim))
        self.screen = pg.display.set_mode((self.nb_columns * self.square_dim, self.nb_lines * self.square_dim))
        pg.display.set_caption('Game Of Life V3')
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
        self.change_rand_menu(root)
        self.change_size_menu(root)
        tk.Button(root, text='Done', command=lambda: root.destroy()).pack()
        Ct.center(root)
        root.mainloop()


if __name__ == '__main__':
    Game()
