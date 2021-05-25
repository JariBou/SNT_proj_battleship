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


def create_menu(menubar: tk.Menu):
    menubar.add_command(label="Help", command=g_help)
    menubar.add_command(label="About", command=about)
    # menubar.add_command(label="Stats", command=self.stats)
    # menubar.add_command(label="Game Select Menu", command=lambda: [self.root.destroy(), run_main.run_main()])
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
        for arg in ['bapple', 'accelerato', 'walls', 'colormania', 'randomania', 'speed']:
            self.args[arg] = kwargs.get(arg, False)
        # self.args = {'bapple': kwargs.get('bapple', False), 'accelerato': False, 'walls': False, 'colormania': False,
        #                    'randomania': False, 'speed': True}
        print(self.args)
        # self.nb_walls = 5
        # self.acceleration = 0.0075
        self.nb_walls = kwargs.get('nb_walls', 5)
        self.acceleration = kwargs.get('acceleration', 0.0075)
        self.time = kwargs.get('speed', 0.045)
        self.color_types = ['modern', 'vintage', 'floorislava', 'ocean', 'outerworld']
        self.redo_bapples = True

        self.nb_columns = kwargs.get('nb_columns', 70)
        self.nb_lines = kwargs.get('nb_lines', 70)
        self.square_dim = kwargs.get('square_dim', 12)
        #######
        self.cpt = 0
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
        self.down = self.up = self.left = False
        self.right = True
        self.has_apple = self.has_bapple = False
        self.updated = True
        self.nb_bapples = 3
        self.walls: list = []
        self.wall_nb = 0
        self.add_lenght = 0
        self.random_range = [-3, 5]
        self.apple_cpt = 0

        self.apple_color = self.RED
        self.bapple_color = self.PEACH
        self.snake_color = self.WHITE
        self.head_color = self.BLUE
        self.wall_color = self.DARK_BLUE
        self.bg_color = self.GREY
        self.text_color = self.WHITE

        # root = tk.Tk()
        # root.title('Select size')
        # self.change_size_menu(root, True)
        # self.args_menu(root)
        # Ct.center(root)
        # root.mainloop()

        self.init_lvl()
        self.draw_all()
        self.clear_board()
        self.draw_snake()
        self.draw_text('Press <space> to start!', 'center')

        self.wall_colors = [self.BLUE, self.BLACK, self.BROWN, self.YELLOW, self.VIOLET]
        self.snake_distance = 10

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        if not self.playing:
                            self.resume_screen()
                        elif self.playing:
                            self.pause_screen()
                    if event.key == pg.K_w:
                        self.walls = []
                        self.clear_board()
                        self.draw_snake()
                        # self.draw_radius()
                        self.wall_nb = 0
                        for o in range(4):
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
                    elif event.key == pg.K_c:
                        self.walls = []
                        self.clear_board()
                    if event.key == pg.K_r:
                        self.restart()
            keys = pg.key.get_pressed()
            if keys[pg.K_DOWN]:
                self.switch_direction('down')
            elif keys[pg.K_UP]:
                self.switch_direction('up')
            elif keys[pg.K_RIGHT]:
                self.switch_direction('right')
            elif keys[pg.K_LEFT]:
                self.switch_direction('left')
            time.sleep(self.time)
            pg.display.update()

    def pause_screen(self):
        self.playing = False
        self.clear_board()
        self.draw_text('Press <space> to resume', 'center')
        print('playing now disabled')

    def resume_screen(self):
        self.clear_board()
        self.playing = True
        print('playing now enabled')

    def init_lvl(self):
        self.apple: list[int, int] = [0, 0]
        self.bapple: list[list[int, int]] = []
        self.snake: list[list[int, int]] = [[9, 5], [8, 5], [7, 5], [6, 5], [5, 5], [4, 5], [4, 6], [4, 7], [4, 8]]

        self.apple_color = self.RED
        self.bapple_color = self.PEACH
        self.snake_color = self.WHITE
        self.head_color = self.BLUE
        self.wall_color = self.DARK_BLUE
        self.bg_color = self.GREY
        self.text_color = self.WHITE

        self.down = False
        self.up = False
        self.left = False
        self.right = True
        self.has_apple = False
        self.has_bapple = False
        self.walls: list = []
        self.wall_nb = 0
        self.add_lenght = 0
        self.random_range = [-3, 5]
        self.apple_cpt = 0

        surface = pg.Surface((self.nb_columns * self.square_dim, self.nb_lines * self.square_dim))
        pg.draw.rect(surface, self.GREY, surface.get_rect())
        self.screen.blit(surface, (0, 0))

        self.clear_board()
        if not self.playing:
            self.draw_text('Press <space> to start!', 'center')
        self.draw_snake()

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
        x_off = 1 if self.right else (-1 if self.left else 0)
        y_off = -1 if self.up else (1 if self.down else 0)
        x = self.snake[0][0] + x_off
        y = self.snake[0][1] + y_off
        if x == 0 or x == self.nb_columns + 1:
            x = (self.nb_columns if x == 0 else 1)
        if y == 0 or y == self.nb_lines + 1:
            y = (self.nb_lines if y == 0 else 1)
        self.draw_next_snake([x, y])
        # self.draw_radius()

    def draw_radius(self):
        self.clear_board()
        self.draw_snake()
        self.draw_walls()
        for x in range(1, self.nb_columns):
            for y in range(1, self.nb_lines):
                if self.get_snake_distance((x, y), 'min') == self.snake_distance:
                    col = (x - 1) * self.square_dim
                    line = (y - 1) * self.square_dim
                    self.draw_rect((col, line), self.RED)

    def place_walls(self):
        #          east    north    west    south
        directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        facing = directions[randint(0, len(directions)-1)]
        x = randint(1, self.nb_columns + 1)
        y = randint(1, self.nb_lines + 1)
        if self.get_snake_distance((x, y)) > self.snake_distance and self.is_far_from_wall((x, y), 8) and not (x > self.nb_columns - 8 and y < 8):
            x, y, last_facing = self.place_wall_at((x, y), facing)
            directions.remove(last_facing)
            facing = directions[randint(0, len(directions)-1)]
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
            if [x + facing[0] * i, y + facing[1] * i] in self.walls:
                return x + facing[0] * (i) , y + facing[1] * (i) , facing
            if self.get_snake_distance((x + facing[0] * i, y + facing[1] * i)) > self.snake_distance:
                col = (x + facing[0] * i - 1) * self.square_dim
                line = (y + facing[1] * i - 1) * self.square_dim
                self.draw_rect((col, line), self.wall_colors[self.wall_nb])
                self.walls.append([x + facing[0] * i, y + facing[1] * i])
                i += 1
            else:
                facing = [[1, 0], [0, 1], [-1, 0], [0, -1]][randint(0, 3)]
        return x + facing[0] * i, y + facing[1] * i, facing

    def get_snake_distance(self, position: tuple[int, int], arg: str = 'min') -> int:
        x, y = position
        if arg == 'min':
            min_distance = self.nb_columns * 2
            for spos in self.snake:
                sx, sy = self.snake[0]
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
        self.pop_snake(self.snake)
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

    def round(self):
        self.draw_all()
        while self.playing:
            self.draw_text(f'  {self.cpt}  ', 'top_right')
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
        font = pg.font.Font('freesansbold.ttf', self.nb_columns*self.square_dim//16 if size == -1 else size)
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
            textRect.bottomleft = ((self.nb_columns * self.square_dim // 2) - textRect.width // 2, self.nb_lines * self.square_dim)
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

    def restart(self):
        self.clear_board()
        self.init_lvl()

    def draw_walls(self):
        for pos in self.walls:
            col = (pos[0] - 1) * self.square_dim
            line = (pos[1] - 1) * self.square_dim
            self.draw_rect((col, line), self.wall_color)

    def draw_all(self):
        self.draw_snake()
        self.draw_walls()


if __name__ == '__main__':
    Game()
