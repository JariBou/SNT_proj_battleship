from tkinter import *
import tkinter.font as ft
from src.games import Battleship, Demineur, GameOfLife, Rock_paper_scissors, Pendu_gui, Last_letter_game, Snake
from src.resources.utils.Constants import Constants as Ct
from src.games.Chess import run_chess
from src.games.GameOfLife import run_gol
from src.games.TicTacToe import run_TTT as Runmorpion


class run_main:

    def __init__(self):
        self.w = Tk()
        self.w.title("Choose GameMode")
        self.w.config(bg="lightgray")
        self.path = Ct.get_path()
        self.images  = {'morpion':PhotoImage(file='resources\\images\\TicTacToe\\tictactoe.png'),
                        'battleship':PhotoImage(file='resources\\images\\Battleship\\battleship_icon.png'),
                        'chess':PhotoImage(file='resources\\images\\Chess\\taskbar_img_2.png'),
                        'shifumi':PhotoImage(file='resources\\images\\rock_paper_scissors\\shifumi_icon.gif'),
                        'hangman':PhotoImage(file='resources\\images\\Hangman\\pendu_icon.gif'),
                        'demineur':PhotoImage(file='resources\\images\\Demineur\\mine.png'),
                        'snake':PhotoImage(file='resources\\images\\snake\\snake.png')}

        """'GoL':Ct.get_img(self.path.joinpath('ressources\\images\\GoL\\GoL.png''))"""

        customFont = ft.Font(size=20)

        # Set all buttons for apps
        buttonList = [Button(text="Morpion", image=self.images['morpion'], command=lambda: (self.w.destroy(), Runmorpion.run()), font=customFont),
                      Button(text="Battleship", image=self.images['battleship'], command=lambda: (self.w.destroy(), Battleship.Battleship_1v1()),
                             font=customFont),
                      Button(text="Echecs", image=self.images['chess'], command=lambda: (self.w.destroy(), run_chess.ChessGui()), font=customFont),
                      Button(text="Jeu de la Vie", command=lambda: (self.w.destroy(), run_gol.run()), font=customFont),
                      Button(text="Dernière Lettre", command=lambda: (self.w.destroy(), Last_letter_game.Last_letter()),
                             font=customFont),
                      Button(text="Shifumi", image=self.images['shifumi'], command=lambda: (self.w.destroy(), Rock_paper_scissors.Game()),
                             font=customFont),
                      Button(text="Hangman", image=self.images['hangman'], command=lambda: (self.w.destroy(), Pendu_gui.Game('Lexique')),
                             font=customFont),
                      Button(text="Démineur", image=self.images['demineur'], command=lambda: (self.w.destroy(), Demineur.Game()), font=customFont),
                      Button(text="Snake", image=self.images['snake'], command=lambda: (self.w.destroy(), Snake.Game()), font=customFont)]

        size = 3
        while len(buttonList) % size != 0:
            buttonList.append('None')

        buttonList = Ct.regroup_list(buttonList, size)

        print(buttonList)
        exit_flag = False

        for row_index, row in enumerate(buttonList):
            print(row)
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
