import ctypes
from threading import Thread
import time
import tkinter as tk
import sys as system
import random
import pygame as pygame

from PIL.ImageTk import PhotoImage
from tkinter import messagebox

from src.resources.utils.Constants import Constants as Ct
from src import run_main


#####          STATIC METHODS          ####


def get_img(path):
    img = PhotoImage(file=path)
    return img


def g_help():
    messagebox.showinfo(title="Help & Rules", message="Cliquer sur une case de la grille révèle:\n\n"
                                                      "- Une zone ne contenant aucune mine\n"
                                                      "- Une case bordée par 1, 2, 3 ou 4 mines dans un rayon d'1\n"
                                                      "  case (verticalement, horizontalement, diagonalement\n")


def about():
    """ Used to display an about messageBox """
    messagebox.showinfo(title="About", message="Made by: Mathis & Jari \n "
                                               "Version: Alpha 0.1")


####                                  ####


class Game:
    nb_columns: int
    nb_lines: int
    nb_mines: int
    square_dim: int
    gap: int
    nb_seen_squares: int
    playing: bool

    def __init__(self):
        ## Window creation
        self.nb_mines = 0
        self.root = tk.Tk()
        self.root.title("Démineur - Alpha V1.0")
        self.root.protocol("WM_DELETE_WINDOW", self.exit_game)
        self.root.resizable(width=False, height=False)

        self.path = Ct.get_path()
        myappid = 'mjcorp.demineur.alphav1.0'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.root.iconbitmap(self.path.joinpath('resources\\images\\Demineur\\demineur_taskbar.ico'))

        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar, bg='white')
        self.create_menu(menubar)

        self.nb_columns, self.nb_lines, self.nb_mines = 10, 10, 0
        self.square_dim, self.gap, self.nb_seen_squares = 30, 3, 0
        self.playing = True
        self.games_played, self.wins, self.loses = 0, 0, 0

        self.t1: Thread = Thread()
        self.s_round = 0
        self.time_dict = {'minutes': 0, 'seconds': 0}

        self.images = {
            'cross': get_img(self.path.joinpath('resources\\images\\Demineur\\croixj.gif')),
            'flag': get_img(self.path.joinpath('resources\\images\\Demineur\\drapeauj.gif')),
            'mine1': get_img(self.path.joinpath('resources\\images\\Demineur\\mine.png')),
            'minej': get_img(self.path.joinpath('resources\\images\\Demineur\\minej.gif'))
            }

        self.mines: dict = {}
        self.player_board: dict = {}

        self.timer = tk.Label(self.root, text='Timer: --min --s')
        self.timer.pack()

        self.land_canvas = tk.Canvas(self.root, width=(self.square_dim * self.nb_columns) + self.gap,
                                     height=(self.square_dim * self.nb_lines) + self.gap, bg='grey')
        self.land_canvas.bind("<Button-1>", self.pointeurG)
        self.land_canvas.bind("<Button-3>", self.pointeurD)

        self.land_canvas.pack(side=tk.RIGHT)

        self.difficulty_frame = tk.Frame(self.root)

        self.difficulty = tk.IntVar()
        self.difficulty.set(1)

        radio1 = tk.Radiobutton(self.difficulty_frame, text='Noob', command=self.start, variable=self.difficulty,
                                value=1)
        radio1.pack(anchor='nw', padx=30)
        radio2 = tk.Radiobutton(self.difficulty_frame, text='Average', command=self.start, variable=self.difficulty,
                                value=2)
        radio2.pack(anchor='nw', padx=30)
        radio3 = tk.Radiobutton(self.difficulty_frame, text='U good dawg', command=self.start, variable=self.difficulty,
                                value=3)
        radio3.pack(anchor='nw', padx=30)
        radio4 = tk.Radiobutton(self.difficulty_frame, text='GOAT jr.', command=self.start, variable=self.difficulty,
                                value=4)
        radio4.pack(anchor='nw', padx=30)
        radio5 = tk.Radiobutton(self.difficulty_frame, text='xXx_GOAT_xXx', command=self.start,
                                variable=self.difficulty, value=5)
        radio5.pack(anchor='nw', padx=30)
        radio6 = tk.Radiobutton(self.difficulty_frame, text='INSANE360', command=self.start, variable=self.difficulty,
                                value=6)
        radio6.pack(anchor='nw', padx=30)
        self.difficulty_frame.pack()

        self.info = tk.Frame(self.root)
        self.mine_count = tk.Label(self.info, text='Mines restantes: --')
        self.mine_count.grid(row=0, column=0, sticky='nw')  # 4
        self.squares_left = tk.Label(self.info, text='Cases restantes: --')
        self.squares_left.grid(row=1, column=0, sticky='nw')  # 5
        self.info.pack()

        self.volume = 0.8
        sound_frame = tk.Frame(self.root)
        w = tk.Scale(sound_frame, from_=0, to=100, orient=tk.HORIZONTAL, label="Change Volume")
        w['command'] = lambda w2=w: self.change_volume(w2)
        w.set(80)
        test_sound = tk.Button(sound_frame, text='Test Volume',
                               command=lambda: self.play(self.path.joinpath('resources\\sounds\\fail\\ah.mp3')))
        w.pack()
        test_sound.pack()
        sound_frame.pack(side=tk.RIGHT)

        self.new_game_frame = tk.Frame(self.root)
        self.restart_button = tk.Button(self.new_game_frame, width=15, text='New game', font='Arial 10',
                                        command=self.start)
        self.restart_button.pack(side=tk.BOTTOM, padx=5, pady=5)
        self.new_game_frame.pack(side=tk.BOTTOM)

        self.img_frame = tk.Frame(self.root)
        self.img_lab = tk.Label(self.img_frame, image=self.images.get('mine1'))
        self.img_lab.pack(side=tk.BOTTOM)
        self.img_frame.pack(side=tk.BOTTOM)

        self.hidden_mines = self.nb_mines
        self.colors = ['blue', 'orange', 'red', 'green', 'cyan', 'skyblue', 'pink']
        self.empty_colors = ['green', 'red', 'orange', 'yellow', 'cyan']
        self.sounds = {'win': [self.path.joinpath('resources\\sounds\\destroy\\amaterasu-sound-effect.mp3'),
                               self.path.joinpath('resources\\sounds\\destroy\\yes-yes-yes-yes.mp3')],
                       'lose': [self.path.joinpath('resources\\sounds\\fail\\bruh-sound-effect.mp3'),
                                self.path.joinpath('resources\\sounds\\fail\\oof-sound-effect.mp3'),
                                self.path.joinpath('resources\\sounds\\fail\\plouf.mp3'),
                                self.path.joinpath('resources\\sounds\\fail\\ah.mp3'),
                                self.path.joinpath('resources\\sounds\\fail\\hotel-mario-non.mp3')],
                       'void': [self.path.joinpath('resources\\sounds\\touch\\ha-got-emm-sound-effect.mp3'),
                                self.path.joinpath('resources\\sounds\\touch\\sharingan-sound-effect.mp3'),
                                self.path.joinpath('resources\\sounds\\touch\\sr-pelo-boom-sound-effect.mp3'),
                                self.path.joinpath('resources\\sounds\\touch\\wazaaaa.mp3')]}

        self.ratio_value = 'N/A'

        Ct.set_color(self.root, 'white')
        self.start()

        self.root.mainloop()

    def draw_separators(self, origine):
        x1 = origine
        y1 = origine
        y2 = y1 + (self.square_dim * self.nb_lines)
        x2 = x1 + (self.square_dim * self.nb_columns)
        for x in [x1 + self.square_dim * p for p in range(self.nb_columns + 1)]:
            self.land_canvas.create_line(x, y1, x, y2, width=2, fill='black')
        for y in [y1 + self.square_dim * p for p in range(self.nb_lines + 1)]:
            self.land_canvas.create_line(x1, y, x2, y, width=2, fill='black')

    def init_lvl(self):
        self.land_canvas.delete(tk.ALL)
        level = self.difficulty.get()
        self.time_dict = {'minutes': 0, 'seconds': 0}
        if level == 1:
            self.nb_columns, self.nb_lines, self.nb_mines = 10, 10, 12
        elif level == 2:
            self.nb_columns, self.nb_lines, self.nb_mines = 15, 15, 30
        elif level == 3:
            self.nb_columns, self.nb_lines, self.nb_mines = 20, 20, 50
        elif level == 4:
            self.nb_columns, self.nb_lines, self.nb_mines = 30, 30, 80
        elif level == 5:
            self.nb_columns, self.nb_lines, self.nb_mines = 30, 30, 150
        elif level == 6:
            self.nb_columns, self.nb_lines, self.nb_mines = 30, 30, 250

        self.land_canvas.config(width=(self.square_dim * self.nb_columns) + self.gap,
                                height=(self.square_dim * self.nb_lines) + self.gap)
        self.draw_separators(3)
        self.nb_seen_squares, self.hidden_mines = 0, self.nb_mines

    def start(self):
        self.playing = True
        self.init_lvl()
        for y in range(1, self.nb_lines + 1):
            for x in range(1, self.nb_columns + 1):
                self.mines[x, y] = 0
                self.player_board[x, y] = ""
                self.land_canvas.create_rectangle((x - 1) * self.square_dim + self.gap,
                                                  (y - 1) * self.square_dim + self.gap,
                                                  x * self.square_dim + self.gap, y * self.square_dim + self.gap,
                                                  width=0, fill='grey')
        self.draw_separators(3)
        nb_mines = 0
        while nb_mines < self.nb_mines:
            col = random.randint(1, self.nb_columns)
            line = random.randint(1, self.nb_lines)
            if self.mines[col, line] != 9:
                self.mines[col, line] = 9
                nb_mines += 1
        self.affiche_compteur()
        Ct.center(self.root)
        self.t1 = Thread(target=self.update_timer)
        self.t1.start()

    def affiche_compteur(self):
        self.mine_count.config(text=f'Mines restantes: {self.hidden_mines}')
        self.squares_left.config(text=f'Cases restantes:{(self.nb_columns * self.nb_lines) - self.nb_seen_squares}')

    def affiche_nb_mines(self, nb_mines_voisines, col, line):
        if self.player_board[col, line] == "":
            self.nb_seen_squares += 1
        elif self.player_board[col, line] == "d":
            self.hidden_mines += 1
            self.nb_seen_squares -= 1
            self.affiche_compteur()
        self.player_board[col, line] = nb_mines_voisines
        self.land_canvas.create_rectangle((col - 1) * self.square_dim + self.gap + 3,
                                          (line - 1) * self.square_dim + self.gap + 3,
                                          col * self.square_dim + self.gap - 3, line * self.square_dim + self.gap - 3,
                                          width=0, fill="ivory")
        self.land_canvas.create_text(col * self.square_dim - self.square_dim // 2 + self.gap,
                                     line * self.square_dim - self.square_dim // 2 + self.gap,
                                     text=f'{nb_mines_voisines}',
                                     fill=self.colors[nb_mines_voisines - 1], font='Arial 22')

    def get_neighbours(self, col, line) -> int:
        min_column = col - 1 if col > 1 else col
        max_column = col + 1 if col < self.nb_columns else col

        min_line = line - 1 if line > 1 else line
        max_line = line + 1 if line < self.nb_lines else line

        return len([key for key in self.mines.keys() if (self.mines[key] == 9)
                    & (min_line <= key[1] <= max_line)
                    & (min_column <= key[0] <= max_column)])

    def pointeurG(self, event):
        if not self.playing:
            return
        nCol = (event.x - self.gap) // self.square_dim + 1
        nLine = (event.y - self.gap) // self.square_dim + 1
        if not (1 <= nCol <= self.nb_columns and 1 <= nLine <= self.nb_lines):
            return
        # si la cellule est vide:
        if not self.player_board[nCol, nLine] == "":
            return

        if self.mines[nCol, nLine] == 9:
            self.lost(nCol, nLine)
            return

        nb_neightbour_mines = self.get_neighbours(nCol, nLine)
        if nb_neightbour_mines >= 1:
            self.affiche_nb_mines(nb_neightbour_mines, nCol, nLine)
            self.player_board[nCol, nLine] = "v"
        else:
            self.play(self.sounds.get('void')[random.randint(0, len(self.sounds.get('void')) - 1)])
            self.vide_plage_zero(nCol, nLine)

        self.affiche_compteur()

        if self.has_won():
            self.won()

    def vide_plage_zero(self, col, line):
        # c quand tu te mets sur un truc ou y'a pas de mines a coté et tu dois tout enlever TMTC
        if not (1 <= col <= self.nb_columns and 1 <= line <= self.nb_lines):
            return
        nb_neightbour_mines = self.get_neighbours(col, line)
        if self.player_board[col, line] == 'v':
            return
        if not nb_neightbour_mines:
            # self.land_canvas.create_rectangle((col - 1) * self.square_dim + self.gap + 3,
            #                                   (line - 1) * self.square_dim + self.gap + 3,
            #                                   col * self.square_dim + self.gap - 3,
            #                                   line * self.square_dim + self.gap - 3,
            #                                   width=0, fill="ivory")
            self.land_canvas.create_rectangle((col - 1) * self.square_dim + self.gap + 3,
                                              (line - 1) * self.square_dim + self.gap + 3,
                                              col * self.square_dim + self.gap - 3,
                                              line * self.square_dim + self.gap - 3,
                                              width=0, fill=self.colors[random.randint(0, len(self.empty_colors) - 1)])
            self.nb_seen_squares += 1
            self.player_board[col, line] = 'v'
            self.land_canvas.update_idletasks()
            self.vide_plage_zero(col + 1, line)
        else:
            self.affiche_nb_mines(nb_neightbour_mines, col, line)
            return
        self.vide_plage_zero(col, line + 1)
        self.vide_plage_zero(col, line - 1)
        self.vide_plage_zero(col - 1, line)
        # time.sleep(0.01)

        pass

    def pointeurD(self, event):
        if not self.playing:
            return
        nCol = (event.x - self.gap) // self.square_dim + 1
        nLine = (event.y - self.gap) // self.square_dim + 1
        if not (1 <= nCol <= self.nb_columns and 1 <= nLine <= self.nb_lines):
            return
        self.land_canvas.create_rectangle((nCol - 1) * self.square_dim + self.gap,
                                          (nLine - 1) * self.square_dim + self.gap,
                                          nCol * self.square_dim + self.gap, nLine * self.square_dim + self.gap,
                                          width=0, fill='grey')
        if self.player_board[nCol, nLine] == "":
            self.land_canvas.create_image(nCol * self.square_dim - self.square_dim // 2 + self.gap,
                                          nLine * self.square_dim - self.square_dim // 2 + self.gap,
                                          image=self.images.get('flag'))
            self.player_board[nCol, nLine] = "d"
            self.nb_seen_squares += 1
            self.hidden_mines -= 1
            if self.has_won():
                self.won()
        elif self.player_board[nCol, nLine] == "d":
            self.land_canvas.create_text(nCol * self.square_dim - self.square_dim // 2 + self.gap,
                                         nLine * self.square_dim - self.square_dim // 2 + self.gap, text='?',
                                         fill='black', font='Arial 20')
            self.player_board[nCol, nLine] = "?"
            self.nb_seen_squares -= 1
            self.hidden_mines += 1
        elif self.player_board[nCol, nLine] == '?':
            self.player_board[nCol, nLine] = ""
        self.draw_separators(3)
        self.affiche_compteur()

    def has_won(self) -> bool:
        if not (((self.nb_lines * self.nb_columns) == self.nb_seen_squares) and self.hidden_mines == 0):
            return False
        for y in range(1, self.nb_lines + 1):
            for x in range(1, self.nb_columns + 1):
                if self.mines[x, y] == 9 and self.player_board[x, y] != "d":
                    return False
        return True

    def won(self):
        self.playing = False
        for line in range(1, self.nb_lines + 1):
            for col in range(1, self.nb_columns + 1):
                if self.player_board[col, line] == "d":
                    self.land_canvas.create_image(col * self.square_dim - self.square_dim // 2 + self.gap,
                                                  line * self.square_dim - self.square_dim // 2 + self.gap,
                                                  image=self.images.get('cross'))
        self.land_canvas.create_text(int(self.land_canvas.cget('width')) // 2,
                                     int(self.land_canvas.cget('height')) // 2, fill="green",
                                     font="Times 35 italic bold", text="WON")
        self.games_played += 1
        self.ratio_value = ((self.wins // self.games_played) * 100)
        self.wins += 1

    def lost(self, nCol, nLine):
        self.play(self.sounds.get('lose')[random.randint(0, len(self.sounds.get('lose')) - 1)])
        for line in range(1, self.nb_lines + 1):
            for col in range(1, self.nb_columns + 1):
                if self.mines[col, line] != 9:
                    continue
                if self.player_board[col, line] == "d":
                    self.land_canvas.create_image(col * self.square_dim - self.square_dim // 2 + self.gap,
                                                  line * self.square_dim - self.square_dim // 2 + self.gap,
                                                  image=self.images.get('cross'))
                    continue
                self.land_canvas.create_image(col * self.square_dim - self.square_dim // 2 + self.gap,
                                              line * self.square_dim - self.square_dim // 2 + self.gap,
                                              image=self.images.get('minej'))
        self.land_canvas.create_image(nCol * self.square_dim - self.square_dim // 2 + self.gap,
                                      nLine * self.square_dim - self.square_dim // 2 + self.gap,
                                      image=self.images.get('cross'))
        self.playing = False
        self.land_canvas.create_text(int(self.land_canvas.cget('width')) // 2,
                                     int(self.land_canvas.cget('height')) // 2, fill="red",
                                     font="Times 35 italic bold", text="LOST")
        self.games_played += 1
        self.ratio_value = ((self.wins // self.games_played) * 100)
        self.loses += 1

    def stats(self):
        messagebox.showinfo(title="Stats", message=f"Games played: {self.games_played}\n "
                                                   f"Wins: {self.wins}\n"
                                                   f"Loses: {self.loses}\n"
                                                   f"Win ration: {self.ratio_value} \n")

    def update_timer(self):
        while self.playing:
            time.sleep(0.25)
            if not self.playing:
                return
            self.s_round += 1
            curr = self.time_dict
            if self.s_round == 2:
                curr['seconds'] += 0.5
                self.s_round = 0
            if curr['seconds'] >= 60:
                curr['minutes'] += 1
                curr['seconds'] = 0
            if not self.playing:
                return
            self.timer.config(text=f"{curr.get('minutes')}min {curr.get('seconds')}s")
        return

    def exit_game(self):
        self.playing = False
        if self.t1 is not None:
            self.t1.join()
        time.sleep(0.5)
        system.exit('User cancelation')

    def create_menu(self, menubar: tk.Menu):
        colorsettings = tk.Menu(menubar, tearoff=0)
        colorsettings.add_command(label="White (default)", command=lambda: Ct.set_color(self.root, 'white'))
        colorsettings.add_command(label="Light grey", command=lambda: Ct.set_color(self.root, 'lightgrey'))
        colorsettings.add_command(label="Grey", command=lambda: Ct.set_color(self.root, 'grey'))
        colorsettings.add_command(label="Light blue", command=lambda: Ct.set_color(self.root, 'lightblue'))
        menubar.add_cascade(label="Color settings", menu=colorsettings)
        menubar.add_command(label="Help", command=g_help)
        menubar.add_command(label="About", command=about)
        menubar.add_command(label="Stats", command=self.stats)
        menubar.add_command(label="Game Select Menu", command=lambda: [self.root.destroy(), run_main.run_main()])

    def play(self, path):
        """ Plays a sound
        :param path: Path to sound
        """
        pygame.init()
        pygame.mixer.music.load(path)  # Loading File Into Mixer
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()

    def change_volume(self, w):
        """ Changes the volume at which sounds are played
        :param w: slider value
        """
        self.volume = int(w) / 100


if __name__ == '__main__':
    Game()
