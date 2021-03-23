import ctypes
from pathlib import Path
from random import randint
import tkinter as tk
import sys as system


class Last_letter:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Last letter - Alpha V0.1")
        self.root.protocol("WM_DELETE_WINDOW", lambda: system.exit("User cancelation"))
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.width, self.height = screen_width / 1.25, screen_height / 1.25
        ## calculate x and y coordinates for the window to be opened at
        x = (screen_width / 2) - (self.width / 2)
        y = (screen_height / 2) - (self.height / 2)
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))
        ## Add Icon
        myappid = 'mjcorp.battleship.alphav1.2'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.path = Path(__file__).parent.parent

        self.alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                         "t",
                         "u", "v", "w", "x", "y", "z"]
        self.voyelles = ["a", "e", "i", "o", "u"]
        self.cons = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t",
                     "v", "w", "x", "y", "z"]

        self.used = []

        self.input_field = tk.Entry(self.root)
        self.input_field.grid(row=3, column=0)

        self.print_input = tk.Button(self.root, text='print_input', command=self.print_input_to_console)
        self.print_input.grid(row=4, column=0)

        self.player_input = ''
        self.first_letter = self.alphabet[randint(0, 26)]
        print("First letter: ", self.first_letter)
        self.mots = []
        self.dernier = None
        self.points = 0
        self.turns_count = 1

        self.root.mainloop()

    def print_input_to_console(self):
        self.player_input = self.input_field.get()
        print(self.player_input)
        self.input_field.delete(0, len(self.player_input))
        self.turn()

    def turn(self):
        if self.player_input not in self.used:
            self.used.append(self.player_input)
        else:
            ## Word already used
            pass
        pass


if __name__ == '__main__':
    Last_letter()
