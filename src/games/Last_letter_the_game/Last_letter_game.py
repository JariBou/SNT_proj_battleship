import ctypes
from pathlib import Path
from random import randint
import tkinter as tk
import sys as system
from tkinter import font, messagebox


# noinspection SpellCheckingInspection
def about():
    """ Used to display an about messageBox """
    messagebox.showinfo(title="About", message="Made by: Jari\n "
                                               "Version: Alpha V0.6")


def help():
    messagebox.showinfo(title="About", message="""Rules: You have to write a word that starts with the las letter of the previous word.
The game reminds you of the last written word and the last letter.
The game gives you the letter for the first word.
You can close the game at any moment by typing 'stop'
You can get the list of the words used by typing 'words'
Please keep in mind that you cannot use special characters nor uppercase letters.""")


class Last_letter:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Last letter - Alpha V0.6")
        self.root.protocol("WM_DELETE_WINDOW", lambda: system.exit("User cancelation"))
        w = 475
        h = 300
        ## get screen width and height
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        ## Add Icon
        myappid = 'mjcorp.lastword.alphav0.6'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.path = Path(__file__).parent.parent
        self.root.bind('<Return>', self.print_input_to_console)

        self.alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                         "t", "u", "v", "w", "x", "y", "z"]
        self.voyelles = ["a", "e", "i", "o", "u"]
        self.cons = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t",
                     "v", "w", "x", "y", "z"]

        self.used = []

        for i in range(3):
            self.root.rowconfigure(i, minsize=75)
            self.root.columnconfigure(i, minsize=110)

        customLabelFont = font.Font(family="Times", size=13)

        self.mylist = tk.Listbox(self.root)
        self.mylist.grid(row=1, column=4)

        ## Create a Menubar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        # diffmenu = tk.Menu(menubar, tearoff=0)
        menubar.add_command(label="Help", command=help)
        menubar.add_command(label="About", command=about)

        self.first_letter = self.alphabet[randint(0, 25)]
        self.letter_display = tk.Label(self.root, text=f"First letter: {self.first_letter}", font=customLabelFont, borderwidth=3, relief='sunken')
        self.letter_display.grid(row=0, column=0, sticky='nsew')

        self.last_word = 'None'
        self.last_word_display = tk.Label(self.root, text=f"Last Word: {self.last_word}", font=customLabelFont, borderwidth=3, relief='sunken')
        self.last_word_display.grid(row=0, column=1, sticky='nsew')

        self.points = 0
        self.points_display = tk.Label(self.root, text=f"Points: {self.points}", font=customLabelFont, borderwidth=3, relief='sunken')
        self.points_display.grid(row=0, column=2, sticky='nsew')

        self.console_output = tk.Label(self.root, text='', font=customLabelFont, borderwidth=3, relief='sunken')
        self.console_output.grid(row=1, column=0, sticky='nsew', columnspan=3)

        self.input_field = tk.Entry(self.root, bd=5)
        self.input_field.grid(row=2, column=1)

        self.enter_word_label = tk.Label(self.root, text='Enter a word:', font=customLabelFont)
        self.enter_word_label.grid(row=2, column=0)

        self.print_input = tk.Button(self.root, text='print_input', command=self.print_input_to_console)
        self.print_input.grid(row=3, column=0)

        self.player_input = ''
        self.mots = []
        self.points = 0
        self.turns_count = 1

        self.root.mainloop()

    def print_input_to_console(self, event):
        self.console_output.config(text="")
        self.player_input = self.input_field.get()
        print(self.player_input)
        self.input_field.delete(0, len(self.player_input))
        self.turn()

    def turn(self):
        if not self.test_word(self.player_input):
            ## Wrong input
            return
        elif self.player_input not in self.used:
            word_points = self.get_word_points(self.player_input)
            self.mylist.insert(tk.END, f"{self.player_input}     {word_points}")
            self.last_word = self.player_input
            self.used.append(self.player_input)
            self.first_letter = self.player_input[-1]
            self.points += word_points
            self.update_gui()
        else:
            ## Word already used
            pass
        pass

    def update_gui(self):
        self.letter_display.config(text=f"First letter: {self.first_letter}")
        self.points_display.config(text=f"Points: {self.points}")
        self.last_word_display.config(text=f"Last Word: {self.last_word}")
        self.player_input = ''

    def test_word(self, w):
        lon = len(w)
        if lon == 1:
            self.console_output.config(text="Please use words longer than 1 letter, c'mon")
            print("Please use words longer than 1 letter, c'mon")
            return False
        for i in range(0, lon):
            if w[i] not in self.alphabet:
                self.console_output.config(text="Nope, You cannot use special characters")
                print("Nope, You cannot use special characters")
                return False
        return True

    def get_word_points(self, word):
        points = 0
        for letter in word:
            if letter == 'y':
                points += 5
            elif letter == 'w':
                points += 4
            elif letter in self.voyelles:
                points += 3
            elif letter in self.cons:
                points += 2
        return points


if __name__ == '__main__':
    Last_letter()
