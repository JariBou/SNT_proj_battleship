## Code Cleaned Up ##
import ctypes
from tkinter import *
import tkinter.font as ft

from src import run_main
from src.games.TicTacToe.MorpionSolo import MorpionSolo
from src.games.TicTacToe.MorpionMulti import MorpionMulti
from src.resources.utils.Constants import Constants as Ct


class run:

    def __init__(self):
        self.w = Tk()
        self.w.title("Choose GameMode")
        self.w.config(bg="lightgray")

        ## Create a Menubar
        menubar = Menu(self.w)
        self.w.config(menu=menubar)
        menubar.add_command(label="Game Select Menu", command=lambda: [self.w.destroy(), run_main.run_main()])

        myappid = 'mjcorp.tictactoe.alphav1.1'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.path = Ct.get_path()
        self.w.iconbitmap(self.path.joinpath('resources\\images\\TicTacToe\\icon.ico'))
        self.w.resizable(width=False, height=False)

        customFont = ft.Font(size=20)
        single = Button(text="SinglePlayer", command=lambda: (self.w.destroy(), MorpionSolo()), font=customFont)
        single.grid(row=0, column=0, sticky="nsew")
        multi = Button(text="2Players", command=lambda: (self.w.destroy(), MorpionMulti()), font=customFont)
        multi.grid(row=0, column=1, sticky="nsew")

        Ct.center(self.w)
        w = self.w.winfo_width()
        h = self.w.winfo_height()
        print(w)
        self.w.columnconfigure(0, minsize=round(w / 2))
        self.w.columnconfigure(1, minsize=round(w / 2))
        self.w.rowconfigure(0, minsize=h)
        Ct.center(self.w)

        self.w.mainloop()


if __name__ == '__main__':
    run()
