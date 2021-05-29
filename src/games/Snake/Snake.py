import threading
import time
import tkinter as tk
import sys as system
from math import sqrt
from random import randint
from typing import Optional

import pygame as pg


"""from src.games.Snake.run_snake import g_help as Rshelp"""
from src import run_main
from src.resources.utils.Constants import Constants as Ct
from tkinter import messagebox
from src.games.Snake.run_snake import Launcher


#####          STATIC METHODS          ####
def g_help():
    messagebox.showinfo(title="Help & Rules", message="Colormania : \n"
                                                      "Le thème du jeu change de couleur à chaque nouvelle pomme mangée\n"
                                                      "------------------------------------------------------------\n"
                                                      "Randomania : \n"
                                                      "Augmente ou réduit la taille du serpent aléatoirement selon les paramètres donnés\n"
                                                      "------------------------------------------------------------\n"
                                                      "Bapple : \n"
                                                      "Génère des mauvaises pommes, qui si mangées réduisent de 1 votre serpent\n"
                                                      "------------------------------------------------------------\n"
                                                      "Accelerato : \n"
                                                      "Augmente la vitesse du serpent d'un montant fixe (paramètre) après chaque pomme\n"
                                                      "------------------------------------------------------------\n"
                                                      "Walls : \n"
                                                      "Génère des murs de la longueur mentionnée\n\n"
                                                      "Appuyez sur H en jeu pour faire apparaître un menu pour l'aide ou pour changer de jeu\n"
                                                      "Appuyez sur R en jeu pour réinitialiser la partie\n"
                                                      "Appuyez sur C en jeu pour changer le thème de couleur\n"
                                                      "Appuyez sur W en jeu pour créer des murs\n"
                                                      "Press 'm' to return to snake menu or 'e' to return to game selection menu")  ##TODO: help text


def about():
    """ Used to display an about messageBox """
    messagebox.showinfo(title="About", message="Made by: Jari \n "
                                               "Version: Alpha 1.0")


def create_menu(menubar: tk.Menu, root: Optional[tk.Tk]):
    menubar.add_command(label="Help", command=g_help)
    menubar.add_command(label="About", command=about)
    # menubar.add_command(label="Stats", command=self.stats)
    menubar.add_command(label="Game Select Menu", command=lambda: [pg.quit(), root.destroy(), run_main.run_main()])


####                                  ####


class Game:
    args: dict = {}

    def __init__(self, **kwargs):
        self.BLACK = pg.Color(0, 0, 0)
        self.GREY = pg.Color(100, 100, 100)
        self.DARK_GREY = pg.Color(32, 32, 32)
        self.YELLOW = pg.Color(204, 204, 0)
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
        self.YELLOW = pg.Color(204, 204, 0)
        self.WEIRD_ORANGE = pg.Color(102, 51, 0)
        self.VIOLET = pg.Color(51, 0, 102)
        self.FADE_GREEN = pg.Color(0, 204, 102)
        self.CYAN = pg.Color(0, 204, 204)
        self.PINK = pg.Color(255, 0, 255)

        #######
        print(kwargs)
        self.color = kwargs.get('color', 'modern')
        self.random_color = kwargs.get('random_color', False)
        for arg in ['bapple', 'accelerato', 'walls', 'colormania', 'randomania', 'speed']:
            self.args[arg] = kwargs.get(arg, False)
        # self.args = {'bapple': kwargs.get('bapple', False), 'accelerato': False, 'walls': False, 'colormania': False,
        #                    'randomania': False, 'speed': True}
        print(self.args)
        self.wall_nb = kwargs.get('nb_walls', 5)
        self.acceleration = kwargs.get('acceleration', 0.0055)
        self.time = kwargs.get('speed', 0.075)
        self.max_speed = kwargs.get('max_speed', 0.01)
        self.color_types = ['modern', 'vintage', 'floorislava', 'ocean', 'outerworld']
        self.redo_bapples = True
        self.nb_bapples = kwargs.get('nb_bapple', 3)
        self.random_range = kwargs.get('rando_range', [-3, 5])

        self.nb_columns = kwargs.get('nb_columns', 30)
        self.nb_lines = kwargs.get('nb_lines', 30)
        self.square_dim = kwargs.get('square_dim', 10)
        #######
        self.cpt = 0
        self.square_size = (self.square_dim, self.square_dim)
        self.square_surface = pg.Surface(self.square_size)
        self.root = pg.Surface((self.nb_columns * self.square_dim, self.nb_lines * self.square_dim))
        self.path = Ct.get_path()
        pg.display.set_caption(f'Snake - current args: {self.get_curr_args()}')
        self.screen = pg.display.set_mode((self.nb_columns * self.square_dim, self.nb_lines * self.square_dim))
        pg.display.flip()
        pg.init()

        self.t1 = None
        self.playing = False

        self.apple: list[int, int] = [0, 0]
        self.bapple: list[list[int, int]] = []
        self.snake: list[list[int, int]] = [[9, 5], [8, 5], [7, 5], [6, 5], [5, 5], [4, 5]]

        running = True
        self.down = self.up = self.left = False
        self.right = True
        self.has_apple = self.has_bapple = False
        self.updated = True
        self.walls: list[list[int, int]] = []
        self.add_lenght = 0
        self.apple_cpt = 0
        self.dead = False

        self.apple_color = self.RED
        self.bapple_color = self.PEACH
        self.snake_color = self.WHITE
        self.head_color = self.BLUE
        self.wall_color = self.DARK_BLUE
        self.bg_color = self.GREY
        self.text_color = self.WHITE

        # self.settings(True)

        self.init_lvl()

        master = tk.Tk()
        master.withdraw()
        g_help()
        master.destroy()   ## THis bloody fixes problems going back to main menu
        master.quit()
        self.displayed = False

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                    pg.quit()
                    quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        if not self.playing and not self.dead:
                            self.resume_screen()
                        elif self.playing:
                            self.pause_screen()
                        # self.playing = True if not self.playing else False
                        # print('playing now enabled' if self.playing else 'playing now disabled')
                        # self.clear_board()
                        # if not self.playing:
                        #     self.draw_text('Press <space> to resume', 'center')
                        # if self.playing:
                        #     threading.Thread(target=self.round).start()
                    if event.key == pg.K_h:
                        self.settings()
                        # self.help()
                    if event.key == pg.K_w:
                        if self.wall_nb <= 10:
                            for o in range(3):
                                self.place_walls()
                                self.wall_nb += 1
                    if event.key == pg.K_i:
                        print(self.args)
                        print(self.acceleration)
                        print(self.random_range)
                        print(self.bapple)
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
                    if event.key == pg.K_e:
                        self.playing = False
                        if self.t1 is not None:
                            self.t1.join()
                        pg.quit()
                        Launcher()

                    if event.key == pg.K_m:
                        self.playing = False
                        if self.t1 is not None:
                            self.t1.join()
                        pg.quit()
                        run_main.run_main()
            pg.display.update()
            if self.dead and not self.displayed:
                self.displayed = True
                master = tk.Tk()
                master.withdraw()
                messagebox.showinfo("End of Game",
                                    "After closing this window press 'r' to restart,\n'm' to return to snake menu,\n or 'e' to return to game menu")
                master.destroy()  ## THis bloody fixes problems going back to main menu
                master.quit()

    def get_color(self, get_random: bool = False):
        color_list = ['modern', 'vintage', 'floorislava', 'ocean', 'outerworld']
        if get_random:
            color_list.remove(self.color)
            next_color = color_list[randint(0, len(color_list) - 1)]
            return next_color
        pos = color_list.index(self.color)
        next_color = color_list[pos + 1 if pos + 1 < len(color_list) else 0]
        # return 'vintage' if self.color == 'modern' else ('floorislava' if self.color == 'vintage' else 'modern')
        return next_color

    def pause_screen(self):
        self.playing = False
        self.clear_board()
        self.draw_text('Press <space> to resume', 'center')
        print('playing now disabled')

    def resume_screen(self):
        self.clear_board()
        self.playing = True
        threading.Thread(target=self.round).start()
        print('playing now enabled')

    def init_lvl(self):
        self.dead = False
        self.apple: list[int, int] = [0, 0]
        self.bapple: list[list[int, int]] = []
        self.snake: list[list[int, int]] = [[9, 5], [8, 5], [7, 5], [6, 5], [5, 5], [4, 5]]
        self.redo_bapples = True
        self.cpt = 0
        self.down = self.up = self.left = False
        self.right = True
        self.has_apple = self.has_bapple = False
        self.updated = True
        self.walls: list[list[int, int]] = []
        self.add_lenght = 0
        self.apple_cpt = 0

        self.change_colors(self.color)

        if self.args.get('bapple'):
            for i in range(self.nb_bapples):
                self.place_bad_apple()
        if self.args.get('walls'):
            for i in range(self.wall_nb):
                self.place_walls()
                self.wall_nb += 1

        self.draw_all()
        self.clear_board()
        self.draw_snake()
        self.draw_text('Press <space> to start!', 'center')

    def switch_direction(self, direction):
        if not self.updated or not self.playing:
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
        y = randint(1, self.nb_lines)
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
        if [x, y] in self.snake or [x, y] in self.walls + self.bapple or self.get_snake_distance((x, y), 'min') < 6 or [
            x, y] == self.apple:
            self.place_bad_apple()
        else:
            self.bapple.append([x, y])
            col = (x - 1) * self.square_dim
            line = (y - 1) * self.square_dim
            self.draw_rect((col, line), self.bapple_color)
            self.has_bapple = True

    def change_bapples(self):
        self.redo_bapples = False
        for pos in self.bapple:
            col = (pos[0] - 1) * self.square_dim
            line = (pos[1] - 1) * self.square_dim
            self.draw_rect((col, line), self.bg_color)
        self.bapple = []
        while len(self.bapple) < self.nb_bapples:
            self.place_bad_apple()
        self.draw_bapples()

    def draw_snake(self):
        col = (self.snake[0][0] - 1) * self.square_dim
        line = (self.snake[0][1] - 1) * self.square_dim
        self.draw_rect((col, line), self.head_color)
        for position in self.snake[1:len(self.snake)]:
            col = (position[0] - 1) * self.square_dim
            line = (position[1] - 1) * self.square_dim
            self.draw_rect((col, line), self.snake_color)

    def draw_next_snake(self, next_pos: list[int, int], snake=None):
        if snake is None:
            snake = self.snake
        self.updated = True
        if len(snake) == 1:
            self.playing = False
            self.dead = True
            self.draw_text('You chopped your head silly...', 'bottom')
            return
        if next_pos in self.walls:
            self.walls.remove(next_pos)
            col = (next_pos[0] - 1) * self.square_dim
            line = (next_pos[1] - 1) * self.square_dim
            self.draw_rect((col, line), self.bg_color)
            self.pop_snake(snake)
            self.cpt -= 1
            return
        if next_pos in snake:
            self.playing = False
            self.dead = True
            self.draw_text('You ate yourself, smart...', 'bottom')
            return
        if self.args.get('bapple') and next_pos in self.bapple:
            self.apple_cpt += 1
            self.pop_snake(snake)
            self.bapple.remove(next_pos)
            self.has_bapple = False
            self.cpt -= 1
        if next_pos == self.apple:
            self.cpt += 1
            self.has_apple = False
            # if self.cpt == 1:
            #     print(f'{self.cpt} apple eaten')
            # else:
            #     print(f'{self.cpt} apples grallées')
            if self.args.get('randomania'):
                a, b = self.random_range
                self.add_lenght = randint(a, b)
            if self.args.get('colormania'):
                self.change_colors(self.get_color(self.random_color))
            if self.args.get('accelerato') and self.time >= self.acceleration:
                if self.time >= self.acceleration:
                    self.time -= self.acceleration
                elif self.time != self.max_speed:
                    self.time = self.max_speed
        else:
            if self.add_lenght != 0:
                if self.add_lenght < 0:
                    self.pop_snake(snake)
                    self.pop_snake(snake)
                    self.cpt -= 2
                self.cpt += 1
                self.add_lenght += 1 if self.add_lenght < 0 else -1
            else:
                self.pop_snake(snake)

        snake.insert(0, next_pos)
        col = (next_pos[0] - 1) * self.square_dim
        line = (next_pos[1] - 1) * self.square_dim
        self.draw_rect((col, line), self.head_color)
        for position in self.snake[1:len(snake)]:
            col = (position[0] - 1) * self.square_dim
            line = (position[1] - 1) * self.square_dim
            self.draw_rect((col, line), self.snake_color)

    def pop_snake(self, snake: list[list[int, int]]):
        old = snake.pop()
        col = (old[0] - 1) * self.square_dim
        line = (old[1] - 1) * self.square_dim
        self.draw_rect((col, line), self.bg_color)

    def clear_board(self):
        self.screen.fill(self.bg_color)

    def place_walls(self):
        #          east    north    west    south
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        facing = directions[randint(0, len(directions) - 1)]
        x = randint(1, self.nb_columns + 1)
        y = randint(1, self.nb_lines + 1)
        if self.get_snake_distance((x, y)) > 5 and self.is_far_from_wall((x, y), 7) and not (
                x > self.nb_columns - 8 and y < 8):
            x, y, last_facing = self.place_wall_at((x, y), facing)
            directions.remove(last_facing)
            facing = directions[randint(0, len(directions) - 1)]
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
                return x + facing[0] * (i - 1) - 1, y + facing[1] * (i - 1) - 1, facing
            if self.get_snake_distance((x + facing[0] * i, y + facing[1] * i)) > 5:
                col = (x + facing[0] * i - 1) * self.square_dim
                line = (y + facing[1] * i - 1) * self.square_dim
                self.draw_rect((col, line), self.wall_color)
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
            return distances // len(self.snake)

    def is_far_from_wall(self, position: tuple[int, int], min_distance: int = 3) -> bool:
        x, y = position
        for x2 in range(x - min_distance, x + min_distance + 1):
            for y2 in range(y - min_distance, y + min_distance + 1):
                if [x2, y2] in self.walls:
                    return False
        return True

    def round(self):
        self.draw_all()
        while self.playing:
            self.draw_text(f'  {self.cpt}  ', 'top_right')
            # self.draw_apple()
            # self.draw_bapples()
            if not self.has_apple:
                self.place_apple()
            if self.args.get('bapple'):
                if (self.apple_cpt + 1) % 5 == 0 and self.redo_bapples:
                    self.change_bapples()
                elif (self.apple_cpt + 1) % 5 != 0:
                    self.redo_bapples = True
                if not self.has_bapple:
                    while len(self.bapple) < self.nb_bapples:
                        self.place_bad_apple()
            if not self.snake:
                pass
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

    def draw_text(self, text: str, position: str, size: int = -1):
        font = pg.font.Font('freesansbold.ttf', self.nb_columns * self.square_dim // 16 if size == -1 else size)
        text = font.render(text, True, self.text_color, self.bg_color)
        textRect = text.get_rect()
        if position == 'top_right':
            textRect.topright = (self.nb_columns * self.square_dim, 0)
        elif position == 'center':
            textRect.center = (self.nb_columns * self.square_dim // 2, self.nb_lines * self.square_dim // 2)
        elif position == 'top_left':
            textRect.topleft = (0, 0)
        elif position == 'bottom_left':
            textRect.bottomleft = (0, self.nb_lines * self.square_dim)
        elif position == 'bottom_right':
            textRect.bottomright = (self.nb_columns * self.square_dim, self.nb_lines * self.square_dim)
        elif position == 'top':
            textRect.topleft = ((self.nb_columns * self.square_dim // 2) - textRect.width // 2, 0)
        elif position == 'bottom':
            textRect.bottomleft = (
                (self.nb_columns * self.square_dim // 2) - textRect.width // 2, self.nb_lines * self.square_dim)
        else:
            raise Exception(f"Invalid argument '{position}'")
        self.screen.blit(text, textRect)

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
            tk.Button(window, text="Confirm", command=lambda: self.change_size_val(entry, window)).pack()

    def change_size_val(self, entry: tk.Entry, window=None):
        string = entry.get()
        if string == '':
            self.change_sizes(self.nb_columns, self.nb_lines, self.square_dim)
            if window is not None:
                window.destroy()
            return
        vals = string.split('+')
        squareDim = int(vals.pop())
        nCol, nLine = vals[0].split('x')
        self.change_sizes(int(nCol), int(nLine), squareDim)
        if window is not None:
            window.destroy()

    # def help(self, start=False):
    #     if self.playing:
    #         self.playing = False
    #         print('playing set to false')
    #         self.draw_text('press <space> to resume', 'top', self.nb_columns * self.square_dim // 20)
    #     root = tk.Tk()
    #     root.title('Aide')
    #     root.geometry('450x350')
    #     root.protocol("WM_DELETE_WINDOW", self.exit_game)
    #     Texte = tk.Label(root, text="Colormania : \n"
    #                                 "Le thème du jeu change de couleur à chaque nouvelle pomme mangée\n"
    #                                 "------------------------------------------------------------\n"
    #                                 "Randomania : \n"
    #                                 "Augmente ou réduit la taille du serpent aléatoirement selon les paramètres donnés\n"
    #                                 "------------------------------------------------------------\n"
    #                                 "Bapple : \n"
    #                                 "Génère des mauvaises pommes, qui si mangées réduisent de 1 votre serpent\n"
    #                                 "------------------------------------------------------------\n"
    #                                 "Accelerato : \n"
    #                                 "Augmente la vitesse du serpent d'un montant fixe (paramètre) après chaque pomme\n"
    #                                 "------------------------------------------------------------\n"
    #                                 "Walls : \n"
    #                                 "Génère des murs de la longueur mentionnée\n\n"
    #                                 "Appuyez sur H en jeu pour faire apparaître l'aide\n"
    #                                 "Appuyez sur R en jeu pour réinitialiser la partie\n"
    #                                 "Appuyez sur C en jeu pour changer le thème de couleur\n"
    #                                 "Appuyez sur W en jeu pour créer des murs\n")
    #     Texte.pack()
    #     tk.Button(root, text='Ok', command=lambda: root.destroy()).pack()
    #     root.mainloop()

    def settings(self, start=False):
        if self.playing:
            self.playing = False
            print('playing set to false')
            self.draw_text('press <space> to resume', 'top', self.nb_columns * self.square_dim // 20)
        root = tk.Tk()
        root.title('Settings')
        root.resizable(width=False, height=False)
        root.protocol("WM_DELETE_WINDOW", self.exit_game)
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        create_menu(menubar, root)
        self.change_size_menu(root, start)
        self.args_menu(root)
        tk.Button(root, text='Done', command=lambda: root.destroy()).pack()
        Ct.center(root)
        root.mainloop()
        pg.display.set_caption(f'Snake - current args: {self.get_curr_args()}')
        threading.Thread(target=self.round).start()

    def get_curr_args(self) -> str:
        active = [arg for arg in self.args.keys() if self.args[arg] and not arg.endswith('_vals')]
        if not active:
            return 'None'
        strbuilder = ''
        for arg in active:
            if arg == 'speed':
                continue
            if strbuilder != '':
                strbuilder += ' & ' + arg
            else:
                strbuilder += arg
        return strbuilder

    def restart(self):
        self.displayed = False
        self.playing = False
        self.init_lvl()

    def args_menu(self, window):
        tk.Label(window, text="Enter args (dev_only)").pack()
        entry = tk.Entry(window)
        entry.pack()
        tk.Button(window, text="Confirm", command=lambda: self.pass_argsV2(entry)).pack()

    def pass_argsV2(self, entry: tk.Entry):
        string = entry.get()
        if string[0] == '+' or string[0] == '\\':
            string = string[1:len(string)]
            print('keeping args')
        else:
            self.args: dict = {'bapple': False, 'accelerato': False, 'walls': False, 'colormania': False,
                               'randomania': False, 'speed': True}
            print('reseting args')
        args: list[str] = string.split('+')
        for arg in args:

            if arg.__contains__('='):
                name, value = arg.split('=')
                if name not in self.args.keys():
                    raise ValueError(f"wrong input: {name} is not a valid argument")
                if name == 'accelerato':
                    val = float(value)
                    self.acceleration = val
                elif name == 'speed':
                    val = float(value)
                    self.time = val
                elif name == 'bapple':
                    val = int(value)
                    self.nb_bapples = val
                elif name == 'randomania':
                    val = value.split(',')
                    val = [int(val[0]), int(val[1])]
                    self.random_range = val
                else:
                    raise AttributeError(f"wrong input: {name} doesn't support value assignement")
            else:
                name = arg
                if name not in self.args.keys():
                    raise ValueError(f"wrong input: {name} is not a valid argument")
                if name == 'accelerato':
                    self.acceleration = self.args[name + '_vals'] = 0.005
                elif name == 'bapple':
                    self.nb_bapples = self.args[name + '_vals'] = 3
                elif name == 'randomania':
                    self.random_range = self.args[name + '_vals'] = [-3, 5]
            self.args[name] = True
        entry.delete(0, len(entry.get()))

    def change_colors(self, color):
        self.color = color
        if color == 'modern':
            self.apple_color = self.RED
            self.bapple_color = self.PEACH
            self.snake_color = self.WHITE
            self.head_color = self.BLUE
            self.wall_color = self.DARK_BLUE
            self.bg_color = self.GREY
        elif color == 'vintage':
            self.apple_color = self.DARK_RED
            self.bapple_color = self.PEACH
            self.snake_color = self.GREEN
            self.head_color = self.DARK_GREEN
            self.wall_color = self.DARK_BLUE
            self.bg_color = self.BLACK
        elif color == 'floorislava':
            self.apple_color = self.GREY
            self.bapple_color = self.BLUE
            self.snake_color = self.BROWN
            self.head_color = self.DARK_BROWN
            self.wall_color = self.BLACK
            self.bg_color = self.ORANGE
        elif color == 'ocean':
            self.apple_color = self.GREEN
            self.bapple_color = self.YELLOW
            self.snake_color = self.DARK_GREY
            self.head_color = self.BLACK
            self.wall_color = self.WEIRD_ORANGE
            self.bg_color = self.BLUE
        elif color == 'outerworld':
            self.apple_color = self.DARK_GREEN
            self.bapple_color = self.YELLOW
            self.snake_color = self.CYAN
            self.head_color = self.FADE_GREEN
            self.wall_color = self.WEIRD_ORANGE
            self.bg_color = self.VIOLET
        self.screen.fill(self.bg_color)
        self.draw_all()

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
