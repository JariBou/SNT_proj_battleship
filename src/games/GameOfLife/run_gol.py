## Code Cleaned Up ##

from tkinter import *
import tkinter.font as ft

from src import run_main
from src.games.GameOfLife import GameOfLife, GameOfLifeV2, GameOfLifeV3
from src.resources.utils.Constants import Constants as Ct


class run:

    def __init__(self):
        self.w = Tk()
        self.w.title("Choose Version")
        self.w.config(bg="lightgray")

        ## Create a Menubar
        menubar = Menu(self.w)
        self.w.config(menu=menubar)
        menubar.add_command(label="Game Select Menu", command=lambda: [self.w.destroy(), run_main.run_main()])

        customFont = ft.Font(size=20)
        V1 = Button(text="V1.0", command=lambda: (self.w.destroy(), GameOfLife.GameOfLife()), font=customFont)
        V1.grid(row=0, column=0, sticky="nsew")
        V2 = Button(text="V2.0", command=lambda: (self.w.destroy(), GameOfLifeV2.Game()), font=customFont)
        V2.grid(row=0, column=1, sticky="nsew")
        V3 = Button(text="V3.0", command=lambda: (self.w.destroy(), GameOfLifeV3.Game()), font=customFont)
        V3.grid(row=0, column=2, sticky="nsew")

        Ct.center(self.w)
        w = self.w.winfo_width()
        h = self.w.winfo_height()
        print(w)
        for i in range(3):
            self.w.columnconfigure(i, minsize=round(w / 2))
        self.w.rowconfigure(0, minsize=h)
        Ct.center(self.w)

        self.w.mainloop()


if __name__ == '__main__':
    run()
