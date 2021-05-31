import ctypes
import random
import tkinter as tk
import tkinter.font
from pathlib import Path
from tkinter import messagebox
from PIL import ImageTk, Image
from typing import Union

import pygame as pygame
import sys as system

from src import run_main
from src.resources.utils.Constants import Constants as Ct


#####          STATIC METHODS          ####
def get_img(path) -> ImageTk.PhotoImage:
    """ resources\\images\\XXX """
    img = Image.open(path)
    new_img = img.resize((44, 44))
    photo = ImageTk.PhotoImage(new_img)
    return photo


# noinspection SpellCheckingInspection
def about():
    """ Used to display an about messageBox """
    messagebox.showinfo(title="About", message="Made by: LeTiramissou & Jari\n "
                                               "Version: Alpha V2.0")


def g_help():
    """Used to display help_rules about the game"""
    messagebox.showinfo(title="Help & Rules", message="Commencer une partie de bataille navale \n"
                                                      "---------------------------------------\n"
                                                      "Au début du jeu, chaque joueur place à sa guise tous ses bateaux sur sa grille (à gauche) avec possibilité de les faire pivoter (Rotate)(r) , puis confirme le placement de ses bateaux.\n\n"
                                                      "Chaque joueur dispose de la flotte suivante: \n"
                                                      "-1 porte avion (5 cases)\n"
                                                      "-1 croiseur (4 cases, cliquer sur les 2 cases centrales)\n"
                                                      "-1 contre torpilleur (3 cases)\n"
                                                      "-1 sous-marin (3 cases)\n"
                                                      "-1 torpilleur (2 cases, pareil que les 4 cases)\n\n"
                                                      "Bien entendu, un joueur ne doit pas voir la grille de son adversaire.\n"
                                                      "Une fois tous les bateaux en jeu, la partie peut commencer.\n"
                                                      "Un à un, les joueurs se tirent dessus en cliquant sur la grille de droite.\n\n"
                                                      "Il faut confirmer le changement de joueur lorsque l'on prend son tour (Change Player).\n"
                                                      "\n\n"
                                                      "Comment gagner une partie de bataille navale\n"
                                                      "---------------------------------------\n"
                                                      "Une partie de bataille navale se termine lorsque l’un des joueurs n’a plus de navires."
                                                      "\n----------"
                                                      "\n Vous pouvez également utiliser le pavé numérique pour choisir la taille des bateaux ainsi que la touche r pour les tourner")


####                                  ####


# noinspection SpellCheckingInspection
def create_menu(menubar: tk.Menu, root: tk.Tk):
    menubar.add_command(label="Help", command=g_help)
    menubar.add_command(label="About", command=about)
    menubar.add_command(label="Play again", command=lambda: (root.destroy(), Battleship_1v1()))
    menubar.add_command(label="Game Select Menu", command=lambda: [root.destroy(), run_main.run_main()])


def over(player: int):
    messagebox.showinfo('You won!', f'Congrats Player {player+1}, you won!\n You are a master at this game! Or just lucky? Who knows?\n (You may continue playing for whatever reason you have)')
    pass


class Boat:

    def __init__(self, coordinates: list, size):
        ## Coordinates like this: [ [x, y], [x, y], [x, y] ]
        ## State like this:       [  1/0,    1/0,    1/0 ]
        self.is_alive = True
        self.coordinates = coordinates
        self.state = [1] * len(coordinates)
        self.size = str(size)

    def is_dead(self) -> bool:
        return not self.state.__contains__(1)

    def get_type(self) -> str:
        # 2 tiles boat is a Destroyer // 3 tiles boats are Submarine and Cruiser #
        # 4 tiles boat is a Battleship // 5 tiles boat is a Carrier #
        return ['Destroyer', 'Cruiser/Submarine', 'Battleship', 'Carrier'][int(self.size) - 2]

    def get_coordinates(self) -> list:
        return self.coordinates

    def set_state(self, i: int, val: int):
        self.state[i] = val


class Battleship_1v1:

    def __init__(self):
        ## Window creation
        self.root = tk.Tk()
        self.root.title("Battleship - Alpha V2.0")
        self.root.protocol("WM_DELETE_WINDOW", lambda: system.exit("User cancelation"))
        ## Add Icon
        myappid = 'mjcorp.battleship.alphav2.0'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.path = Ct.get_path()
        self.has_prev_key_release = None
        self.root.bind("<KeyPress-r>", self.on_key_press_repeat)
        self.root.bind("<KeyPress-2>", self.on_key_press_repeat)
        self.root.bind("<KeyPress-3>", self.on_key_press_repeat)
        self.root.bind("<KeyPress-4>", self.on_key_press_repeat)
        self.root.bind("<KeyPress-5>", self.on_key_press_repeat)

        ## Scale and test volume button creation
        w = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, label="Change Volume")
        w['command'] = lambda w2=w: self.change_volume(w2)
        w.set(80)
        w.grid(row=9, column=13)
        self.volume = 0.8
        test_sound = tk.Button(self.root, text='Test Volume',
                               command=lambda: self.play(self.path.joinpath('resources\\sounds\\fail\\ah.mp3')))
        test_sound.grid(row=8, column=13)

        ## Create a Menubar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        create_menu(menubar, self.root)

        ## Creation of the dictionary with all sounds
        self.sounds = {'destroy': [self.path.joinpath('resources\\sounds\\destroy\\amaterasu-sound-effect.mp3'),
                                   self.path.joinpath('resources\\sounds\\destroy\\yes-yes-yes-yes.mp3')],
                       'fail': [self.path.joinpath('resources\\sounds\\fail\\bruh-sound-effect.mp3'),
                                self.path.joinpath('resources\\sounds\\fail\\oof-sound-effect.mp3'),
                                self.path.joinpath('resources\\sounds\\fail\\plouf.mp3'),
                                self.path.joinpath('resources\\sounds\\fail\\ah.mp3'),
                                self.path.joinpath('resources\\sounds\\fail\\hotel-mario-non.mp3')],
                       'touch': [self.path.joinpath('resources\\sounds\\touch\\ha-got-emm-sound-effect.mp3'),
                                 self.path.joinpath('resources\\sounds\\touch\\sharingan-sound-effect.mp3'),
                                 self.path.joinpath('resources\\sounds\\touch\\sr-pelo-boom-sound-effect.mp3'),
                                 self.path.joinpath('resources\\sounds\\touch\\wazaaaa.mp3')]}

        ######## BUTTONS AND LABEL FOR GAME CREATION ########
        ## row and column configuration
        for i in range(0, 12):
            self.root.rowconfigure(i, minsize=50)
        for i in range(0, 27):
            self.root.columnconfigure(i, minsize=50)
        self.root.columnconfigure(14, minsize=75)

        alpha = "abcdefghijklmnopqrstuvwxyz"
        ##Boat Board--------------------------------------------------------
        ## row and column indicators
        tk.Label(self.root, bg="sandy brown", fg="white").grid(row=10, column=10, sticky='nsew')
        for row in range(0, 10):
            tk.Label(self.root, text=str(row + 1), bg="peach puff", fg="black").grid(row=row, column=10, sticky='nsew')
        for column in range(0, 10):
            tk.Label(self.root, text=alpha[column], bg="peach puff", fg="black").grid(row=10, column=column,
                                                                                      sticky='nsew')
            ## Buttons
        for column in range(0, 10):
            for row in range(0, 10):
                a = tk.Button(self.root)
                a["command"] = lambda a2=a: self.clicked(a2)
                a.grid(row=row, column=column, sticky='nsew')
        ## --------------------------------------------------------------------

        ##Attack Board--------------------------------------------------------
        self.atk_offset = 17  # offsetr for atk_board
        ## row and column indicators
        tk.Label(self.root, bg="sandy brown", fg="white").grid(row=10, column=self.atk_offset - 1, sticky='nsew')
        for row in range(0, 10):
            tk.Label(self.root, text=str(row + 1), bg="peach puff", fg="black").grid(row=row,
                                                                                     column=self.atk_offset - 1,
                                                                                     sticky='nsew')
        for column in range(self.atk_offset, self.atk_offset + 10):
            tk.Label(self.root, text=alpha[column - self.atk_offset], bg="peach puff", fg="black").grid(row=10,
                                                                                                        column=column,
                                                                                                        sticky='nsew')
            ## Buttons
        for column in range(self.atk_offset, self.atk_offset + 10):
            for row in range(0, 10):
                a = tk.Button(self.root, state=tk.DISABLED)  ##, bg="cyan"
                a["command"] = lambda a2=a: self.attack(a2)
                a.grid(row=row, column=column, sticky='nsew')
        ## --------------------------------------------------------------------

        ## Rotate boat orientation button and current orientation display
        tk.Button(self.root, bg="white", text="Rotate", command=self.rotate_boat).grid(row=1, column=13, sticky='nsew')
        self.curr_rotation = tk.Label(self.root, text='Horizontal')
        self.curr_rotation.grid(row=1, column=14, sticky='nsew')

        ## Size Buttons
        self.size_2 = tk.Button(self.root, bg="white", text="Size: 2", command=lambda: self.size(self.size_2, "2"))
        self.size_3 = tk.Button(self.root, bg="white", text="Size: 3", command=lambda: self.size(self.size_3, "3"))
        self.size_4 = tk.Button(self.root, bg="white", text="Size: 4", command=lambda: self.size(self.size_4, "4"))
        self.size_5 = tk.Button(self.root, bg="white", text="Size: 5", command=lambda: self.size(self.size_5, "5"))
        self.size_buttons = [self.size_2, self.size_3, self.size_4, self.size_5]
        for b, row in zip(self.size_buttons, range(2, 6)):
            b.grid(row=row, column=13, sticky='nsew')

        ## Change Player button
        self.change_player = tk.Button(self.root, bg="white", text="Change Player", command=self.switch_player, state=tk.DISABLED)
        self.change_player.grid(row=7, column=13, sticky='nsew')

        ## Boards creation
        self.p1_board = Ct.new_board()
        self.p1_atk_board = Ct.new_board()
        self.p2_board = Ct.new_board()
        self.p2_atk_board = Ct.new_board()

        ## Lists to be able to switch between boards according to current player
        self.boards = [self.p1_board, self.p2_board]
        self.atk_boards = [self.p1_atk_board, self.p2_atk_board]

        ## Boat lists creation
        self.p1_boats = []
        self.p2_boats = []
        self.boats = [self.p1_boats, self.p2_boats]

        ## Variables creation
        self.player = 0  ## curr_player
        self.boat = ""
        self.boat_state = "horizontal"
        self.count_3 = 0
        self.turns = 0
        self.defaultbg = self.root.cget('bg')
        self.last_clicked = None

        self.curr_player = tk.Label(self.root, font=tkinter.font.Font(size=15), text=f'Player: {self.player+1}')
        self.curr_player.grid(row=0, column=13, sticky='nsew')

        ## Creation of the dictionary with all images
        self.images_root = {'touched': get_img(self.path.joinpath('resources\\images\\Battleship\\touched.png')),
                            'missed': get_img(self.path.joinpath('resources\\images\\Battleship\\missed.png'))}
        self.images_alive_horizontal = {
            'center': get_img(self.path.joinpath('resources\\images\\Battleship\\horizontal\\alive\\center.png')),
            'first': get_img(self.path.joinpath('resources\\images\\Battleship\\horizontal\\alive\\first.png')),
            'last': get_img(self.path.joinpath('resources\\images\\Battleship\\horizontal\\alive\\last.png'))}
        self.images_alive_vertical = {
            'center': get_img(self.path.joinpath('resources\\images\\Battleship\\vertical\\alive\\center.png')),
            'first': get_img(self.path.joinpath('resources\\images\\Battleship\\vertical\\alive\\first.png')),
            'last': get_img(self.path.joinpath('resources\\images\\Battleship\\vertical\\alive\\last.png'))}
        self.images_destroyed_horizontal = {
            'center': get_img(self.path.joinpath('resources\\images\\Battleship\\horizontal\\destroyed\\center.png')),
            'first': get_img(self.path.joinpath('resources\\images\\Battleship\\horizontal\\destroyed\\first.png')),
            'last': get_img(self.path.joinpath('resources\\images\\Battleship\\horizontal\\destroyed\\last.png'))}
        self.images_destroyed_vertical = {
            'center': get_img(self.path.joinpath('resources\\images\\Battleship\\vertical\\destroyed\\center.png')),
            'first': get_img(self.path.joinpath('resources\\images\\Battleship\\vertical\\destroyed\\first.png')),
            'last': get_img(self.path.joinpath('resources\\images\\Battleship\\vertical\\destroyed\\last.png'))}
        self.images_horizontal = {'alive': self.images_alive_horizontal, 'destroyed': self.images_destroyed_horizontal}
        self.images_vertical = {'alive': self.images_alive_vertical, 'destroyed': self.images_destroyed_vertical}
        self.images_root['horizontal'] = self.images_horizontal
        self.images_root['vertical'] = self.images_vertical
        g_help()

        Ct.center(self.root)

        self.root.mainloop()

    def rotate_boat(self):
        """Changes the placement orientation for odd numbers """
        self.boat_state = "horizontal" if self.boat_state == "vertical" else "vertical"
        self.curr_rotation.config(text='Vertical') if self.curr_rotation.cget(
            'text') == 'Horizontal' else self.curr_rotation.config(text='Horizontal')

    def clicked(self, button: tk.Button):
        """ Function called when placing boats
        :param button: Button pressed
        """
        board = self.boards[self.player]
        boats = self.boats[self.player]
        if self.can_place(self.boat, button):
            if self.boat == "3":
                self.draw_boat(1, button)
                self.count_3 += 1
                if self.count_3 == 2:
                    self.size_3.config(state=tk.DISABLED)
                    self.size_3.config(state=tk.DISABLED, bg='white')
                    self.boat = ""
            elif self.boat == "5":
                self.draw_boat(3, button)
                self.size_5.config(state=tk.DISABLED)
                self.size_5.config(state=tk.DISABLED, bg='white')
                self.boat = ""
            elif self.boat == "2":
                b = button.grid_info()
                button.config(bg="orange")
                if self.last_clicked is not None:
                    b_last = self.last_clicked.grid_info()
                    if abs(b_last["row"] - b["row"]) == 0 and abs(b_last["column"] - b["column"]) == 1:
                        # HORIZONTAL
                        board[b_last["row"]][b_last['column']] = 1
                        board[b["row"]][b['column']] = 1
                        new_boat_coord = [[b_last["row"], b_last['column']], [b["row"], b['column']]]
                        new_boat_coord.sort()
                        new_boat = Boat(new_boat_coord, len(new_boat_coord))
                        boats.append(new_boat)
                        print(new_boat_coord)
                        self.draw_boat_img(new_boat)
                        self.last_clicked = None
                        self.size_2.config(state=tk.DISABLED, bg='white')
                        self.boat = ""

                    elif abs(b_last["row"] - b["row"]) == 1 and abs(b_last["column"] - b["column"]) == 0:
                        # VERTICAL
                        board[b_last["row"]][b_last['column']] = 1
                        board[b["row"]][b['column']] = 1
                        new_boat_coord = [[b_last["row"], b_last['column']], [b["row"], b['column']]]
                        new_boat_coord.sort()
                        new_boat = Boat(new_boat_coord, len(new_boat_coord))
                        boats.append(new_boat)
                        print(new_boat_coord)
                        self.draw_boat_img(new_boat)
                        self.last_clicked = None
                        self.size_2.config(state=tk.DISABLED, bg='white')
                        self.boat = ""

                    else:
                        self.last_clicked.config(bg=self.defaultbg)
                        button.config(bg=self.defaultbg)
                        self.last_clicked = None
                        return
                else:
                    self.last_clicked = button
            elif self.boat == "4":
                b = button.grid_info()
                button.config(bg="orange")
                if self.last_clicked is not None:
                    b_last = self.last_clicked.grid_info()
                    if abs(b_last["row"] - b["row"]) == 0 and abs(b_last["column"] - b["column"]) == 1:
                        # HORIZONTAL
                        if b_last['column'] == 0 or b['column'] == 0 or b_last['column'] == 9 or b['column'] == 9:
                            self.last_clicked.config(bg=self.defaultbg)
                            button.config(bg=self.defaultbg)
                            self.last_clicked = None

                        if (board[b_last["row"]][b_last['column'] + 1] == 0 and
                            board[b_last["row"]][b_last['column'] - 1] == 0) and \
                                (board[b["row"]][b['column'] - 1] == 0 and
                                 board[b["row"]][b['column'] + 1] == 0):

                            new_boat_coord = []

                            board[b_last["row"]][b_last['column'] - 1] = 1
                            board[b_last["row"]][b_last['column'] + 1] = 1
                            board[b["row"]][b['column'] - 1] = 1
                            board[b["row"]][b['column'] + 1] = 1

                            new_boat_coord.append([b_last["row"], b_last['column'] - 1])
                            new_boat_coord.append([b_last["row"], b_last['column'] + 1])
                            new_boat_coord.append([b["row"], b['column'] - 1])
                            new_boat_coord.append([b["row"], b['column'] + 1])
                            new_boat_coord.sort()

                            new_boat = Boat(new_boat_coord, len(new_boat_coord))
                            boats.append(new_boat)
                            print(new_boat_coord)
                            self.draw_boat_img(new_boat)
                            self.last_clicked = None
                            self.size_4.config(state=tk.DISABLED, bg='white')
                            self.boat = ""

                        else:
                            self.last_clicked.config(bg=self.defaultbg)
                            button.config(bg=self.defaultbg)
                            self.last_clicked = None
                            return

                    elif abs(b_last["row"] - b["row"]) == 1 and abs(b_last["column"] - b["column"]) == 0:
                        # VERTICAL
                        if b_last['row'] == 0 or b['row'] == 0 or b_last['row'] == 9 or b['row'] == 9:
                            self.last_clicked.config(bg=self.defaultbg)
                            button.config(bg=self.defaultbg)
                            self.last_clicked = None

                        elif (board[b_last["row"] + 1][b_last['column']] == 0 and
                              board[b_last["row"] - 1][b_last['column']] == 0) and \
                                (board[b["row"] - 1][b['column']] == 0 and
                                 board[b["row"] + 1][b['column']] == 0):

                            new_boat_coord = []

                            board[b_last["row"] - 1][b_last['column']] = 1
                            board[b_last["row"] + 1][b_last['column']] = 1
                            board[b["row"] - 1][b['column']] = 1
                            board[b["row"] + 1][b['column']] = 1

                            new_boat_coord.append([b_last["row"] - 1, b_last['column']])
                            new_boat_coord.append([b_last["row"] + 1, b_last['column']])
                            new_boat_coord.append([b["row"] - 1, b['column']])
                            new_boat_coord.append([b["row"] + 1, b['column']])
                            new_boat_coord.sort()

                            new_boat = Boat(new_boat_coord, len(new_boat_coord))
                            boats.append(new_boat)
                            print(new_boat_coord)
                            self.draw_boat_img(new_boat)
                            self.last_clicked = None
                            self.size_4.config(state=tk.DISABLED, bg='white')
                            self.boat = ""

                        else:
                            self.last_clicked.config(bg=self.defaultbg)
                            button.config(bg=self.defaultbg)
                            self.last_clicked = None
                            return

                    else:
                        # Not 2 adjacent squares
                        self.last_clicked.config(bg=self.defaultbg)
                        button.config(bg=self.defaultbg)
                        self.last_clicked = None
                        return
                else:
                    self.last_clicked = button
        else:
            return
        self.boards[self.player] = board
        self.boats[self.player] = boats
        if len(self.boats[self.player]) == 5:
            self.play(self.path.joinpath('resources\\sounds\\are-you-sure-about-that.mp3'))
            ans = messagebox.askquestion(title='Are you sure about that?',
                                         message="Dou you wish to keep this boat placement?")
            if ans == 'yes':
                self.change_player.config(state=tk.NORMAL, bg='green')
                if self.turns == 1:
                    for child in Ct.all_children(self.root, 'Button'):
                        c = child.grid_info()
                        if c['row'] < 10 and c['column'] < 10:
                            child["image"] = ''
                            child.config(command='')
                    for boat in self.boats[self.player]:
                        self.draw_boat_img(boat)
            else:
                self.boats[self.player].clear()
                self.remove_all_images()
                self.count_3 = 0
                self.boards[self.player] = Ct.new_board()
                for button in self.size_buttons:
                    button.config(state=tk.NORMAL)

    def can_place(self, size: str, button: tk.Button) -> bool:
        """ Checks if you can place a boat of a certain size in a certain orientation
        :param size: size of the boat
        :param button: button clicked
        :return: Boolean
        """
        board = self.boards[self.player]
        ## Pour les bateaux pairs, laisser choisir les deux carres centraux au joueur puis fill le reste TMTC pd bosse un peu
        ## ET si l'player peut pas beh tu restart donc pas besoin de bouton turn, en gros reset la rota a chaque bateau DUCON
        b = button.grid_info()
        if size == "":
            print('Please select a Boat size')
            return False
        size = int(size)
        if size == 2:
            arm = 0
        elif size == 4:
            return board[b["row"]][b["column"]] == 0
        else:
            arm = (size - 1) // 2
        if board[b["row"]][b["column"]] == 1:
            return False
        if self.boat_state == "horizontal":
            for j in range(1, arm + 1):
                try:
                    if b["column"] - j < 0 or b["column"] + j > len(board[0]):
                        return False
                    elif board[b["row"]][b["column"] - j] == 1:
                        return False
                    elif board[b["row"]][b["column"] + j] == 1:
                        return False
                except IndexError:
                    print("out of bounds")
                    return False
            return True
        else:
            for j in range(1, round(arm + 1)):
                try:
                    if b["row"] - j < 0 or b["row"] + j > len(board[0]):
                        return False
                    elif board[b["row"] - j][b["column"]] == 1:
                        return False
                    elif board[b["row"] + j][b["column"]] == 1:
                        return False
                except IndexError:
                    print("out of bounds")
                    return False
            return True

    def draw_boat(self, arm_size: int, button: tk.Button):
        """ !USE ONLY WITH ODD NUMBERS! draws the boat in the players board {mechanical, only in code, not visual}
        :param arm_size: Size of the boat -1 and divided by 2
        :param button: button clicked
        """
        board = self.boards[self.player]
        boats = self.boats[self.player]
        arm_size = 2 if arm_size == 1 else arm_size
        b = button.grid_info()
        boat_coordinates = [[b['row'], b['column']]]
        board[b["row"]][b['column']] = 1
        if self.boat_state == "horizontal":
            for child in Ct.all_children(self.root, "Button"):
                info = child.grid_info()
                for j in range(1, arm_size):
                    if info['row'] == b["row"] and info['column'] == b["column"] - j:
                        board[b["row"]][b['column'] - j] = 1
                        boat_coordinates.append([b["row"], b['column'] - j])
                    elif info['row'] == b["row"] and info['column'] == b["column"] + j:
                        board[b["row"]][b['column'] + j] = 1
                        boat_coordinates.append([b["row"], b['column'] + j])
        elif self.boat_state == "vertical":
            for child in Ct.all_children(self.root, "Button"):
                info = child.grid_info()
                for j in range(1, arm_size):
                    if info['row'] == b["row"] - j and info['column'] == b["column"]:
                        board[b["row"] - j][b['column']] = 1
                        boat_coordinates.append([b["row"] - j, b['column']])
                    elif info['row'] == b["row"] + j and info['column'] == b["column"]:
                        board[b["row"] + j][b['column']] = 1
                        boat_coordinates.append([b["row"] + j, b['column']])
        boat_coordinates.sort()
        boat_coordinates = Ct.remove_duplicates(boat_coordinates)
        new_boat = Boat(boat_coordinates, len(boat_coordinates))
        boats.append(new_boat)
        print(boat_coordinates)
        self.draw_boat_img(new_boat)
        self.boards[self.player] = board
        self.boats[self.player] = boats

    def draw_boat_img(self, boat: Boat):
        """ Draws a boat in its coordinates on the player's board {visual}
        :param boat: The boat to be drawn -> Boat class
        """
        coordinates = boat.get_coordinates()
        boat_size = len(boat.get_coordinates())
        orientation = "vertical" if coordinates[0][1] == coordinates[1][1] else 'horizontal'
        part = 0
        boat_state = boat.state
        for child in Ct.all_children(self.root, 'Button'):
            c = child.grid_info()
            if [c['row'], c['column']] == coordinates[part]:
                if part == 0:
                    if boat_state[part] == 1:
                        child.config(image=self.images_root.get(orientation).get('alive').get('first'), bg=self.defaultbg)
                    else:
                        child.config(image=self.images_root.get(orientation).get('destroyed').get('first'),
                                     bg=self.defaultbg)
                        pass  # Draw touched texture
                elif part == boat_size - 1:
                    if boat_state[part] == 1:
                        child.config(image=self.images_root.get(orientation).get('alive').get('last'), bg=self.defaultbg)
                    else:
                        child.config(image=self.images_root.get(orientation).get('destroyed').get('last'),
                                     bg=self.defaultbg)
                        pass  # Draw touched texture
                    break
                else:
                    if boat_state[part] == 1:
                        child.config(image=self.images_root.get(orientation).get('alive').get('center'), bg=self.defaultbg)
                    else:
                        child.config(image=self.images_root.get(orientation).get('destroyed').get('center'),
                                     bg=self.defaultbg)
                        pass  # Draw touched texture
                part += 1

    def draw_attacks(self):
        """Draws the attacks and attempts in the player's atk board {visual}"""
        board = self.atk_boards[self.player]
        for child in Ct.all_children(self.root, 'Button'):
            c = child.grid_info()
            if c['column'] >= self.atk_offset:
                if board[c['row']][c['column'] - self.atk_offset] == 1:
                    child.config(image=self.images_root.get('touched'))
                elif board[c['row']][c['column'] - self.atk_offset] == -1:
                    child.config(image=self.images_root.get('missed'))

    def size(self, button: tk.Button, size: str):
        """ Changes the size of the boat to be drawn and colors in green the button with the size chosen
        :param button: Button clicked
        :param size: Size to next boat
        """
        self.boat = size
        for buttons in self.size_buttons:
            buttons.config(bg='white')
        button.config(bg="green")

    def attack(self, button: tk.Button):
        """ Called when attacking in the right atk board, mechanically attacks and draws the attempt on screen.
        Detects if a boat was sunk
        :param button: Button pressed
        """
        other_player_board = self.boards[abs(self.player - 1)]
        other_player_boats = self.boats[abs(self.player - 1)]
        curr_player_atk_board = self.atk_boards[self.player]

        b = button.grid_info()
        if self.atk_boards[self.player][b['row']][b['column'] - self.atk_offset] != 0:
            return
        if other_player_board[b['row']][b['column'] - self.atk_offset] == 1:
            for boat in other_player_boats:
                coords = boat.get_coordinates()
                for xy in coords:
                    if xy == [b['row'], b['column'] - self.atk_offset]:
                        boat.set_state(coords.index(xy), 0)
                        button.config(image=self.images_root.get('touched'))
                        curr_player_atk_board[b['row']][b['column'] - self.atk_offset] = 1
                        if boat.is_dead():
                            self.play(
                                self.sounds.get('destroy')[random.randint(0, len(self.sounds.get('destroy')) - 1)])
                            tk.messagebox.showinfo(title='Nice', message=f'You sank a {boat.get_type()} boat')
                            one_alive = False
                            for checkboat in other_player_boats:
                                if not checkboat.is_dead():
                                    one_alive = True
                                    break
                            if not one_alive:
                                over(self.player)
                        else:
                            self.play(self.sounds.get('touch')[random.randint(0, len(self.sounds.get('touch')) - 1)])
        else:
            self.play(self.sounds.get('fail')[random.randint(0, len(self.sounds.get('fail')) - 1)])
            button.config(image=self.images_root.get('missed'))
            curr_player_atk_board[b['row']][b['column'] - self.atk_offset] = -1
        self.atk_boards[self.player] = curr_player_atk_board

        self.boats[abs(self.player - 1)] = other_player_boats
        self.end_turn()

    def end_turn(self):
        """ Called at every end of turn from the moment self.turns >= 2"""
        for child in Ct.all_children(self.root, 'Button'):
            c = child.grid_info()
            if c['row'] < 10 and c['column'] >= self.atk_offset:
                child.config(command='')
        self.change_player.config(state=tk.NORMAL, bg='green')

    def remove_all_images(self):
        """ Removes every image from every Button on the screen"""
        for child in Ct.all_children(self.root, 'Button'):
            child["image"] = ''

    def switch_player(self):
        """Called to switch players"""
        self.change_player.config(text="Confirm Change", command=self.confirm_change)
        self.remove_all_images()
        self.player = 1 if self.player == 0 else 0
        self.turns += 1

    def confirm_change(self):
        """Called when the other player confirms the change"""
        self.change_player.config(text="Change Player", command=self.switch_player, state=tk.DISABLED,
                                  bg=self.defaultbg)
        self.curr_player.config(text=f'Player: {self.player+1}')
        self.draw_attacks()
        for boat in self.boats[self.player]:
            self.draw_boat_img(boat)
        if self.turns >= 2:
            for child in Ct.all_children(self.root, 'Button'):
                c = child.grid_info()
                if c['row'] < 10 and c['column'] >= self.atk_offset:
                    child.config(command=lambda child2=child: self.attack(child2), state=tk.NORMAL)
        if self.turns < 2:
            self.count_3 = 0
            self.size_2.config(state=tk.NORMAL)
            self.size_3.config(state=tk.NORMAL)
            self.size_4.config(state=tk.NORMAL)
            self.size_5.config(state=tk.NORMAL)

    def change_volume(self, w):
        """ Changes the volume at which sounds are played
        :param w: slider value
        """
        self.volume = int(w) / 100

    def play(self, path: Union[str, Path]):
        """ Plays a sound
        :param path: Path to sound
        """
        pygame.init()
        pygame.mixer.music.load(path)  # Loading File Into Mixer
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()

    def on_key_press(self, event: chr):
        key_pressed = repr(event.char).replace("'", '', 2)
        if key_pressed == 'r':
            self.rotate_boat()
        elif key_pressed == '2':
            self.size(self.size_2, "2")
        elif key_pressed == '3':
            self.size(self.size_3, "3")
        elif key_pressed == '4':
            self.size(self.size_4, "4")
        elif key_pressed == '5':
            self.size(self.size_5, "5")
        print("on_key_press", repr(event.char))

    def on_key_press_repeat(self, event: chr):
        if self.has_prev_key_release:
            self.root.after_cancel(self.has_prev_key_release)
            self.has_prev_key_release = None
            print("on_key_press_repeat", repr(event.char))
        else:
            self.on_key_press(event)


if __name__ == '__main__':
    Battleship_1v1()
