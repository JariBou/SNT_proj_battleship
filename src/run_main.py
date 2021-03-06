import tkinter.font as ft
from tkinter import *
import ctypes
import sys as system

from src.games import Battleship, Demineur, Last_letter_game, Pendu_gui, Rock_paper_scissors, Othello
from src.games.BlackJack import BlackJack
from src.games.Chess import chess_launcher
from src.games.GameOfLife import run_gol
from src.games.Snake import run_snake, start_snake
from src.games.TicTacToe import run_TTT as Runmorpion
from src.resources.utils.Constants import clean_path, Constants as Ct


class run_main:

    def __init__(self):
        self.w = Tk()
        self.w.title("Game Library - Steam x86")
        self.w.config(bg="lightgray")
        self.w.protocol("WM_DELETE_WINDOW", lambda: system.exit("User cancelation"))
        self.path = Ct.get_path()
        self.images = {'morpion': Ct.get_square_img(clean_path('resources\\images\\TicTacToe\\tictactoe.png')),
                       'battleship': Ct.get_square_img(clean_path('resources\\images\\Battleship\\battleship_icon.png')),
                       'chess': Ct.get_square_img(clean_path('resources\\images\\Chess\\taskbar_img_2.png')),
                       'GoL': Ct.get_square_img(clean_path('resources\\images\\GoL\\GoL_icon.png')),
                       'shifumi': Ct.get_square_img(clean_path('resources\\images\\rock_paper_scissors\\shifumi_icon.gif')),
                       'hangman': Ct.get_square_img(clean_path('resources\\images\\Hangman\\pendu_icon.gif')),
                       'demineur': Ct.get_square_img(clean_path('resources\\images\\Demineur\\mine.png')),
                       'snake': Ct.get_square_img(clean_path('resources\\images\\snake\\snake.png')),
                       'othello': Ct.get_square_img(clean_path('resources\\images\\Othello\\taskbar_ico_img.png'), size=128),
                       'lastletter': Ct.get_square_img(clean_path('resources\\images\\LastLetter\\LettersIco_img.png'), size=128),
                       'blackjack': Ct.get_rectangle_img(clean_path('resources\\images\\BlackJack\\roi_trefle.gif'), height=128, width=96)}

        myappid = 'mjcorp.launcher.alphav1.1'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.w.iconbitmap(self.path.joinpath('resources\\images\\steam_icon.ico'))

        customFont = ft.Font(family='Bahnschrift SemiBold', size=20)
        print(ft.families())

        # Set all buttons for apps
        buttonList = [
            Button(text="Morpion", image=self.images['morpion'], command=lambda: (self.w.destroy(), Runmorpion.run()),
                   font=customFont, compound='top'),
            Button(text="Battleship", image=self.images['battleship'],
                   command=lambda: (self.w.destroy(), Battleship.Battleship_1v1()),
                   font=customFont, compound='top'),
            Button(text="??checs", image=self.images['chess'], command=lambda: (self.w.destroy(), chess_launcher.Launcher()),
                   font=customFont, compound='top'),
            Button(text="Jeu de la Vie", image=self.images['GoL'], command=lambda: (self.w.destroy(), run_gol.run()), font=customFont, compound='top'),
            Button(text="Derni??re Lettre", image=self.images['lastletter'], command=lambda: (self.w.destroy(), Last_letter_game.Last_letter()),
                   font=customFont, compound='top'),
            Button(text="Shifumi", image=self.images['shifumi'],
                   command=lambda: (self.w.destroy(), Rock_paper_scissors.Game()),
                   font=customFont, compound='top'),
            Button(text="Hangman", image=self.images['hangman'],
                   command=lambda: (self.w.destroy(), Pendu_gui.Game('Lexique')),
                   font=customFont, compound='top'),
            Button(text="D??mineur", image=self.images['demineur'], command=lambda: (self.w.destroy(), Demineur.Game()),
                   font=customFont, compound='top'),
            Button(text="Snake", image=self.images['snake'], command=lambda: (self.w.destroy(), start_snake.run()),
                   font=customFont, compound='top'),
            Button(text="Othello", image=self.images['othello'], command=lambda: (self.w.destroy(), Othello.Game()),
                   font=customFont, compound='top'),
            Button(text="BlackJack", image=self.images['blackjack'], command=lambda: (self.w.destroy(), BlackJack.Launcher()),
                   font=customFont, compound='top')
            ]

        size = 4
        while len(buttonList) % size != 0:
            buttonList.append('None')

        buttonList = Ct.regroup_list(buttonList, size)

        exit_flag = False

        for row_index, row in enumerate(buttonList):
            self.w.rowconfigure(row_index, minsize=150)
            if exit_flag:
                break
            for index, button in enumerate(row):
                self.w.columnconfigure(index, minsize=150)
                if button == 'None':
                    exit_flag = True
                    break
                button.grid(row=row_index, column=index, sticky='nsew')

        Ct.center(self.w)

        self.w.mainloop()


if __name__ == '__main__':
    run_main()
