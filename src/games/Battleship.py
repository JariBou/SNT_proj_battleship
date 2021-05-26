import ctypes
import random
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import pygame as pygame
import sys as system

from src import run_main
from src.resources.utils.Constants import Constants as Ct


## TODO: code cleanup
## TODO: add touched boats texture
## TODO: add key listeners for keybindings to rotate and select ship size


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
    messagebox.showinfo(title="About", message="Made by: LeTiramissu & Jari\n "
                                               "Version: Alpha V1.3")


def g_help():
    """Used to display help_rules about the game"""
    messagebox.showinfo(title="Help & Rules", message="Commencer une partie de bataille navale \n"
                                                      "---------------------------------------\n"
                                                      "Au début du jeu, chaque joueur place à sa guise tous ses bateaux sur sa grille (à gauche) avec possibilité de les faire pivoter (Rotate) , puis confirme le placement de ses bateaux.\n\n"
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
                                                      "Une partie de bataille navale se termine lorsque l’un des joueurs n’a plus de navires.")


####                                  ####


# noinspection SpellCheckingInspection
class Battleship_1v1:

    def __init__(self):
        ## Window creation
        self.root = tk.Tk()
        self.root.title("Battleship - Alpha V1.3")
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
        self.path = Ct.get_path()
        self.root.iconbitmap(self.path.joinpath('resources\\images\\Battleship\\Battleship_taskbar.ico'))

        self.has_prev_key_release = None
        self.root.bind("<KeyRelease-r>", self.on_key_release_repeat)
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
        test_sound.grid(row=10, column=13)

        ## Create a Menubar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        self.create_menu(menubar)

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
        for i in range(0, 30):
            self.root.rowconfigure(i, minsize=50)
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
        self.rotate = tk.Button(self.root, bg="white", text="Rotate", command=self.rotate_boat)
        self.rotate.grid(row=0, column=13, sticky='nsew')
        self.curr_rotation = tk.Label(self.root, text='Horizontal')
        self.curr_rotation.grid(row=0, column=14, sticky='nsew')

        ## Size Buttons
        self.size_2 = tk.Button(self.root, bg="white", text="Size: 2", command=lambda: self.size(self.size_2, "2"))
        self.size_2.grid(row=1, column=13, sticky='nsew')
        self.size_3 = tk.Button(self.root, bg="white", text="Size: 3", command=lambda: self.size(self.size_3, "3"))
        self.size_3.grid(row=2, column=13, sticky='nsew')
        self.size_4 = tk.Button(self.root, bg="white", text="Size: 4", command=lambda: self.size(self.size_4, "4"))
        self.size_4.grid(row=3, column=13, sticky='nsew')
        self.size_5 = tk.Button(self.root, bg="white", text="Size: 5", command=lambda: self.size(self.size_5, "5"))
        self.size_5.grid(row=4, column=13, sticky='nsew')
        self.size_buttons = [self.size_2, self.size_3, self.size_4, self.size_5]

        ## Helper Buttons   {TO BE REMOVED}
        self.console_out = tk.Button(self.root, bg="white", text="print_board", command=self.print_console)
        self.console_out.grid(row=6, column=13, sticky='nsew')
        self.boat_list = tk.Button(self.root, bg="white", text="boat_interactions", command=self.boat_interactions)
        self.boat_list.grid(row=7, column=13, sticky='nsew')

        ## Change Player button
        self.change_player = tk.Button(self.root, bg="white", text="Change Player", command=self.switch_player)
        self.change_player.grid(row=8, column=13, sticky='nsew')
        self.change_player.config(state=tk.DISABLED)

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

        ## Creation of the dictionary with all images
        self.images_root = {'touched': get_img(self.path.joinpath('resources\\images\\Battleship\\touched.png')),
                            'missed': get_img(self.path.joinpath('resources\\images\\Battleship\\missed.png'))}
        self.images_horizontal = {
            'center': get_img(self.path.joinpath('resources\\images\\Battleship\\horizontal\\center.png')),
            'first': get_img(self.path.joinpath('resources\\images\\Battleship\\horizontal\\first.png')),
            'last': get_img(self.path.joinpath('resources\\images\\Battleship\\horizontal\\last.png'))}
        self.images_vertical = {
            'center': get_img(self.path.joinpath('resources\\images\\Battleship\\vertical\\center.png')),
            'first': get_img(self.path.joinpath('resources\\images\\Battleship\\vertical\\first.png')),
            'last': get_img(self.path.joinpath('resources\\images\\Battleship\\vertical\\last.png'))}
        self.images_root['horizontal'] = self.images_horizontal
        self.images_root['vertical'] = self.images_vertical

        self.root.mainloop()

    def rotate_boat(self):
        """Changes the placement orientation for odd numbers """
        self.boat_state = "horizontal" if self.boat_state == "vertical" else "vertical"
        self.curr_rotation.config(text='Vertical') if self.curr_rotation.cget(
            'text') == 'Horizontal' else self.curr_rotation.config(text='Horizontal')

    def clicked(self, button):
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
                        return

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
                        return

                    else:
                        self.last_clicked.config(bg=self.defaultbg)
                        button.config(bg=self.defaultbg)
                        self.last_clicked = None
                        return
                self.last_clicked = button if self.last_clicked is None else self.last_clicked

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
                            return

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

                            return
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
                            return

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
                            return

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

                self.last_clicked = button if self.last_clicked is None else self.last_clicked

        else:
            print("Nope")
        self.boards[self.player] = board
        self.boats[self.player] = boats
        if len(self.boats[self.player]) == 5:
            print("Suka")
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
                self.size_2.config(state=tk.NORMAL)
                self.size_3.config(state=tk.NORMAL)
                self.size_4.config(state=tk.NORMAL)
                self.size_5.config(state=tk.NORMAL)

    def can_place(self, size, button) -> bool:
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
            return True
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

    def draw_boat(self, arm_size, button):
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

    def draw_boat_img(self, boat):
        """ Draws a boat in its coodinates on the player's board {visual}
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
                        child.config(image=self.images_root.get(orientation).get('first'), bg=self.defaultbg)
                    else:
                        pass  # Draw touched texture
                elif part == boat_size - 1:
                    if boat_state[part] == 1:
                        child.config(image=self.images_root.get(orientation).get('last'), bg=self.defaultbg)
                    else:
                        # child.config(image=self.images_touched_root.get(orientation).get('last'), bg=self.defaultbg)
                        pass  # Draw touched texture
                    break
                else:
                    if boat_state[part] == 1:
                        child.config(image=self.images_root.get(orientation).get('center'), bg=self.defaultbg)
                    else:
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

    def size(self, button, size):
        """ Changes the size of the boat to be drawn and colors in green the button with the size chosen
        :param button: Button clicked
        :param size: Size to next boat
        """
        self.boat = size
        for buttons in self.size_buttons:
            buttons.config(bg='white')
        button.config(bg="green")

    def print_console(self):
        """Prints the current player's Board in the console"""
        for k in self.boards[self.player]:
            print(str(k))

    def boat_interactions(self):
        """Prints the current player's Boat coordinates and state of each coordinate in the console"""
        for boat in self.boats[self.player]:
            print(boat.get_coordinates())
            print(boat.state)

    def attack(self, button):
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
        boats = self.boats[self.player]
        for boat in boats:
            if boat.is_dead():
                boats.remove(boat)
        self.boats[self.player] = boats
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

    def play(self, path):
        """ Plays a sound
        :param path: Path to sound
        """
        pygame.init()
        pygame.mixer.music.load(path)  # Loading File Into Mixer
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()

    def on_key_release(self, event):
        self.has_prev_key_release = None
        print("on_key_release", repr(event.char))

    def on_key_press(self, event):
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

    def on_key_release_repeat(self, event):
        self.has_prev_key_release = self.root.after_idle(self.on_key_release, event)
        print("on_key_release_repeat", repr(event.char))

    def on_key_press_repeat(self, event):
        if self.has_prev_key_release:
            self.root.after_cancel(self.has_prev_key_release)
            self.has_prev_key_release = None
            print("on_key_press_repeat", repr(event.char))
        else:
            self.on_key_press(event)

    def create_menu(self, menubar):
        colorsettings = tk.Menu(menubar, tearoff=0)
        colorsettings.add_command(label="White (default)", command=lambda: Ct.set_color(self.root, 'white', 'Label'))
        colorsettings.add_command(label="Light grey", command=lambda: Ct.set_color(self.root, 'lightgrey', 'Label'))
        colorsettings.add_command(label="Grey", command=lambda: Ct.set_color(self.root, 'grey', 'Label'))
        colorsettings.add_command(label="Light blue", command=lambda: Ct.set_color(self.root, 'lightblue', 'Label'))
        menubar.add_cascade(label="Color settings", menu=colorsettings)
        menubar.add_command(label="Help", command=g_help)
        menubar.add_command(label="About", command=about)
        menubar.add_command(label="Game Select Menu", command=lambda: [self.root.destroy(), run_main.run_main()])


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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Battleship_1v1()

# See PyCharm help_rules at https://www.jetbrains.com/help/pycharm/
