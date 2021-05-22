## Code Cleaned Up ##

from tkinter import *
import tkinter.font as ft

from src import run_main
from src.games.TicTacToe.MorpionSolo import MorpionSolo
from src.games.TicTacToe.MorpionMulti import MorpionMulti


class run:

    def __init__(self):
        self.w = Tk()
        self.w.title("Choose GameMode")
        self.w.config(bg="lightgray")

        w = 350  # width for the Tk root
        h = 200  # height for the Tk root

        # get screen width and height
        ws = self.w.winfo_screenwidth()  # width of the screen
        hs = self.w.winfo_screenheight()  # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        # set the dimensions of the screen
        # and where it is placed
        self.w.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.w.columnconfigure(0, minsize=round(w/2))
        self.w.columnconfigure(1, minsize=round(w/2))
        self.w.rowconfigure(0, minsize=h)

        ## Create a Menubar
        menubar = Menu(self.w)
        self.w.config(menu=menubar)
        menubar.add_command(label="Game Select Menu", command=lambda: [self.w.destroy(), run_main.run_main()])

        customFont = ft.Font(size=20)
        single = Button(text="SinglePlayer", command=self.single, font=customFont)
        single.grid(row=0, column=0, sticky="nsew")
        multi = Button(text="2Players", command=self.multi, font=customFont)
        multi.grid(row=0, column=1, sticky="nsew")

        self.w.mainloop()

    def single(self):
        self.w.destroy()
        MorpionSolo()

    def multi(self):
        self.w.destroy()
        MorpionMulti()


if __name__ == '__main__':
    run()
