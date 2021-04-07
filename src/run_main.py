from tkinter import *
import tkinter.font as ft
from src.games.MorpionSolo import MorpionSolo
from src.games.MorpionMulti import MorpionMulti
import src.games.run_TTT as runmorpion


class run:

    def __init__(self):
        self.w = Tk()
        self.w.title("Choose GameMode")
        self.w.config(bg="lightgray")

        w = 700  # width for the Tk root
        h = 700  # height for the Tk root

        # get screen width and height
        ws = self.w.winfo_screenwidth()  # width of the screen
        hs = self.w.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.w.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.w.columnconfigure(0, minsize=130)
        self.w.columnconfigure(1, minsize=150)
        self.w.rowconfigure(0, minsize=150)

        customFont = ft.Font(size=20)

        # Set all buttons for apps

        morpion = Button(text="Morpion", font=customFont)
        morpion.grid(row=0, column=0, sticky="nsew")
        battleship = Button(text="Battleship", font=customFont)
        battleship.grid(row=0, column=1, sticky="nsew")
        chess = Button(text="Chess",font=customFont)
        chess.grid(row=0, column=2, sticky="nsew")
        gameoflife = Button(text="Jeu de la Vie", font=customFont)
        gameoflife.grid(row=0, column=3, sticky="nsew")
        last_letter = Button(text="Dernière Lettre", font=customFont)
        last_letter.grid(row=1, column=0, sticky="nsew")
        rockps = Button(text="Shifumi", font=customFont)
        rockps.grid(row=1, column=1, sticky="nsew")
        lastgame = Button(text="???", font=customFont)
        lastgame.grid(row=1, column=2, sticky="nsew")



        self.w.mainloop()

    def morpion(self):
        self.w.destroy()
        runmorpion()

    def single(self):
        self.w.destroy()
        MorpionSolo()

    def multi(self):
        self.w.destroy()
        MorpionMulti()


if __name__ == '__main__':
    run()
