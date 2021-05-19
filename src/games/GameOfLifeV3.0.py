import ctypes
import threading
import time
import tkinter as tk
import sys as system
import pygame as pg

from src import run_main
from src.resources.utils.Constants import Constants as Ct
from tkinter import messagebox


#####          STATIC METHODS          ####


def g_help():
    messagebox.showinfo(title="Help & Rules", message="Cliquer sur une case de la grille révèle:\n\n"
                                                      "- Une zone ne contenant aucune mine\n"
                                                      "- Une case bordée par 1, 2, 3 ou 4 mines dans un rayon d'1\n"
                                                      "  case (verticalement, horizontalement, diagonalement\n")


def about():
    """ Used to display an about messageBox """
    messagebox.showinfo(title="About", message="Made by: Jari \n "
                                               "Version: Alpha 2.0")


####                                  ####

class Game:

    def __init__(self):
        pg.init()
        self.root = pg.Surface((300, 300))
        self.screen = pg.display.set_mode((300, 300))
        pg.display.set_caption('Game Of Life V3')
        pg.display.flip()

        self.t1 = None
        self.playing = False
        self.placing = False

        self.square_dim = 10
        self.square_size = (10, 10)
        self.square_surface = pg.Surface(self.square_size)

        size = (50, 50)

        self.WHITE = pg.Color(255, 255, 255)
        self.GREY = pg.Color(100, 100, 100)
        self.RED = pg.Color(255, 0, 0)
        self.pos: list[int, int] = [20, 20]

        self.nb_columns = 50
        self.nb_lines = 50

        self.logic_board = {}
        self.test_dict = {}
        self.alive = {}
        self.to_kill = {}
        self.to_born = {}

        running = True

        self.init_lvl()

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    # if event.key == pg.K_LEFT:
                    #     self.pos[0] -= 5
                    # if event.key == pg.K_RIGHT:
                    #     self.pos[0] += 5
                    # if event.key == pg.K_UP:
                    #     self.pos[1] -= 5
                    # if event.key == pg.K_DOWN:
                    #     self.pos[1] += 5
                    if event.key == pg.K_RETURN:
                        self.playing = True if not self.playing else False
                        print('playing now enabled')
                    # self.draw_rect(tuple(self.pos), self.WHITE)
                elif event.type == pg.MOUSEBUTTONUP:
                    self.place(pg.mouse.get_pos())
                if self.playing:
                    self.round()
            #self.round()
            pg.display.update()

    def init_lvl(self):
        self.to_born = {}
        self.to_kill = {}
        self.alive = {}

        surface = pg.Surface((self.nb_columns*self.square_dim, self.nb_lines*self.square_dim))
        pg.draw.rect(surface, self.RED, surface.get_rect())
        self.screen.blit(surface, (0, 0))

        for y in range(1, self.nb_lines + 1):
            for x in range(1, self.nb_columns + 1):
                self.alive[x, y] = 0

    def place(self, pos):
        print(pos)
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

    def get_neighbours(self, col, line) -> int:
        min_column = col - 1 if col > 1 else col
        max_column = col + 1 if col < self.nb_columns else col

        min_line = line - 1 if line > 1 else line
        max_line = line + 1 if line < self.nb_lines else line

        ans = len([key for key in self.alive.keys() if ((self.alive[key] == 1)
                    & (min_line <= key[1] <= max_line)
                    & (min_column <= key[0] <= max_column))])

        if self.alive[col, line] == 1:
            ans -= 1

        return ans

    def update_dicts(self):
        for key in self.test_dict.keys():
            is_born = True if (self.test_dict.get(key) == 3 and (self.alive[key] == 0)) else False
            keeps_alive = True if ((self.test_dict.get(key) in [2, 3]) and self.alive[key] == 1) else False
            self.alive[key] = 1 if (is_born or keeps_alive) else 0
            if is_born:
                self.to_born[key] = 1
            dies = False if self.test_dict.get(key) in [2, 3] else True
            if dies:
                self.to_kill[key] = 1

    def round(self):
        self.to_born = {}
        self.to_kill = {}
        t1 = threading.Thread(target=self.half_t)
        t1.start()
        t2 = threading.Thread(target=self.half_t2)
        t2.start()
        t3 = threading.Thread(target=self.half_t3)
        t3.start()
        for y in range(1, self.nb_lines//4):
            for x in range(1, self.nb_columns + 1):
                self.test_dict[x, y] = self.get_neighbours(x, y)
        t1.join()
        t2.join()
        t3.join()
        self.update_dicts()
        self.update_gui()
            #time.sleep(self.time)

    def half_t(self):
        for y in range(self.nb_lines//4, self.nb_lines//4*2+1):
            for x in range(1, self.nb_columns + 1):
                self.test_dict[x, y] = self.get_neighbours(x, y)

    def half_t2(self):
        for y in range(self.nb_lines//4*2+1, self.nb_lines//4*3+1):
            for x in range(1, self.nb_columns + 1):
                self.test_dict[x, y] = self.get_neighbours(x, y)

    def half_t3(self):
        for y in range(self.nb_lines//4*3+1, self.nb_lines + 1):
            for x in range(1, self.nb_columns + 1):
                self.test_dict[x, y] = self.get_neighbours(x, y)

    def update_gui(self):
        tb_keys = self.to_born.keys()
        tk_keys = self.to_kill.keys()
        # for y in range(1, self.nb_lines + 1):
        #     for x in range(1, self.nb_columns + 1):
        #         if self.alive[x, y] == 1:
        #             self.draw_rect(((x-1) * self.square_dim, (y-1) * self.square_dim), self.WHITE)
        #         else:
        #             self.draw_rect(((x-1) * self.square_dim, (y-1) * self.square_dim), self.GREY)
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

    def create_menu(self, menubar: tk.Menu):
        menubar.add_command(label="Help", command=g_help)
        menubar.add_command(label="About", command=about)
        # menubar.add_command(label="Stats", command=self.stats)
        #menubar.add_command(label="Game Select Menu", command=lambda: [self.root.destroy(), run_main.run_main()])


if __name__ == '__main__':
    Game()
