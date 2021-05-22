import copy
import time
from abc import ABC
from typing import Union

import pygame as pg

from src.resources.utils.Constants import Position


class GuiHandler:

    def __init__(self, screen, square_dim):
        self.screen = screen
        self.square_dim = square_dim
        self.square_surface = pg.Surface((square_dim, square_dim))

    def draw_rect(self, position: tuple[int, int], color: pg.Color):
        col = (position[0] - 1) * self.square_dim
        line = (position[1] - 1) * self.square_dim
        pg.draw.rect(self.square_surface, color, self.square_surface.get_rect())
        self.screen.blit(self.square_surface, (col, line))


class Spaceship:
    position: Position
    color: pg.Color
    bullet_color: pg.Color
    lives: int

    def __init__(self, position: Position, color: pg.Color, bullet_color: pg.Color, screen_args: tuple):
        self.position = position
        self.gun_position = Position([position.x, position.y-1])
        self.color = color
        self.lives = 3
        self.bullet_color = bullet_color
        self.active_bullets = []
        self.Gh = GuiHandler(screen_args[0], screen_args[1])

    def set_color(self, color: pg.Color):
        self.color = color

    def shot(self):
        self.active_bullets.append(Bullet(1, self.gun_position, self.bullet_color, self.Gh))

    def update_bullets(self):
        for i in range(4):
            for bullet in self.active_bullets:
                bullet.move()
                pg.display.update()
            time.sleep(1)

    def draw_spaceship(self):
        self.Gh.draw_rect((self.position.x, self.position.y), self.color)


class Bullet:
    size: int
    position: Position
    color: pg.Color
    old_pos: Union[Position, None]

    def __init__(self, size: int, position: Position, color: pg.Color, guihandler: GuiHandler):
        self.size = size
        self.position = position
        self.old_pos = None
        self.color = color
        self.Gh = guihandler

    def move(self):
        self.draw_bullet()
        self.old_pos = copy.deepcopy(self.position)
        self.remove_bullet()
        self.position.add('y=-1')
        self.draw_bullet()
        self.old_pos = None

    def draw_bullet(self):
        self.Gh.draw_rect((self.position.x, self.position.y), self.color)

    def remove_bullet(self):
        self.Gh.draw_rect((self.position.x, self.position.y), pg.Color(0, 0, 0))


class Game:

    def __init__(self):
        self.nb_columns = 20
        self.nb_lines = 20
        self.square_dim = 10
        self.square_size = (self.square_dim, self.square_dim)
        self.square_surface = pg.Surface(self.square_size)
        self.root = pg.Surface((self.nb_columns * self.square_dim, self.nb_lines * self.square_dim))
        self.screen = pg.display.set_mode((self.nb_columns * self.square_dim, self.nb_lines * self.square_dim))
        pg.display.set_caption('Game Of Life V3 - idle')
        pg.display.flip()

        spaceship = Spaceship(Position([6, 6]), pg.Color(255, 255, 255), pg.Color(255, 0, 0), (self.screen, self.square_dim))
        spaceship.draw_spaceship()
        spaceship.shot()
        spaceship.update_bullets()

        running = True
        while running:
            for event in pg.event.get():
                pass
            pg.display.update()


if __name__ == '__main__':
    Game()
