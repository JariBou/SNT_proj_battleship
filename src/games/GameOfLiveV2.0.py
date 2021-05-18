import copy
import ctypes
from threading import Thread
import time
import tkinter as tk
import sys as system
import random
import pygame as pygame

from PIL.ImageTk import PhotoImage
from tkinter import messagebox

from src.resources.utils.Constants import Constants as Ct
from src import run_main


#####          STATIC METHODS          ####


def get_img(path):
    img = PhotoImage(file=path)
    return img


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
    nb_columns: int
    nb_lines: int
    nb_mines: int
    square_dim: int
    gap: int
    nb_seen_squares: int
    playing: bool

    def __init__(self):
        ## Window creation
        self.nb_columns, self.nb_lines = 10, 10
        self.change_grid_size()

        self.root = tk.Tk()
        self.root.title("GameOfLife - Alpha V2.0")
        self.root.protocol("WM_DELETE_WINDOW", self.exit_game)
        self.root.resizable(width=False, height=False)

        self.path = Ct.get_path()
        myappid = 'mjcorp.gameoflife.alphav2.0'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.root.iconbitmap(self.path.joinpath('resources\\images\\Demineur\\demineur_taskbar.ico'))

        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar, bg='white')
        self.create_menu(menubar)

        self.square_dim, self.gap = 30, 3
        self.playing = True
        self.placing = True
        self.time = 0.0

        self.t1: Thread = Thread()

        self.images = {
            'cross': get_img(self.path.joinpath('resources\\images\\Demineur\\croixj.gif')),
            'flag': get_img(self.path.joinpath('resources\\images\\Demineur\\drapeauj.gif')),
            'mine1': get_img(self.path.joinpath('resources\\images\\Demineur\\mine.png')),
            'minej': get_img(self.path.joinpath('resources\\images\\Demineur\\minej.gif'))
            }

        self.to_born: dict = {}
        self.to_kill: dict = {}
        self.alive: dict = {}

        self.land_canvas = tk.Canvas(self.root, width=(self.square_dim * self.nb_columns) + self.gap,
                                     height=(self.square_dim * self.nb_lines) + self.gap, bg='grey')
        self.land_canvas.bind("<Button-1>", self.pointeurG)
        # self.land_canvas.bind("<Button-3>", self.pointeurD)

        self.land_canvas.pack(side=tk.BOTTOM)

        self.w = tk.Scale(self.root, from_=0, to=2, orient=tk.HORIZONTAL, length=250, resolution=0.1, tickinterval=0.4,
                          label="Change Time between generations (s)")
        self.w['command'] = lambda w2=self.w: self.change_time(w2)
        self.w.set(0.0)
        self.w.pack(side=tk.TOP)

        self.start_button = tk.Button(self.root, text='Start', command=self.start)
        self.start_button.pack(side=tk.TOP)

        Ct.set_color(self.root, 'white')
        self.init_board()
        Ct.center(self.root)
        self.t1 = None
        self.test_dict = {}

        self.root.mainloop()

    def size(self, widget: tk.Entry, w: tk.Tk):
        values: list = widget.get().split('x')
        print(values)
        try:
            self.nb_columns = int(values[0])
            self.nb_lines = int(values[1])
        except (IndexError, ValueError):
            w.destroy()
            self.change_grid_size('Wrong input')
            return
        w.destroy()

    def draw_separators(self, ):
        x1 = self.gap
        y1 = self.gap
        y2 = y1 + (self.square_dim * self.nb_lines)
        x2 = x1 + (self.square_dim * self.nb_columns)
        for x in [x1 + self.square_dim * p for p in range(self.nb_columns + 1)]:
            self.land_canvas.create_line(x, y1, x, y2, width=2, fill='grey')
        for y in [y1 + self.square_dim * p for p in range(self.nb_lines + 1)]:
            self.land_canvas.create_line(x1, y, x2, y, width=2, fill='grey')

    def init_lvl(self):
        self.land_canvas.delete(tk.ALL)
        self.land_canvas.config(width=(self.square_dim * self.nb_columns) + self.gap,
                                height=(self.square_dim * self.nb_lines) + self.gap)
        self.draw_separators()

    def init_board(self):
        self.init_lvl()
        self.to_born = {}
        self.to_kill = {}
        self.alive = {}
        for y in range(1, self.nb_lines + 1):
            for x in range(1, self.nb_columns + 1):
                self.alive[x, y] = 0
                self.land_canvas.create_rectangle((x - 1) * self.square_dim + self.gap,
                                                  (y - 1) * self.square_dim + self.gap,
                                                  x * self.square_dim + self.gap, y * self.square_dim + self.gap,
                                                  width=0, fill='white')
        self.draw_separators()
        Ct.center(self.root)

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

    def pointeurG(self, event):
        if not self.placing:
            return
        nCol = (event.x - self.gap) // self.square_dim + 1
        nLine = (event.y - self.gap) // self.square_dim + 1
        if not (1 <= nCol <= self.nb_columns and 1 <= nLine <= self.nb_lines):
            return
        # si la cellule est vide:
        if self.alive[nCol, nLine] == 0:
            self.alive[nCol, nLine] = 1
            self.land_canvas.create_rectangle((nCol - 1) * self.square_dim + self.gap + self.gap / 2,
                                              (nLine - 1) * self.square_dim + self.gap + self.gap / 2,
                                              nCol * self.square_dim + self.gap - self.gap / 2,
                                              nLine * self.square_dim + self.gap - self.gap / 2,
                                              width=0, fill='black')
            # self.draw_separators()
        else:
            self.alive[nCol, nLine] = 0
            self.land_canvas.create_rectangle((nCol - 1) * self.square_dim + self.gap + self.gap / 2,
                                              (nLine - 1) * self.square_dim + self.gap + self.gap / 2,
                                              nCol * self.square_dim + self.gap - self.gap / 2,
                                              nLine * self.square_dim + self.gap - self.gap / 2,
                                              width=0, fill='white')
            # self.draw_separators()
            pass

    def start(self):
        self.t1 = Thread(target=self.round)
        self.playing = True
        self.placing = False
        self.t1.start()
        self.start_button.config(text='Pause', command=self.pause)

    def pause(self):
        self.playing = False
        self.placing = True
        self.start_button.config(text='Resume', command=self.start)

    def update_dicts(self):
        for key in self.test_dict.keys():
            is_born = True if (self.test_dict.get(key) == 3 and (self.alive[key] == 0)) else False
            keeps_alive = True if ((self.test_dict.get(key) in [2, 3]) and self.alive[key] == 1) else False
            dies = False if self.test_dict.get(key) in [2, 3] else True
            self.alive[key] = 1 if (is_born or keeps_alive) else 0
            if dies:
                self.to_kill[key] = 1
            elif is_born:
                self.to_born[key] = 1

    def update_dicts2(self):
        for key in self.to_born.keys():
            self.alive[key] = 1

        for key in self.to_kill.keys():
            self.alive[key] = 0

    def round(self):
        while self.playing:
            self.to_born = {}
            self.to_kill = {}
            for y in range(1, self.nb_lines + 1):
                if not self.playing:
                    return
                for x in range(1, self.nb_columns + 1):
                    if not self.playing:
                        return
                    # n = self.get_neighbours(x, y)
                    self.test_dict[x, y] = self.get_neighbours(x, y)
                    # if 3 < n < 2:
                    #     self.to_kill[x, y] = 1
                    # elif n == 3 and self.alive[x, y] == 0:
                    #     self.to_born[x, y] = 1

            self.update_dicts()
            self.update_gui2()
            time.sleep(self.time)

    def update_gui(self):
        for y in range(1, self.nb_lines + 1):
            for x in range(1, self.nb_columns + 1):
                self.land_canvas.create_rectangle((x - 1) * self.square_dim + self.gap + self.gap / 2,
                                                  (y - 1) * self.square_dim + self.gap + self.gap / 2,
                                                  x * self.square_dim + self.gap - self.gap / 2,
                                                  y * self.square_dim + self.gap - self.gap / 2,
                                                  width=0, fill=('black' if self.alive[x, y] == 1 else 'white'))

    def update_gui1(self):
        for y in range(self.nb_lines//2, self.nb_lines + 1):
            for x in range(1, self.nb_columns + 1):
                self.land_canvas.create_rectangle((x - 1) * self.square_dim + self.gap + self.gap / 2,
                                                  (y - 1) * self.square_dim + self.gap + self.gap / 2,
                                                  x * self.square_dim + self.gap - self.gap / 2,
                                                  y * self.square_dim + self.gap - self.gap / 2,
                                                  width=0, fill=('black' if self.alive[x, y] == 1 else 'white'))

    def update_gui2(self):
        for key in self.to_kill.keys():
            self.land_canvas.create_rectangle((key[0] - 1) * self.square_dim + self.gap + self.gap / 2,
                                              (key[1] - 1) * self.square_dim + self.gap + self.gap / 2,
                                              key[0] * self.square_dim + self.gap - self.gap / 2,
                                              key[1] * self.square_dim + self.gap - self.gap / 2,
                                              width=0, fill='white')
        for key in self.to_born.keys():
            self.land_canvas.create_rectangle((key[0] - 1) * self.square_dim + self.gap + self.gap / 2,
                                              (key[1] - 1) * self.square_dim + self.gap + self.gap / 2,
                                              key[0] * self.square_dim + self.gap - self.gap / 2,
                                              key[1] * self.square_dim + self.gap - self.gap / 2,
                                              width=0, fill='black')

    # def pointeurD(self, event):
    #     if not self.playing:
    #         return
    #     nCol = (event.x - self.gap) // self.square_dim + 1
    #     nLine = (event.y - self.gap) // self.square_dim + 1
    #     if not (1 <= nCol <= self.nb_columns and 1 <= nLine <= self.nb_lines):
    #         return
    #     self.land_canvas.create_rectangle((nCol - 1) * self.square_dim + self.gap,
    #                                       (nLine - 1) * self.square_dim + self.gap,
    #                                       nCol * self.square_dim + self.gap, nLine * self.square_dim + self.gap,
    #                                       width=0, fill='grey')
    #     if self.player_board[nCol, nLine] == "":
    #         self.land_canvas.create_image(nCol * self.square_dim - self.square_dim // 2 + self.gap,
    #                                       nLine * self.square_dim - self.square_dim // 2 + self.gap,
    #                                       image=self.images.get('flag'))
    #         self.player_board[nCol, nLine] = "d"
    #         self.nb_seen_squares += 1
    #         self.hidden_mines -= 1
    #         if self.has_won():
    #             self.won()
    #     elif self.player_board[nCol, nLine] == "d":
    #         self.land_canvas.create_text(nCol * self.square_dim - self.square_dim // 2 + self.gap,
    #                                      nLine * self.square_dim - self.square_dim // 2 + self.gap, text='?',
    #                                      fill='black', font='Arial 20')
    #         self.player_board[nCol, nLine] = "?"
    #         self.nb_seen_squares -= 1
    #         self.hidden_mines += 1
    #     elif self.player_board[nCol, nLine] == '?':
    #         self.player_board[nCol, nLine] = ""
    #     self.draw_separators(3)
    #     self.affiche_compteur()

    def exit_game(self):
        self.playing = False
        if self.t1 is not None:
            self.t1.join()
        time.sleep(1)
        system.exit('User cancelation')

    def create_menu(self, menubar: tk.Menu):
        menubar.add_command(label="Start", command=lambda: self.start())
        menubar.add_command(label="Help", command=g_help)
        menubar.add_command(label="About", command=about)
        # menubar.add_command(label="Stats", command=self.stats)
        menubar.add_command(label="Game Select Menu", command=lambda: [self.root.destroy(), run_main.run_main()])

    def change_time(self, w2):
        w2 = float(w2)
        self.time = w2

    def change_grid_size(self, additionnal_message: str = ''):
        if additionnal_message != '':
            additionnal_message = '       /!\\' + additionnal_message + '/!\\'
        size_choice = tk.Tk()
        size_choice.title("GameOfLife - Alpha V2.0")
        tk.Label(size_choice, text="Plese enter a grid size like this -> column_number x row_number").grid(row=0,
                                                                                                           column=0)
        tk.Label(size_choice, text="Example: 25x25" + additionnal_message).grid(row=1, column=0)
        entry = tk.Entry(size_choice)
        entry.grid(row=2, column=0)
        tk.Button(size_choice, text="Confirm", command=lambda: self.size(entry, size_choice)).grid(row=3, column=0)
        Ct.center(size_choice)
        entry.bind("<Return>", lambda event=None: self.press(event, entry, size_choice))
        size_choice.mainloop()

    def press(self, event, entry, window):
        print(event)
        self.size(entry, window)


if __name__ == '__main__':
    Game()
