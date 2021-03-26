import ctypes
import threading
import time
from pathlib import Path
from random import randint
import tkinter as tk
import sys as system
from tkinter import font, messagebox

from src.resources.utils.Constants import Constants as Ct


# noinspection SpellCheckingInspection
def about():
    """ Used to display an about messageBox """
    messagebox.showinfo(title="About", message="Made by: Jari\n "
                                               "Version: Alpha V0.6")


def help():
    messagebox.showinfo(title="About", message="""Rules: You have to write a word that starts with the las letter of the previous word.
The game reminds you of the last written word and the last letter.
The game gives you the letter for the first word.
You can close the game at any moment by typing 'stop' or 'exit'
Once you fail 3 times you lose. 
Please keep in mind that you cannot use special characters nor uppercase letters.""")


def new_game(old_window=None):
    if old_window is not None:
        old_window.destroy()
    Last_letter()


class Last_letter:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Last letter - Alpha V0.6")
        self.root.protocol("WM_DELETE_WINDOW", self.exit_game)
        w = 550
        h = 310
        ## get screen width and height
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        ## Add Icon
        myappid = 'mjcorp.lastword.alphav0.6'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.path = Ct.get_path()
        self.root.bind('<Return>', self.print_input_to_console)

        self.alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                         "t", "u", "v", "w", "x", "y", "z"]
        self.voyelles = ["a", "e", "i", "o", "u"]
        self.cons = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t",
                     "v", "w", "x", "y", "z"]

        self.quiting = False

        self.used = []
        self.t1 = None

        for i in range(4):
            self.root.rowconfigure(i, minsize=75)
            self.root.columnconfigure(i, minsize=110)
        customLabelFont = font.Font(family="Times", size=13)

        scrollbar = tk.Scrollbar(self.root)
        scrollbar.grid(row=1, column=5, sticky='nsew')
        self.mylist = tk.Listbox(self.root, yscrollcommand=scrollbar.set)
        self.mylist.grid(row=1, column=3, columnspan=2, sticky='nsew')
        self.mylist.insert(tk.END, 'Word  +  Points')
        scrollbar.config(command=self.mylist.yview)

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
        self.last_word_display.grid(row=0, column=1, columnspan=2, sticky='nsew')

        self.points = 0
        self.points_display = tk.Label(self.root, text=f"Points: {self.points}", font=customLabelFont, borderwidth=3, relief='sunken')
        self.points_display.grid(row=0, column=3, sticky='nsew')

        self.next_game_button = tk.Button(self.root, text="New Game", font=customLabelFont, borderwidth=3, command=lambda: new_game(self.root))
        self.next_game_button.grid(row=0, column=4, sticky='nsew')

        self.console_output = tk.Label(self.root, text='', font=customLabelFont, borderwidth=3, relief='sunken')
        self.console_output.grid(row=1, column=0, sticky='nsew', columnspan=3)

        self.tries = 0
        self.input_field = tk.Entry(self.root, bd=5)
        self.input_field.grid(row=2, column=1, columnspan=2, sticky='ew')

        self.tries_state_button = tk.Label(self.root, text=f"Tries left: {3 - self.tries}", font=customLabelFont, borderwidth=3, relief='sunken')
        self.tries_state_button.grid(row=2, column=3, columnspan=2, sticky='nsew')

        self.enter_word_label = tk.Label(self.root, text='Enter a word:', font=customLabelFont)
        self.enter_word_label.grid(row=2, column=0)

        self.print_input = tk.Button(self.root, text='print_input', command=self.admin_command)
        self.print_input.grid(row=3, column=0)

        self.player_input = ''
        self.mots = []
        self.points = 0
        self.turns_count = 1

        self.root.mainloop()

    def admin_command(self):
        print(self.mylist.get(0, tk.END))

    def print_input_to_console(self, event):
        self.console_output.config(text="")
        self.player_input = self.input_field.get()
        print(self.player_input)
        self.input_field.delete(0, len(self.player_input))
        self.turn()

    def turn(self):
        if self.player_input in ['stop', 'exit']:
            self.exit_game()
        if not self.test_word(self.player_input):
            self.tries += 1
            ## Wrong input
        elif self.player_input not in self.used:
            word_points = self.get_word_points(self.player_input)
            self.mylist.insert(tk.END, f"{self.player_input}              {word_points}")
            self.last_word = self.player_input
            self.used.append(self.player_input)
            self.first_letter = self.player_input[-1]
            self.points += word_points
        else:
            self.console_output.config(text="You already used that word!")
            self.tries += 1
            ## Word already used
        self.update_gui()
        if 3 - self.tries == 0:
            self.input_field.config(state=tk.DISABLED)
            self.tries_state_button.config(text="Game Over", bg='red')
            self.t1 = threading.Thread(target=self.game_over, args=())
            self.t1.start()

    def update_gui(self):
        self.letter_display.config(text=f"First letter: {self.first_letter}")
        self.points_display.config(text=f"Points: {self.points}")
        self.last_word_display.config(text=f"Last Word: {self.last_word}")
        self.tries_state_button.config(text=f"Tries left: {3 - self.tries}")
        self.player_input = ''

    def test_word(self, w):
        lon = len(w)
        if lon == 1:
            self.console_output.config(text="Please use words longer than 1 letter, c'mon")
            print("Please use words longer than 1 letter, c'mon")
            return False
        elif self.player_input[0] != self.first_letter:
            self.console_output.config(text="Wrong first letter")
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

    def exit_game(self):
        self.quiting = True
        time.sleep(0.2)
        try:
            self.t1.join()
        except AttributeError:
            pass
        system.exit('User Cancelation')

    def game_over(self):
        while not self.quiting:
            try:
                self.tries_state_button.config(text="Game Over", bg='red')
                time.sleep(0.7)
                if self.quiting:   ## To fix window not exiting, main thread probably continues when time.sleep is called
                    return         ## So we need to check the more often possible
                self.tries_state_button.config(text="Press New Game", bg='red')
                time.sleep(0.7)
                if self.quiting:
                    return
                self.tries_state_button.config(text="To Continue", bg='red')
                time.sleep(0.7)
            except:
                return
        return


if __name__ == '__main__':
    a = Last_letter()
