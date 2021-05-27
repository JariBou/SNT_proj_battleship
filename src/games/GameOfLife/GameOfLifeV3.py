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
    messagebox.showinfo(title="Help & Rules",
                        message="Une cellule possède huit voisins, qui sont les cellules adjacentes horizontalement, verticalement et diagonalement.\n\n"
                                "À chaque étape, l’évolution d’une cellule est déterminée par l’état de ses huit voisines de la façon suivante :\n\n"
                                "* Une cellule morte possédant exactement trois voisines vivantes devient vivante (elle naît)\n"
                                "* une cellule vivante possédant deux ou trois voisines vivantes le reste, sinon elle meurt\n"
                                "\n Cliquez sur l'écran pour placer ou tuer une cellule")


def about():
    """ Used to display an about messageBox """
    messagebox.showinfo(title="About", message="Made by: Jari \n "
                                               "Version: Alpha 3.0")


####                                  ####

def create_menu(menubar: tk.Menu):
    menubar.add_command(label="Help", command=g_help)
    menubar.add_command(label="About", command=about)
    # menubar.add_command(label="Stats", command=self.stats)
    # menubar.add_command(label="Game Select Menu", command=lambda: [self.root.destroy(), run_main.run_main()])


class Game:

    def __init__(self, **kwargs):
        self.alive: dict = {}
        self.GREY = pg.Color(100, 100, 100)
        self.BLACK = pg.Color(0, 0, 0)
        self.WHITE = pg.Color(255, 255, 255)
        self.RED = pg.Color(255, 0, 0)

        self.bg_color = self.BLACK
        self.cell_color = self.WHITE
        self.nb_columns = kwargs.get('nb_columns', 30)
        self.nb_lines = kwargs.get('nb_lines', 3)
        self.square_dim = kwargs.get('square_size', 10)
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

        self.pos: list[int, int] = [20, 20]

        self.test_dict: dict = {}
        self.to_kill: dict = {}
        self.to_born: dict = {}

        running = True
        self.time = 0.05
        self.percentage = 10

        self.init_lvl()
        master = tk.Tk()  ## So that a new Tk window isn't created when you use g_help()
        master.withdraw()
        g_help()

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
                    if event.key == pg.K_UP:
                        self.change_speed(0.01)
                    if event.key == pg.K_DOWN:
                        self.change_speed(-0.01)
                elif event.type == pg.MOUSEBUTTONUP:
                    self.place(pg.mouse.get_pos())
            if self.playing:
                self.round()
            pg.display.update()

    def set_time(self, x: float):
        self.time = x

    def change_speed(self, amount: float):
        if str(amount)[0] == '-':
            self.time += abs(amount)
        elif self.time >= abs(amount):
            self.time -= amount

    def init_lvl(self):
        self.to_born = {}
        self.to_kill = {}
        self.alive = {}

        self.screen.fill(self.bg_color)

        for y in range(1, self.nb_lines + 1):
            for x in range(1, self.nb_columns + 1):
                self.alive[x, y] = 0

    def place(self, pos):
        nCol = (pos[0] + 1) // self.square_dim + 1
        nLine = (pos[1] + 1) // self.square_dim + 1
        col = (nCol - 1) * self.square_dim
        line = (nLine - 1) * self.square_dim
        if self.alive[nCol, nLine] == 0:
            self.alive[nCol, nLine] = 1
            self.draw_rect((col, line), self.cell_color)
        else:
            self.alive[nCol, nLine] = 0
            self.draw_rect((col, line), self.bg_color)

    def randomize(self):
        print('randomizing')
        for x in range(1, self.nb_columns + 1):
            for y in range(1, self.nb_lines + 1):
                rand = randint(0, 100)
                if rand <= self.percentage:
                    self.alive[x, y] = 1
                    self.draw_rect(((x - 1) * self.square_dim, (y - 1) * self.square_dim), self.cell_color)
        print('done')

    def clear_board(self):
        print('playing now disabled - clearing...')
        self.playing = False
        pg.display.set_caption(f'Game Of Life V3 - idle')
        for x in range(1, self.nb_columns + 1):
            for y in range(1, self.nb_lines + 1):
                self.alive[x, y] = 0
                self.draw_rect(((x - 1) * self.square_dim, (y - 1) * self.square_dim), self.bg_color)
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
                self.draw_rect(((key[0] - 1) * self.square_dim, (key[1] - 1) * self.square_dim), self.cell_color)
            dies = False if (self.test_dict.get(key) in [2, 3]) or (self.alive[key] == 0) else True
            self.alive[key] = 1 if (is_born or ((self.test_dict.get(key) in [2, 3]) and self.alive[key] == 1)) else 0
            if dies:
                self.draw_rect(((key[0] - 1) * self.square_dim, (key[1] - 1) * self.square_dim), self.bg_color)

    def round(self):
        for y in range(1, self.nb_lines + 1):
            for x in range(1, self.nb_columns + 1):
                self.test_dict[x, y] = self.get_neighbours(x, y)
        self.update_dicts()
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
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        create_menu(menubar)
        tk.Button(root, text='Done', command=lambda: root.destroy()).pack()
        Ct.center(root)
        root.mainloop()


import ctypes
import threading
import tkinter as tk
from PIL.ImageTk import PhotoImage
from tkinter import font as ft, messagebox
from typing import Union
from src.resources.utils.Constants import Constants
from src import run_main


#####          STATIC METHODS          ####
def aboutL():
    """ Used to display an about messageBox """
    messagebox.showinfo(title="About", message="Made by: Jari & Mathis \n "
                                               "Version: Alpha 1.2")


####                                  ####


class Launcher:

    def __init__(self):
        self.w = tk.Tk()
        self.w.title("Snake Launcher")
        menubar = tk.Menu(self.w)
        self.w.config(menu=menubar)
        self.create_menu(menubar)
        myappid = 'mjcorp.snake.alphav1.2'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.path = Constants.get_path()
        self.w.iconbitmap(self.path.joinpath('resources\\images\\snake\\snake.ico'))

        self.rando = tk.IntVar(value=30)
        self.speed = tk.DoubleVar(value=0.075)
        self.columns = tk.IntVar(value=30)
        self.lines = tk.IntVar(value=30)
        self.square_size = tk.IntVar(value=10)

        customFont = ft.Font(family='Source Sans Pro Black', size=17)
        self.running = True
        imgs = {'logo': PhotoImage(file=self.path.joinpath('resources\\images\\GoL\\GoL_icon.png'))}

        tk.Label(self.w, text='Snake', image=imgs['logo'], font=customFont).grid(row=0, column=1, sticky='n')

        self.args_frame = tk.Frame(self.w)
        tk.Label(self.args_frame, text='--Args--', font=customFont).grid(row=0, column=0, columnspan=2, sticky='n')
        tk.Label(self.args_frame, text='Random percentage', font=customFont, anchor='w').grid(row=1, column=0,
                                                                                              sticky='w')
        tk.Label(self.args_frame, text='Base speed(advanced)', font=customFont, anchor='w').grid(row=2, column=0,
                                                                                                 sticky='w')
        self.rentry = tk.Entry(self.args_frame, font=customFont, textvariable=self.rando, state=tk.DISABLED)
        self.rentry.grid(row=1, column=1)
        tk.Entry(self.args_frame, font=customFont, textvariable=self.speed).grid(row=2, column=1)

        size_frame = tk.Frame(self.w)
        tk.Label(size_frame, text='Size:', font=customFont, anchor='w').grid(row=0, column=0, sticky='w')
        tk.Label(size_frame, text='columns: ', font=customFont, anchor='w').grid(row=1, column=0, sticky='w')
        tk.Entry(size_frame, textvariable=self.columns, font=customFont).grid(row=1, column=1)
        tk.Label(size_frame, text='lines: ', font=customFont, anchor='w').grid(row=2, column=0, sticky='w')
        tk.Entry(size_frame, textvariable=self.lines, font=customFont).grid(row=2, column=1)
        tk.Label(size_frame, text='square length: ', font=customFont, anchor='w').grid(row=3, column=0, sticky='w')
        tk.Entry(size_frame, textvariable=self.square_size, font=customFont).grid(row=3, column=1)
        size_frame.grid(row=2, column=0, columnspan=4)

        tk.Button(self.w, text='Open snake',
                  command=self.snakeuh, font=customFont, relief=tk.RAISED, border=10).grid(row=5, column=0,
                                                                                           columnspan=2)

        self.t1 = threading.Thread(target=self.loop)
        self.t1.start()

        ### pas du tout Ctrl + C  Ctrl + V
        self.color_frame = tk.Frame(self.w)
        self.color_var = tk.StringVar()
        self.color_var.set('modern')
        tk.Label(self.color_frame, text='--Colors--', font=customFont).pack(anchor='n', padx=30)
        radio1 = tk.Radiobutton(self.color_frame, text='Modern', font=customFont, variable=self.color_var,
                                value='modern')
        radio1.pack(anchor='nw', padx=30)
        radio2 = tk.Radiobutton(self.color_frame, text='Vintage', font=customFont, variable=self.color_var,
                                value='vintage')
        radio2.pack(anchor='nw', padx=30)
        radio3 = tk.Radiobutton(self.color_frame, text='Floor is lava', font=customFont, variable=self.color_var,
                                value='floorislava')
        radio3.pack(anchor='nw', padx=30)
        radio4 = tk.Radiobutton(self.color_frame, text='Ocean', font=customFont, variable=self.color_var,
                                value='ocean')
        radio4.pack(anchor='nw', padx=30)
        radio5 = tk.Radiobutton(self.color_frame, text='Outerworld', font=customFont,
                                variable=self.color_var, value='outerworld')
        radio5.pack(anchor='nw', padx=30)

        self.color_frame.grid(row=1, column=1)
        from src.resources.utils.Constants import Constants as Ct

        Ct.center(self.w)

        self.w.mainloop()

    def loop(self):
        while self.running:
            self.bentry.config(state=(tk.NORMAL if self.bapple.get() else tk.DISABLED))
            self.rentry.config(state=(tk.NORMAL if self.randomania.get() else tk.DISABLED))
            self.accentry.config(state=(tk.NORMAL if self.accelerato.get() else tk.DISABLED))
            self.wentry.config(state=(tk.NORMAL if self.walls.get() else tk.DISABLED))

    def snakeuh(self):
        from src.games.Snake.Snake import Game
        self.running = False
        self.w.destroy()
        Game(color=self.color_var.get(),
             randomania=self.randomania.get(),
             rando_range=Constants.convert_str_to_list(self.rando.get()),
             bapple=self.bapple.get(),
             nb_bapple=self.bapple_nb.get(),
             accelerato=self.accelerato.get(),
             acceleration=self.acceleration.get(),
             walls=self.walls.get(),
             nb_walls=self.walls_nb.get(),
             colormania=self.colormania.get(),
             speed=self.speed.get(),
             nb_columns=self.columns.get(),
             nb_lines=self.lines.get(),
             square_dim=self.square_size.get(),
             max_speed=self.max_speed.get())

    def create_menu(self, menubar: tk.Menu):
        menubar.add_command(label="Help", command=g_help)
        menubar.add_command(label="About", command=about)
        # menubar.add_command(label="Stats", command=self.stats)
        menubar.add_command(label="Game Select Menu", command=lambda: [self.w.destroy(), run_main.run_main()])


if __name__ == '__main__':
    Launcher()

if __name__ == '__main__':
    Game()
