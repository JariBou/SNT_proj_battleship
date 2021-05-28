import tkinter.font as ft
from tkinter import *

from src.games import Battleship, Demineur, Last_letter_game, Pendu_gui, Rock_paper_scissors
from src.games.Chess import chess_launcher
from src.games.GameOfLife import run_gol
from src.games.Snake import run_snake
from src.games.TicTacToe import run_TTT as Runmorpion
from src.resources.utils.Constants import Constants as Ct


class run_main:

    def __init__(self):
        self.w = Tk()
        self.w.title("Game Library - Steam x86")
        self.w.config(bg="lightgray")
        self.path = Ct.get_path()
        self.w.iconbitmap(self.path.joinpath('resources\\images\\steam_icon.ico'))
        self.images = {'morpion': PhotoImage(file='resources\\images\\TicTacToe\\tictactoe.png'),
                       'battleship': PhotoImage(file='resources\\images\\Battleship\\battleship_icon.png'),
                       'chess': PhotoImage(file='resources\\images\\Chess\\taskbar_img_2.png'),
                       'GoL': PhotoImage(file='resources\\images\\GoL\\GoL_icon.png'),
                       'shifumi': PhotoImage(file='resources\\images\\rock_paper_scissors\\shifumi_icon.gif'),
                       'hangman': PhotoImage(file='resources\\images\\Hangman\\pendu_icon.gif'),
                       'demineur': PhotoImage(file='resources\\images\\Demineur\\mine.png'),
                       'snake': PhotoImage(file='resources\\images\\snake\\snake.png')}

        customFont = ft.Font(family='Source Sans Pro Black', size=20)
        customFont = ft.Font(family='Bahnschrift SemiBold', size=20)
        print(ft.families())

        # Set all buttons for apps
        buttonList = [
            Button(text="Morpion", image=self.images['morpion'], command=lambda: (self.w.destroy(), Runmorpion.run()),
                   font=customFont, compound='top'),
            Button(text="Battleship", image=self.images['battleship'],
                   command=lambda: (self.w.destroy(), Battleship.Battleship_1v1()),
                   font=customFont, compound='top'),
            Button(text="Échecs", image=self.images['chess'], command=lambda: (self.w.destroy(), chess_launcher.Launcher()),
                   font=customFont, compound='top'),
            Button(text="Jeu de la Vie", image=self.images['GoL'], command=lambda: (self.w.destroy(), run_gol.run()), font=customFont, compound='top'),
            Button(text="Dernière Lettre", command=lambda: (self.w.destroy(), Last_letter_game.Last_letter()),
                   font=customFont, compound='top'),
            Button(text="Shifumi", image=self.images['shifumi'],
                   command=lambda: (self.w.destroy(), Rock_paper_scissors.Game()),
                   font=customFont, compound='top'),
            Button(text="Hangman", image=self.images['hangman'],
                   command=lambda: (self.w.destroy(), Pendu_gui.Game('Lexique')),
                   font=customFont, compound='top'),
            Button(text="Démineur", image=self.images['demineur'], command=lambda: (self.w.destroy(), Demineur.Game()),
                   font=customFont, compound='top'),
            Button(text="Snake", image=self.images['snake'], command=lambda: (self.w.destroy(), run_snake.Launcher()),
                   font=customFont, compound='top')]

        size = 3
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
        print('hello')
        input()
        while True:
            pass


if __name__ == '__main__':
    run_main()
