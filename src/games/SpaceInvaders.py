import copy
import threading
import time
from typing import Union

import pygame as pg

from src.resources.utils.Constants import Position


class GuiHandler:

    def __init__(self, screen, square_dim, collines: tuple[int, int]):
        self.screen = screen
        self.square_dim = square_dim
        self.square_surface = pg.Surface((square_dim, square_dim))
        self.nb_columns, self.nb_lines = collines

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
    board: Union[dict, None]

    def __init__(self, position: Position, color: pg.Color, bullet_color: pg.Color, guihandler: GuiHandler):
        self.position = position
        self.gun_position = Position([position.x, position.y-1])
        self.color = color
        self.lives = 3
        self.bullet_color = bullet_color
        self.active_bullets = []
        self.active_obstacles = []
        self.Gh = guihandler
        self.board = None
        self.t1 = None

    def set_color(self, color: pg.Color):
        self.color = color

    def shot(self):
        bullet = Bullet(1, copy.deepcopy(self.gun_position), self.bullet_color, self.Gh)
        bullet.draw_bullet()
        self.board[self.gun_position.x, self.gun_position.y] = bullet
        bullet.pass_board(self.board)
        self.active_bullets.append(bullet)

    def update_start(self):
        self.t1 = threading.Thread(target=self.update_bullets)
        self.t1.start()

    def update_bullets(self):
        while True:
            obstacles = [ob for ob in self.board.values() if isinstance(ob, Obstacle)]

            for obstacle in obstacles:
                obstacle.pass_board(self.board)
                obstacle.move()

            bullets = [bullet for bullet in self.board.values() if isinstance(bullet, Bullet)]
            obstacles_pos = [ob.position.get_position() for ob in self.board.values() if isinstance(ob, Obstacle)]
            for bullet in bullets:
                bullet.pass_board(self.board)
                if bullet.position.get_position() in obstacles_pos:
                    self.board[bullet.position.x, bullet.position.y] = ''
                    continue
                elif not bullet.move():
                    self.board[bullet.position.x, bullet.position.y - 1] = ''
                    self.board[bullet.position.x, bullet.position.y] = ''

            pg.display.update()
            time.sleep(0.25)

    def draw_spaceship(self):
        self.Gh.draw_rect((self.position.x, self.position.y), self.color)

    def remove_spaceship(self):
        self.Gh.draw_rect((self.position.x, self.position.y), pg.Color(0, 0, 0))

    def pass_board(self, board: dict):
        self.board = board

    def create_obstacle(self):
        obstacle = Obstacle(1, Position([self.position.x, 0]), pg.Color(0, 105, 0), self.Gh)
        obstacle.draw_obstacle()
        self.board[self.position.x, 0] = obstacle
        obstacle.pass_board(self.board)
        self.active_obstacles.append(obstacle)

    def move_ship(self, direction: str):
        self.remove_spaceship()
        if direction == 'right':
            if self.position.x + 1 < self.Gh.nb_columns + 1:
                self.position.add('x=1')
                self.gun_position.add('x=1')
        elif direction == 'left':
            if self.position.x - 1 > 0:
                self.position.add('x=-1')
                self.gun_position.add('x=-1')
        elif direction == 'up':
            if self.position.y - 1 > 0:
                self.position.add('y=-1')
                self.gun_position.add('y=-1')
        elif direction == 'down':
            if self.position.y + 1 < self.Gh.nb_lines + 1:
                self.position.add('y=1')
                self.gun_position.add('y=1')
        self.draw_spaceship()


class Bullet:
    size: int
    position: Position
    color: pg.Color
    old_pos: Union[Position, None]
    board: Union[dict, None]

    def __init__(self, size: int, position: Position, color: pg.Color, guihandler: GuiHandler):
        self.size = size
        self.position = position
        self.old_pos = None
        self.color = color
        self.Gh = guihandler
        self.board = None

    def move(self) -> bool:
        if self.position.y == 1:
            self.remove_bullet()
            return False
        if isinstance(self.board[self.position.x, self.position.y-1], Obstacle):
            print('hit wall')
            self.remove_bullet()
            self.board[self.position.x, self.position.y-1] = ''
            self.board[self.position.x, self.position.y] = ''
            self.Gh.draw_rect((self.position.x, self.position.y-1), pg.Color(0, 0, 0))
            return False
        self.old_pos = copy.deepcopy(self.position)
        self.remove_bullet()
        self.position.add('y=-1')
        self.draw_bullet()
        self.old_pos = None
        return True

    def draw_bullet(self):
        self.Gh.draw_rect((self.position.x, self.position.y), self.color)

    def remove_bullet(self):
        self.Gh.draw_rect((self.position.x, self.position.y), pg.Color(0, 0, 0))

    def pass_board(self, board: dict):
        self.board = board


class Obstacle:
    size: int
    position: Position
    color: pg.Color
    old_pos: Union[Position, None]
    board: Union[dict, None]

    def __init__(self, size: int, position: Position, color: pg.Color, guihandler: GuiHandler):
        self.size = size
        self.position = position
        self.old_pos = None
        self.color = color
        self.Gh = guihandler
        self.board = None

    def move(self) -> bool:
        if self.position.y == self.Gh.nb_lines+1:
            self.remove_obstacle()
            self.board[self.position.x, self.position.y] = ''
            return False
        self.old_pos = copy.deepcopy(self.position)
        self.board[self.position.x, self.position.y] = ''
        self.remove_obstacle()
        self.position.add('y=1')
        self.board[self.position.x, self.position.y] = self
        self.draw_obstacle()
        self.old_pos = None
        return True

    def draw_obstacle(self):
        self.Gh.draw_rect((self.position.x, self.position.y), self.color)

    def remove_obstacle(self):
        self.Gh.draw_rect((self.position.x, self.position.y), pg.Color(0, 0, 0))

    def pass_board(self, board: dict):
        self.board = board


class Game:

    def __init__(self):
        self.nb_columns = 40
        self.nb_lines = 40
        self.square_dim = 6
        self.square_size = (self.square_dim, self.square_dim)
        self.square_surface = pg.Surface(self.square_size)
        self.root = pg.Surface((self.nb_columns * self.square_dim, self.nb_lines * self.square_dim))
        self.screen = pg.display.set_mode((self.nb_columns * self.square_dim, self.nb_lines * self.square_dim))
        pg.display.set_caption('Space Invaders pre-alpha')
        pg.display.flip()
        self.board = {}
        for x in range(1, self.nb_columns + 1):
            for y in range(1, self.nb_lines + 1):
                self.board[x, y] = f'none at {x, y}'

        self.Gh = GuiHandler(self.screen, self.square_dim, (self.nb_columns, self.nb_lines))

        self.board[6, 3] = 'wall'
        self.draw_walls()
        spaceship = Spaceship(Position([6, 8]), pg.Color(255, 255, 255), pg.Color(255, 0, 0), self.Gh)
        spaceship.draw_spaceship()
        spaceship.pass_board(self.board)
        spaceship.shot()
        spaceship.update_start()

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    # if event.key == pg.K_DOWN:
                    #     spaceship.move_ship('down')
                    # elif event.key == pg.K_UP:
                    #     spaceship.move_ship('up')
                    # elif event.key == pg.K_RIGHT:
                    #     spaceship.move_ship('right')
                    # elif event.key == pg.K_LEFT:
                    #     spaceship.move_ship('left')
                    if event.key == pg.K_SPACE:
                        spaceship.shot()
                    elif event.key == pg.K_c:
                        spaceship.create_obstacle()

            keys = pg.key.get_pressed()
            if keys[pg.K_DOWN]:
                spaceship.move_ship('down')
            elif keys[pg.K_UP]:
                spaceship.move_ship('up')
            elif keys[pg.K_RIGHT]:
                spaceship.move_ship('right')
            elif keys[pg.K_LEFT]:
                spaceship.move_ship('left')
            time.sleep(0.05)

            pg.display.update()

    def draw_walls(self):
        for key in self.board.keys():
            if self.board[key] == 'wall':
                self.Gh.draw_rect((key[0], key[1]), pg.Color(0, 0, 255))


if __name__ == '__main__':
    Game()
