import ctypes
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
        screen = pg.display.set_mode((300, 300))
        pg.display.set_caption('Game Of Life V3')
        pg.display.flip()

        self.t1 = None
        self.playing = False
        self.placing = False

        size = (50, 50)

        WHITE = pg.Color(255, 255, 255)
        RED = pg.Color(255, 0, 0)

        rect_border = pg.Surface(size)  # Create a Surface to draw on.
        pg.draw.rect(rect_border, RED, rect_border.get_rect(), 10)  # Draw on it.

        rect_filled = pg.Surface(size)
        pg.draw.rect(rect_filled, RED, rect_filled.get_rect())

        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            screen.blit(rect_filled, (25, 25))
            screen.blit(rect_border, (25, 25))
            pg.display.update()

    def exit_game(self):
        self.playing = False
        if self.t1 is not None:
            self.t1.join()
        time.sleep(1)
        system.exit('User cancelation')

    def create_menu(self, menubar: tk.Menu):
        menubar.add_command(label="Help", command=g_help)
        menubar.add_command(label="About", command=about)
        # menubar.add_command(label="Stats", command=self.stats)
        #menubar.add_command(label="Game Select Menu", command=lambda: [self.root.destroy(), run_main.run_main()])


if __name__ == '__main__':
    Game()
