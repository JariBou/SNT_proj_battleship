import threading
import time
import tkinter as tk
import sys as system
from random import randint
from typing import Optional

import pygame as pg


"""from src.games.Snake.run_snake import g_help as Rshelp"""
from src import run_main
from src.resources.utils.Constants import Constants as Ct
from tkinter import messagebox
from src.games.Snake.run_snake2P import Launcher


#####          STATIC METHODS          ####
def g_help():   ## NOT UP TO DATE
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
                                                      "Appuyez sur E en jeu pour retourner au launcher Snake©\n"
                                                      "Appuyez sur M en jeu pour retourner dans la Library Steam\n")


def about():
    """ Used to display an about messageBox """
    messagebox.showinfo(title="About", message="Made by: Jari\n "
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

        head_colors: dict = {
            "modern": self.BLUE,
            "vintage": self.DARK_GREEN,
            "therock": self.DARK_BROWN,
            "ocean": self.DARK_BLUE,
            "outerworld": self.FADE_GREEN,
            "darkknight": self.BLACK
            }
        body_colors: dict = {
            "modern": self.WHITE,
            "vintage": self.GREEN,
            "therock": self.BROWN,
            "ocean": self.BLUE,
            "outerworld": self.CYAN,
            "darkknight": self.DARK_GREY
            }

        self.snake1_colors: dict = {
            "head": head_colors.get(kwargs.get("snake1_color")),
            "body": body_colors.get(kwargs.get("snake1_color"))
            }
        self.snake2_colors: dict = {
            "head": head_colors.get(kwargs.get("snake2_color")),
            "body": body_colors.get(kwargs.get("snake2_color"))
            }

        ##
        randomNames = ["Philip", "Olaf", "Olga", "James", "Casper", "Razmo", "Rapido", "Zigg", "Oggy", "Devilman",
                       "Crybaby", "Barbarian", "Elza", "Ssssss", "Einstein", "Gauss", "Conway", "Hawking", "Albert"]
        self.time = kwargs.get("speed")
        self.max_speed = kwargs.get("max_speed")
        self.snakeNames = [kwargs.get("snake1_name") if kwargs.get("snake1_name") != "Random" else randomNames[randint(0, len(randomNames)-1)],
                           kwargs.get("snake2_name") if kwargs.get("snake2_name") != "Random" else randomNames[randint(0, len(randomNames)-1)]]
        ##
        while self.snakeNames[1] == self.snakeNames[0]:
            self.snakeNames[1] = randomNames[randint(0, len(randomNames)-1)]

        self.nb_columns = kwargs.get("nb_columns", 50)
        self.nb_lines = kwargs.get("nb_lines", 50)
        self.square_dim = kwargs.get("square_dim", 10)
        self.square_size = (self.square_dim, self.square_dim)
        self.square_surface = pg.Surface(self.square_size)
        self.root = pg.Surface((self.nb_columns * self.square_dim, self.nb_lines * self.square_dim))
        self.path = Ct.get_path()
        pg.display.set_caption(f'Snake 2 Players Alpha - {self.snakeNames[0]} Vs {self.snakeNames[1]}')
        self.screen = pg.display.set_mode((self.nb_columns * self.square_dim, self.nb_lines * self.square_dim))
        pg.display.flip()
        pg.init()

        self.t1 = None
        self.playing = False
        self.redo_bapples = False

        self.apple: list[int, int] = [0, 0]
        self.bapple: list[list[int, int]] = []
        self.bapple_color = self.DARK_RED

        running = True

        self.apple_cpt = 0

        self.apple_color = self.RED
        self.bg_color = self.GREY
        self.text_color = self.WHITE

        # self.settings(True)
        self.snakes: list[Snake, Snake] = []
        self.init_lvl()

        master = tk.Tk()
        master.withdraw()
        g_help()
        master.destroy()   ## THis bloody fixes problems going back to main menu
        master.quit()
        self.displayed = False
        self.dead = False

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
                    if event.key == pg.K_h:
                        # self.settings()
                        pass
                        # self.help()
                    if event.key == pg.K_i:
                        pass
                        # print(self.args)
                        # print(self.acceleration)
                        # print(self.random_range)
                        # print(self.bapple)

                    if event.key == pg.K_r:
                        self.restart()

                    ## Player 1
                    if event.key == pg.K_z:
                        self.snakes[0].changeDirection((0, -1))
                    if event.key == pg.K_s:
                        self.snakes[0].changeDirection((0, 1))
                    if event.key == pg.K_q:
                        self.snakes[0].changeDirection((-1, 0))
                    if event.key == pg.K_d:
                        self.snakes[0].changeDirection((1, 0))

                    ## Player 2
                    if event.key == pg.K_UP:
                        self.snakes[1].changeDirection((0, -1))
                    if event.key == pg.K_DOWN:
                        self.snakes[1].changeDirection((0, 1))
                    if event.key == pg.K_LEFT:
                        self.snakes[1].changeDirection((-1, 0))
                    if event.key == pg.K_RIGHT:
                        self.snakes[1].changeDirection((1, 0))

                    if event.key == pg.K_e:
                        self.playing = False
                        running = False
                        if self.t1 is not None:
                            self.t1.join()
                        pg.quit()
                        Launcher()

                    if event.key == pg.K_m:
                        self.playing = False
                        running = False
                        if self.t1 is not None:
                            self.t1.join()
                        pg.quit()
                        run_main.run_main()
            pg.display.update()
            if self.dead and not self.displayed:
                self.displayed = True
                self.playing = False
                master = tk.Tk()
                master.withdraw()
                messagebox.showinfo("End of Game",
                                    "After closing this window press 'r' to restart,\n'm' to return to snake menu,\n or 'e' to return to game menu")
                master.destroy()  ## THis bloody fixes problems going back to main menu
                master.quit()
                print(f'{running=}')

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

    def draw_all(self):
        self.draw_scores()
        self.draw_apple()
        for snake in self.snakes:
            snake.draw()

    def init_lvl(self):
        print("Starting level")
        self.apple: list[int, int] = [0, 0]
        self.bapple: list[list[int, int]] = []
        self.apple_cpt = 0
        params = [self.nb_columns, self.nb_lines, self.square_dim]
        self.snakes = [
            Snake(self.screen, self.square_surface, bg_color=self.bg_color, head_color=self.snake1_colors.get("head"),
                  body_color=self.snake1_colors.get("body"), direction=(0, 1), snake=[[2, 3], [2, 4], [2, 5]], name=self.snakeNames[0], param=params),
            Snake(self.screen, self.square_surface, bg_color=self.bg_color, head_color=self.snake2_colors.get("head"),
                  body_color=self.snake2_colors.get("body"), direction=(0, 1), snake=[[8, 3], [9, 3], [10, 3]], name=self.snakeNames[1], param=params)
            ]
        self.snakes[0].setOtherSnake(self.snakes[1])
        self.snakes[1].setOtherSnake(self.snakes[0])

        self.place_apple()
        self.draw_all()
        self.clear_board()
        self.dead = False
        self.draw_text('Press <space> to start!', 'center')

    def restart(self):
        self.playing = False
        self.init_lvl()
        self.pause_screen()

    def place_apple(self):
        x = randint(0, self.nb_columns-1)
        y = randint(0, self.nb_lines-1)

        self.apple = [x, y]
        for snake in self.snakes:
            if self.apple in snake.get():
                return self.place_apple()
            snake.apple = self.apple
        self.draw_apple()

    def place_bapple(self):
        x = randint(0, self.nb_columns-1)
        y = randint(0, self.nb_lines-1)

        bapple = [x, y]
        for snake in self.snakes:
            if self.apple in snake.get():
                return self.place_apple()
            snake.addBapple(bapple)
        self.draw_bapple()

    def draw_apple(self):
        x, y = self.apple
        col = x * self.square_dim
        line = y * self.square_dim
        self.draw_rect((col, line), self.apple_color)

    def draw_bapple(self):
        for x, y in self.bapple:
            col = x * self.square_dim
            line = y * self.square_dim
            self.draw_rect((col, line), self.bapple_color)

    def clear_board(self):
        self.screen.fill(self.bg_color)

    def round(self):
        self.draw_all()
        while self.playing:
            # self.snakes[0].move()
            # self.snakes[1].move()
            for snake in self.snakes:
                snake.move()
                if snake.has_apple:
                    self.draw_scores()
                    self.place_apple()
                snake.has_apple = False
                if not snake.alive:
                    self.dead = True
                    self.playing = False

            time.sleep(self.time)

    def draw_scores(self):
        self.draw_text(str(self.snakes[0].cpt), "top_left")
        self.draw_text(str(self.snakes[1].cpt), "top_right")

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

    def changeSnakeColor(self, snakeNumber: int,):
        ## Snake number according to the player number (so 1 or 2)
        # self.snakes[snakeNumber-1].setColors()
        pass


class Snake:

    def __init__(self, screen: pg.display, square_surface: pg.Surface, param: list[int, int, int], **kwargs):
        self.screen = screen
        self.square_surface = square_surface
        self.nb_columns = param[0]
        self.nb_lines = param[1]
        self.square_dim = param[2]
        self.head_color: pg.Color = kwargs.get("head_color")
        self.body_color: pg.Color = kwargs.get("body_color")
        self.bg_color: pg.Color = kwargs.get("bg_color")
        self.snake: list[list[int, int]] = kwargs.get("snake")
        self.otherSnake: Optional['Snake'] = kwargs.get("otherSnake")
        self.apple: list[int, int] = kwargs.get("apple")
        self.direction: tuple[int, int] = kwargs.get("direction")
        self.name = kwargs.get("name", "unnamed snake")
        self.updated: bool = True
        self.alive = True
        self.has_apple = False
        self.bapples: list[list[int, int]] = []
        self.cpt: int = 0

    def get(self) -> list[list[int, int]]:
        return self.snake

    def changeDirection(self, direction):
        if not self.updated:
            return
        if direction[0] * self.direction[0] != 0 or direction[1] * self.direction[1] != 0 or direction == self.direction:
            return
        self.updated = False
        self.direction = direction

    def move(self):
        x = self.snake[-1][0] + self.direction[0]
        y = self.snake[-1][1] + self.direction[1]
        if x == -1 or x == self.nb_columns:
            x = (self.nb_columns-1 if x == -1 else 0)
        if y == -1 or y == self.nb_lines:
            y = (self.nb_lines-1 if y == -1 else 0)
        if [x, y] in self.otherSnake.get():
            self.alive = False
            print(f"DEAD: {self.name}")
            return
        if [x, y] != self.apple:
            old_x, old_y = self.snake.pop(0)
            self.draw_rect((old_x * self.square_dim, old_y * self.square_dim), self.bg_color)
        else:
            self.has_apple = True
            self.cpt += 1
            print("on top m8")
        if self.bapples and [x, y] in self.bapples:
            old_x, old_y = self.snake.pop(0)
            self.draw_rect((old_x * self.square_dim, old_y * self.square_dim), self.bg_color)
        self.draw_rect((self.snake[-1][0] * self.square_dim, self.snake[-1][1] * self.square_dim), self.body_color)
        self.snake.append([x, y])
        self.draw_rect((x * self.square_dim, y * self.square_dim), self.head_color)
        self.updated = True

    def draw_rect(self, position: tuple[int, int], color: pg.Color):
        pg.draw.rect(self.square_surface, color, self.square_surface.get_rect())
        self.screen.blit(self.square_surface, position)

    def draw(self):
        self.draw_rect((self.snake[-1][0] * self.square_dim, self.snake[-1][1] * self.square_dim), self.head_color)
        for x, y in self.snake[0:-1]:
            self.draw_rect((x * self.square_dim, y * self.square_dim), self.body_color)

    def setOtherSnake(self, snake: 'Snake'):
        self.otherSnake = snake

    def setColors(self, head: pg.Color, body: pg.Color):
        self.head_color = head
        self.body_color = body

    def addBapple(self, bapple_pos: list[int, int]):
        self.bapples.append(bapple_pos)


if __name__ == '__main__':
    Game(snake1_color="therock", snake2_color="outerworld")
