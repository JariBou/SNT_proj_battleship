import ctypes
import threading
import time
import tkinter as tk
import sys as system
from math import sqrt
from random import randint

import pygame as pg

from src import run_main
from src.resources.utils.Constants import Constants as Ct
from tkinter import messagebox


#####          STATIC METHODS          ####


def g_help():
    messagebox.showinfo(title="Help & Rules", message="Cliquer sur une case de la grille révèle:\n\n"
                                                      "- Une zone ne contenant aucune mine\n"
                                                      "- Une case bordée par 1, 2, 3 ou 4 mines dans un rayon d'1\n"
                                                      "  case (verticalement, horizontalement, diagonalement\n")  ##TODO: change help func


def about():
    """ Used to display an about messageBox """
    messagebox.showinfo(title="About", message="Made by: Jari \n "
                                               "Version: Alpha 1.0")


####                                  ####

def create_menu(menubar: tk.Menu):
    menubar.add_command(label="Help", command=g_help)
    menubar.add_command(label="About", command=about)
    # menubar.add_command(label="Stats", command=self.stats)
    # menubar.add_command(label="Game Select Menu", command=lambda: [self.root.destroy(), run_main.run_main()])


class Game:

    def __init__(self):
        self.BLACK = pg.Color(0, 0, 0)
        self.GREY = pg.Color(100, 100, 100)
        self.WHITE = pg.Color(255, 255, 255)
        self.BROWN = pg.Color(153, 76, 0)
        self.DARK_BROWN = pg.Color(51, 25, 0)
        self.ORANGE = pg.Color(255, 111, 0)
        self.RED = pg.Color(255, 0, 0)
        self.DARK_RED = pg.Color(153, 0, 0)
        self.GREEN = pg.Color(0, 153, 0)
        self.DARK_GREEN = pg.Color(0, 51, 0)
        self.PEACH = pg.Color(255, 0, 255)
        self.BLUE = pg.Color(0, 102, 204)
        self.DARK_BLUE = pg.Color(0, 0, 102)

        #######
        self.args: dict = {'bapple': False, 'accelerato': False, 'walls': False, 'colormania': False}
        self.nb_walls = 5
        self.acceleration = 0.0075
        self.color_types = ['modern', 'vintage', 'floorislava']
        #######

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
        pg.init()

        self.t1 = None
        self.playing = False

        self.apple: list[int, int] = [0, 0]
        self.bapple: list[list[int, int]] = []
        self.snake: list[list[int, int]] = [[9, 5], [8, 5], [7, 5], [6, 5], [5, 5], [4, 5]]

        running = True
        self.time = 0.075
        self.down = False
        self.up = False
        self.left = False
        self.right = True
        self.has_apple = False
        self.has_bapple = False
        self.updated = True
        self.nb_bapples = 3
        self.walls: list = []
        self.wall_nb = 0

        self.apple_color = self.RED
        self.bapple_color = self.PEACH
        self.snake_color = self.WHITE
        self.head_color = self.BLUE
        self.wall_color = self.DARK_BLUE
        self.bg_color = self.GREY
        self.text_color = self.WHITE
        self.color = 'modern'

        root = tk.Tk()
        root.title('Select size')
        self.change_size_menu(root, True)
        self.args_menu(root)
        Ct.center(root)
        root.mainloop()

        self.init_lvl()

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
                    if event.key == pg.K_w:
                        if self.wall_nb <= 10:
                            for o in range(3):
                                self.place_walls()
                                self.wall_nb += 1
                    if event.key == pg.K_i:
                        print(self.args)
                        print(self.acceleration)
                    if event.key == pg.K_DOWN:
                        self.switch_direction('down')
                    elif event.key == pg.K_UP:
                        self.switch_direction('up')
                    elif event.key == pg.K_RIGHT:
                        self.switch_direction('right')
                    elif event.key == pg.K_LEFT:
                        self.switch_direction('left')
                    if event.key == pg.K_r:
                        self.restart()
                    if event.key == pg.K_c:
                        self.change_colors(self.get_color())
            # if self.playing:
            #    threading.Thread(target=self.round).start()
            # self.round()   # Put in a separated thread do avoid problems with reaction speed
            pg.display.update()

    def set_time(self, x: float):
        self.time = x

    def get_color(self):
        return 'vintage' if self.color == 'modern' else ('floorislava' if self.color == 'vintage' else 'modern')

    def init_lvl(self):
        self.apple = [randint(0, self.nb_columns), randint(0, self.nb_lines)]

        self.apple: list[int, int] = [0, 0]
        self.bapple: list[list[int, int]] = []
        self.snake: list[list[int, int]] = [[9, 5], [8, 5], [7, 5], [6, 5], [5, 5], [4, 5]]

        self.apple_color = self.RED
        self.bapple_color = self.PEACH
        self.snake_color = self.WHITE
        self.head_color = self.BLUE
        self.wall_color = self.DARK_BLUE
        self.bg_color = self.GREY
        self.text_color = self.WHITE
        self.color = 'modern'

        self.time = 0.075
        self.down = False
        self.up = False
        self.left = False
        self.right = True
        self.has_apple = False
        self.has_bapple = False
        self.walls: list = []
        self.wall_nb = 0

        surface = pg.Surface((self.nb_columns * self.square_dim, self.nb_lines * self.square_dim))
        pg.draw.rect(surface, self.GREY, surface.get_rect())
        self.screen.blit(surface, (0, 0))

        if self.args.get('bapple'):
            for i in range(self.nb_bapples):
                self.place_bad_apple()
        if self.args.get('walls'):
            for i in range(10):
                self.place_walls()
                self.wall_nb += 1
        self.draw_snake()

    def switch_direction(self, direction):
        if not self.updated:
            return
        if direction == 'right' and not self.left:
            self.up, self.down, self.left, self.right = False, False, False, True
        elif direction == 'left' and not self.right:
            self.up, self.down, self.left, self.right = False, False, True, False
        elif direction == 'up' and not self.down:
            self.up, self.down, self.left, self.right = True, False, False, False
        elif direction == 'down' and not self.up:
            self.up, self.down, self.left, self.right = False, True, False, False
        self.updated = False

    def place_apple(self):
        x = randint(1, self.nb_columns)
        y = randint(1, self.nb_columns)
        if [x, y] in self.snake or [x, y] in self.walls:
            self.place_apple()
        else:
            self.apple = [x, y]
            self.draw_apple()
            self.has_apple = True

    def draw_apple(self):
        x, y = self.apple
        line = (y - 1) * self.square_dim
        col = (x - 1) * self.square_dim
        self.draw_rect((col, line), self.apple_color)

    def place_bad_apple(self):
        x = randint(1, self.nb_columns)
        y = randint(1, self.nb_columns)
        if [x, y] in self.snake or [x, y] in self.walls:
            self.place_bad_apple()
        else:
            self.bapple.append([x, y])
            line = (y - 1) * self.square_dim
            col = (x - 1) * self.square_dim
            self.draw_rect((col, line), self.bapple_color)
            self.has_bapple = True

    def draw_snake(self):
        col = (self.snake[0][0] - 1) * self.square_dim
        line = (self.snake[0][1] - 1) * self.square_dim
        self.draw_rect((col, line), self.head_color)
        for position in self.snake[1:len(self.snake)]:
            col = (position[0] - 1) * self.square_dim
            line = (position[1] - 1) * self.square_dim
            self.draw_rect((col, line), self.snake_color)

    def draw_next_snake(self, next_pos):
        self.updated = True
        if next_pos in self.walls:
            self.walls.remove(next_pos)
            col = (next_pos[0] - 1) * self.square_dim
            line = (next_pos[1] - 1) * self.square_dim
            self.draw_rect((col, line), self.bg_color)
            old = self.snake.pop()
            col = (old[0] - 1) * self.square_dim
            line = (old[1] - 1) * self.square_dim
            self.draw_rect((col, line), self.bg_color)
            return

        if next_pos in self.snake:
            self.playing = False
            return
        if self.args.get('bapple') and next_pos in self.bapple:
            old = self.snake.pop()
            self.has_bapple = False
            col = (old[0] - 1) * self.square_dim
            line = (old[1] - 1) * self.square_dim
            self.bapple.remove(next_pos)
            self.draw_rect((col, line), self.bg_color)
        if next_pos == self.apple:
            self.cpt += 1
            self.has_apple = False
            # if self.cpt == 1:
            #     print(f'{self.cpt} apple eaten')
            # else:
            #     print(f'{self.cpt} apples grallées')
            if self.args.get('colormania'):
                self.change_colors(self.get_color())
            if self.args.get('accelerato') and self.time >= self.acceleration:
                self.time -= self.acceleration
        else:
            old = self.snake.pop()
            col = (old[0] - 1) * self.square_dim
            line = (old[1] - 1) * self.square_dim
            self.draw_rect((col, line), self.bg_color)

        self.snake.insert(0, next_pos)
        col = (next_pos[0] - 1) * self.square_dim
        line = (next_pos[1] - 1) * self.square_dim
        self.draw_rect((col, line), self.head_color)
        for position in self.snake[1:len(self.snake)]:
            col = (position[0] - 1) * self.square_dim
            line = (position[1] - 1) * self.square_dim
            self.draw_rect((col, line), self.snake_color)

    def clear_board(self):
        self.screen.fill(self.bg_color)

    def place_walls(self):
        #          east    north    west    south
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        facing = directions[randint(0, len(directions)-1)]
        x = randint(1, self.nb_columns + 1)
        y = randint(1, self.nb_lines + 1)
        if self.get_snake_distance((x, y)) > 5 and self.is_far_from_wall((x, y), 7):
            x, y, last_facing = self.place_wall_at((x, y), facing)
            directions.remove(last_facing)
            facing = directions[randint(0, len(directions)-1)]
            self.place_wall_at((x, y), facing)

        else:
            self.place_walls()
            return

    def place_wall_at(self, position: tuple[int, int], facing: list[int, int]) -> tuple[int, int, list[int, int]]:
        x, y = position
        size = randint(3, 8)
        i = 0
        while i < size:
            # if not self.is_far_from_wall((x + facing[0] * i, y + facing[1] * i), 3):
            #     return x + facing[0] * (i-1) - 1, y + facing[1] * (i-1) - 1, facing
            if [x + facing[0] * i - 1, y + facing[1] * i - 1] in self.walls:
                return x + facing[0] * (i-1) - 1, y + facing[1] * (i-1) - 1, facing
            if self.get_snake_distance((x + facing[0] * i, y + facing[1] * i)) > 5:
                col = (x + facing[0] * i - 1) * self.square_dim
                line = (y + facing[1] * i - 1) * self.square_dim
                self.draw_rect((col, line), self.DARK_BLUE)
                self.walls.append([x + facing[0] * i, y + facing[1] * i])
                i += 1
            else:
                facing = [[1, 0], [0, 1], [-1, 0], [0, -1]][randint(0, 3)]
        return x + facing[0] * i - 1, y + facing[1] * i - 1, facing

    def get_snake_distance(self, position: tuple[int, int], arg: str = 'min') -> int:
        x, y = position
        if arg == 'min':
            min_distance = self.nb_columns * 2
            for spos in self.snake:
                sx, sy = spos
                curr_distance = int(sqrt((x - sx) * (x - sx) + (y - sy) * (y - sy)))
                min_distance = min(curr_distance, min_distance)
            return min_distance
        elif arg == 'max':
            max_distance = -1
            for spos in self.snake:
                sx, sy = spos
                curr_distance = int(sqrt((x - sx) * (x - sx) + (y - sy) * (y - sy)))
                max_distance = max(curr_distance, max_distance)
            return max_distance
        elif arg == 'avrg':
            distances = 0
            for spos in self.snake:
                sx, sy = spos
                distances += int(sqrt((x - sx) * (x - sx) + (y - sy) * (y - sy)))
            return distances//len(self.snake)

    def is_far_from_wall(self, position: tuple[int, int], min_distance: int = 3) -> bool:
        x, y = position
        for x2 in range(x-min_distance, x+min_distance+1):
            for y2 in range(y-min_distance, y+min_distance+1):
                if [x2, y2] in self.walls:
                    return False
        return True

    def round(self):
        while self.playing:
            if not self.has_apple:
                self.place_apple()
            if self.args.get('bapple') and not self.has_bapple:
                while len(self.bapple) <= self.nb_bapples:
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
            self.draw_points()
            self.draw_next_snake([x, y])
            time.sleep(self.time)

    def draw_points(self):
        font = pg.font.Font('freesansbold.ttf', 32)
        text = font.render(str(self.cpt), True, self.text_color, self.bg_color)
        textRect = text.get_rect()
        textRect.topright = (self.nb_columns * self.square_dim, 0)
        self.screen.blit(text, textRect)
        pass

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
        self.args_menu(root)
        tk.Button(root, text='Done', command=lambda: root.destroy()).pack()
        Ct.center(root)
        root.mainloop()

    def restart(self):
        self.clear_board()
        self.init_lvl()

    def args_menu(self, window):
        tk.Label(window, text="Enter args (dev_only)").pack()
        entry = tk.Entry(window)
        entry.pack()
        tk.Button(window, text="Confirm", command=lambda: self.pass_args(entry)).pack()

    def pass_args(self, entry: tk.Entry):
        string = entry.get()
        if string[0] != "\\":
            self.args: dict = {'bapple': False, 'accelerato': False, 'walls': False}
        else:
            string = string[1:len(string)]
        args = string.split('+')
        for arg in args:
            value = None
            try:
                name, value = arg.split('=')
            except ValueError:
                name = arg
            try:
                if name == 'accelerato':
                    self.acceleration = float(value)
                elif name == 'speed':
                    self.time = float(value)
                elif name == 'bapple':
                    self.nb_bapples = int(value)
            except ValueError:
                raise ValueError(f"wrong value for {name}: '{value}'")
            self.args[name] = True
        entry.delete(0, len(entry.get()))

    def change_colors(self, color):
        if color == 'modern':
            self.color = 'modern'
            self.apple_color = self.RED
            self.bapple_color = self.PEACH
            self.snake_color = self.WHITE
            self.head_color = self.BLUE
            self.wall_color = self.DARK_BLUE
            self.bg_color = self.GREY
        elif color == 'vintage':
            self.color = 'vintage'
            self.apple_color = self.DARK_RED
            self.bapple_color = self.PEACH
            self.snake_color = self.GREEN
            self.head_color = self.DARK_GREEN
            self.wall_color = self.DARK_BLUE
            self.bg_color = self.BLACK
        elif color == 'floorislava':
            self.color = 'floorislava'
            self.apple_color = self.GREY
            self.bapple_color = self.BLUE
            self.snake_color = self.BROWN
            self.head_color = self.DARK_BROWN
            self.wall_color = self.BLACK
            self.bg_color = self.ORANGE
        self.screen.fill(self.bg_color)
        self.draw_all()
        pass

    def draw_walls(self):
        for pos in self.walls:
            col = (pos[0] - 1) * self.square_dim
            line = (pos[1] - 1) * self.square_dim
            self.draw_rect((col, line), self.wall_color)

    def draw_bapples(self):
        for pos in self.bapple:
            col = (pos[0] - 1) * self.square_dim
            line = (pos[1] - 1) * self.square_dim
            self.draw_rect((col, line), self.bapple_color)

    def draw_all(self):
        self.draw_snake()
        self.draw_apple()
        self.draw_bapples()
        self.draw_walls()


if __name__ == '__main__':
    Game()
