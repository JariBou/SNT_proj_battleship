import ctypes
import random
import sys as system
import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk
from src.resources.utils.Constants import Constants as Ct

def about():
    messagebox.showinfo(title="About", message="Made by: Jari & LeTiramissou\n "
                                               "Version: Alpha 1.2")

def g_help():
    messagebox.showinfo(title="About", message="Le but est de deviner le mot avant que le monsieur\n"
                                               "soit ignoblement pendu\n\n"
                                               "Vous pouvez utiliser le clavier pour tenter une lettre")

def get_img(path, size=0):
    img = Image.open(path)
    if size != 0:
        img = img.resize((size, size))
    photo = ImageTk.PhotoImage(img)
    return photo


def stat(text):
    dico = []
    for char in text:
        if char not in [" ", ",", ";", ":", "'", "\"", "(", ")", "!", "?"]:
            dico.append(char)
    return dico


def lines_as_str(lines, space=" "):
    text = ""
    for i in lines:
        text += i + space
    return text


class Game:

    def __init__(self, fileName):
        self.fileName = fileName
        ## Window creation
        self.root = tk.Tk()
        self.root.title("Pendu - Alpha V1.2")
        self.root.protocol("WM_DELETE_WINDOW", system.exit)
        w = 800
        h = 600
        ## get screen width and height
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.root.config(bg='white')
        for lettre in range(26):
            self.root.bind(f"<KeyPress-{chr(65+lettre).lower()}>", self.on_key_press)

        #Add a menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar, bg='white')
        self.create_menu(menubar)

        ## Add Icon
        myappid = 'mjcorp.pendu.alphav1.2'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.path = Ct.get_path()
        self.root.iconbitmap(self.path.joinpath('resources\\images\\Hangman\\Pendu.ico'))

        self.mots = []
        with open(self.path.joinpath('resources\\txt_files\\' + (fileName if fileName.endswith(".txt") else fileName + ".txt")), "r") as f:
            for line in f:
                self.mots.append(line.replace("\n", ""))
        self.wrong = 0
        self.already_used = []
        self.word = self.mots[random.randint(0, len(self.mots))]
        self.letters = stat(self.word)
        self.nb_letters = len(self.word)
        self.lines = ['_'] * self.nb_letters
        self.button_list = []
        for i in range(26):
            a = tk.Button(self.root, text=chr(65+i))
            a['command'] = lambda b=a: self.clicked(b)
            a.pack(side=tk.LEFT, anchor='nw')
            self.button_list.append(a)

        self.restart_button = tk.Button(self.root, text='Restart', command=self.restart)
        self.restart_button.pack(side=tk.RIGHT, anchor='nw')

        self.quit_button = tk.Button(self.root, text='Quit', command=system.exit)
        self.quit_button.pack(side=tk.RIGHT, anchor='nw')

        self.canvas = tk.Canvas(self.root, height=500, width=630, bg='white', border=0, highlightthickness=0)
        self.canvas.place(x=100, y=50)

        self.pendu_img = [get_img(self.path.joinpath(f'resources\\images\\Hangman\\pendu_{nb}.gif')) for nb in range(8)]

        self.img_label = tk.Label(self.canvas, image=self.pendu_img[0], border=0)
        self.img_label.place(x=0, y=140)

        self.word_label = self.canvas.create_text(300, 60, text=lines_as_str(self.lines), font='Courrier 30')
        self.root.mainloop()

    def clicked(self, button):
        letter = button['text']
        is_in_word = False

        if button.cget('state') == tk.DISABLED:
            return

        for n in range(self.nb_letters):
            if letter == self.letters[n]:
                self.lines[n] = self.letters[n]
                is_in_word = True
        if not is_in_word:
            self.wrong += 1
        self.test_win()
        self.update_gui()
        button.config(state=tk.DISABLED)
        self.canvas.delete(self.word_label)
        self.word_label = self.canvas.create_text(300, 60, text=lines_as_str(self.lines), font='Courrier 30')

    def update_gui(self):
        self.img_label.config(image=self.pendu_img[self.wrong])

    def restart(self):
        self.root.destroy()
        Game(self.fileName)

    def test_win(self):
        if self.test_full():
            self._over()
        elif self.wrong > 6:
            self._over()

    def _over(self):
        for button in self.button_list:
            button.config(state=tk.DISABLED)

    def test_full(self):
        return '_' not in self.lines

    def on_key_press(self, event):
        key_pressed = repr(event.char).replace("'", '', 2)
        self.clicked(self.button_list[ord(key_pressed.upper()) - ord('A')])

    def on_key_press_repeat(self, event):
        self.on_key_press(event)

    def create_menu(self, menubar: tk.Menu):
        menubar.add_command(label="Help", command=g_help)
        menubar.add_command(label="About", command=about)

if __name__ == '__main__':
    Game("lexique")
