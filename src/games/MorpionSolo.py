## Code Cleaned Up##

import sys as system
import tkinter.font as font
from random import Random
from tkinter import *
from tkinter import messagebox

from src.resources.utils.Constants import Constants as Ct


#####          STATIC METHODS          ####
def difficultyHelp():
    """ Used to display a difficultyHelp in a messageBox """
    messagebox.showinfo(title="Help", message="Difficulty: \n"
                                              "Noob - The CPU will place randomly \n"
                                              "Easy - The CPU will prevent you from winning \n"
                                              "Normal - The CPU will prevent you from winning and will try to")


def about():
    """ Used to display an about messageBox """
    messagebox.showinfo(title="About", message="Made by: Jari \n "
                                               "Version: Beta 2.5-SOLO")
####                                  ####


class MorpionSolo:
    def __init__(self, Ppoints=0, CPUpoints=0, ties=0, whooseTurn=1, level="Noob", previous=None):
        """ class Initialization """
        try:
            previous.destroy()   ## Destroy previous Game just to prevent overloading of memory because of callbacks
        except AttributeError:
            pass
        self.wChoose = Tk().destroy()  # Just so that PyCharms gives me a break
        self.Pcursor, self.CPUcursor = "", ""
        self.baseCursorList = ["X", "O", "><", "@", "^^", "*", "~|~", "#", "}-{", "0_0", "~", "+", "[  ]", ":-:", "UwU",
                               "|/|\\|"]
        self.cursor_window()
        self.cursorList = self.baseCursorList.copy()
        self.Ppoints, self.CPUpoints, self.ties, self.whooseTurn, self.lvl = Ppoints, CPUpoints, ties, whooseTurn, level

        self.w = Tk()
        self.w.protocol("WM_DELETE_WINDOW", lambda: system.exit("User cancelation"))
        w = 800
        h = 400
        ## get screen width and height
        ws = self.w.winfo_screenwidth()
        hs = self.w.winfo_screenheight()
        ## calculate x and y coordinates for the window to be opened at
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.w.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.w.title("Tic Tac Toe - Solo")
        self.w.config(bg="lightgray")

        self.menubar = Menu(self.w)
        self.create_menu()

        self.board = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]

        ## ROW and COLUMN configuration ##
        for i in range(0, 3):
            self.w.columnconfigure(i, minsize=100)
        for i in range(3, 6):
            self.w.columnconfigure(i, minsize=150)
        for i in range(0, 3):
            self.w.rowconfigure(i, minsize=100)
        ##################################

        customFont = font.Font(size=25)
        customLabelFont = font.Font(size=10)

        ####                LABEL CREATION               ####
        self.PcursorLabel = Label(text=f"Player Cursor:  {self.Pcursor}", font=customLabelFont)
        self.PcursorLabel.grid(row=0, column=3, sticky='nsew')

        self.CPUcursorLabel = Label(text=f"CPU Cursor:  {self.CPUcursor}", font=customLabelFont)
        self.CPUcursorLabel.grid(row=1, column=3, sticky='nsew')

        self.PpointsLabel = Label(text=f"Player Points:  {self.Ppoints}", fg="green", font=customLabelFont)
        self.PpointsLabel.grid(row=0, column=4, sticky='nsew')

        self.CPUpointsLabel = Label(text=f"CPU Points:  {self.CPUpoints}", fg="red", font=customLabelFont)
        self.CPUpointsLabel.grid(row=1, column=4, sticky='nsew')

        self.currDifficultyLabel = Label(text=f"Current Difficulty:  {self.lvl}", font=customLabelFont)
        self.currDifficultyLabel.grid(row=0, column=5, sticky='nsew')

        self.tiesLabel = Label(text=f"Number of Ties:  {self.ties}", fg="orange", font=customLabelFont)
        self.tiesLabel.grid(row=1, column=5, sticky='nsew')

        for labels in Ct.all_children(self.w, "Label"):
            labels.config(bg="lightgray")
            labels.config(bd=8, relief=RIDGE)

        ####                                            ####

        ####                BUTTONS CREATION            ####
        self.buttonList = []

        self.button1 = Button(text="", font=customFont, command=lambda: self.button(self.button1))
        self.buttonList.append(self.button1)

        self.button2 = Button(text="", font=customFont, command=lambda: self.button(self.button2))
        self.buttonList.append(self.button2)

        self.button3 = Button(text="", font=customFont, command=lambda: self.button(self.button3))
        self.buttonList.append(self.button3)

        self.button4 = Button(text="", font=customFont, command=lambda: self.button(self.button4))
        self.buttonList.append(self.button4)

        self.button5 = Button(text="", font=customFont, command=lambda: self.button(self.button5))
        self.buttonList.append(self.button5)

        self.button6 = Button(text="", font=customFont, command=lambda: self.button(self.button6))
        self.buttonList.append(self.button6)

        self.button7 = Button(text="", font=customFont, command=lambda: self.button(self.button7))
        self.buttonList.append(self.button7)

        self.button8 = Button(text="", font=customFont, command=lambda: self.button(self.button8))
        self.buttonList.append(self.button8)

        self.button9 = Button(text="", font=customFont, command=lambda: self.button(self.button9))
        self.buttonList.append(self.button9)

        i = 0
        for row in range(0, 3):
            for column in range(0, 3):
                self.buttonList[i].grid(row=row, column=column, sticky="nsew")
                self.buttonList[i].config(bd=6, relief=RAISED)
                i += 1
        ####                                            ####

        self.reset()  ## Just to make sure all buttons are equal

        if (whooseTurn % 2) == 0:
            self.CPUmove(self.lvl)

        self.w.mainloop()

    def create_menu(self):
        """ Used to create the MenuBar"""
        self.w.config(menu=self.menubar)
        diffmenu = Menu(self.menubar, tearoff=0)
        diffmenu.add_command(label="Noob", command=lambda: self.difficulty("Noob"))
        diffmenu.add_command(label="Easy", command=lambda: self.difficulty("Easy"))
        diffmenu.add_command(label="Normal", command=lambda: self.difficulty("Normal"))
        self.menubar.add_cascade(label="Difficulty", menu=diffmenu)
        self.menubar.add_command(label="Help", command=difficultyHelp)
        self.menubar.add_command(label="About", command=about)
        self.menubar.add_command(label="SwitchGamemode", command=self.switch)

    def setCursor(self, cursor):
        """ Used to choose the Player's cursor

        :param cursor: Cursor choosen, same as the button text
        """
        self.Pcursor = cursor
        self.cursorList.remove(self.Pcursor)
        self.CPUcursor = self.cursorList[Random().randint(0, len(self.cursorList) - 1)]
        self.wChoose.destroy()
        try:
            self.reset()
        except AttributeError:  # When first run
            pass

    def _paint(self):
        """ Paints all Buttons in Gray with a Blue Foreground """
        for child in Ct.all_children(self.w, "Button"):
            child.config(bg="gray", fg="blue")

    def check_win(self, who, bg="green", fg="black"):
        """ Used to check if the Player or the CPU won

        :param who: "Player" or "CPU"
        :param bg: Color to use for the background of winning cells if needed
        :param fg: Color to use for the foreground of winning cells if needed
        :return: boolean, True if 'who' won
        """
        _check = 1 if who == "Player" else -1

        top_left = True if self.board[0][0] == _check else False
        top_right = True if self.board[0][2] == _check else False
        middle = True if self.board[1][1] == _check else False
        bottom_left = True if self.board[2][0] == _check else False
        bottom_right = True if self.board[2][2] == _check else False

        if top_left and middle and bottom_right:
            self._paint()
            self.button1.config(bg=bg, fg=fg)
            self.button5.config(bg=bg, fg=fg)
            self.button9.config(bg=bg, fg=fg)
            print(f"{who} Won")
            return True
        elif top_right and middle and bottom_left:
            self._paint()
            self.button3.config(bg=bg, fg=fg)
            self.button5.config(bg=bg, fg=fg)
            self.button7.config(bg=bg, fg=fg)
            print(f"{who} Won")
            return True
        else:
            for column in range(0, 3):
                good = 0
                if (self.board[0][column]) == _check:
                    for k in range(1, 3):
                        if self.board[k][column] == _check:
                            good += 0.5
                        if good == 1:
                            o = 2
                            for child in Ct.all_children(self.w, "Button"):
                                info = child.grid_info()
                                if info['row'] == k - o and info['column'] == column:
                                    child.config(bg=bg, fg=fg)
                                    o -= 1
                                else:
                                    child.config(bg="gray", fg="blue")
                            print(f"{who} Won")
                            return True

            for row in range(0, 3):
                good = 0
                if self.board[row][0] == _check:
                    for k in range(1, 3):
                        if self.board[row][k] == _check:
                            good += 0.5
                        if good == 1:
                            o = 2
                            for child in Ct.all_children(self.w, "Button"):
                                info = child.grid_info()
                                if info['row'] == row and info['column'] == k - o:
                                    child.config(bg=bg, fg=fg)
                                    o -= 1
                                else:
                                    child.config(bg="gray", fg="blue")
                            print(f"{who} Won")
                            return True
            return False

    def board_isFull(self):
        """ Used to detect if the board is full

        :return: True if board is full
        """
        for row in range(0, 3):
            for column in range(0, 3):
                if self.board[row][column] == 0:
                    return False
        return True

    def button(self, button):
        """Used to execute mainscript, called at each button click

        :param button: Takes in parameter the button clicked
        """
        if button.cget('text') != "":
            return
        else:
            bInfo = button.grid_info()
            row = bInfo["row"]
            column = bInfo["column"]
            self.board[row][column] = 1
            button.config(text=self.Pcursor)
            if self.check_win("Player"):
                self._won("Player")
                return
            if self.board_isFull():
                self.board_full()
                return
            self.CPUmove(self.lvl)
            if self.check_win("CPU", "red", "white"):
                self._won("CPU")
                return
            if self.board_isFull():
                self.board_full()
                return

    def do_at(self, row, column):
        """ Used to place CPU's play if it is on a diagonal

        :param row: row of button
        :param column: column of button
        """
        for child in Ct.all_children(self.w, "Button"):
            info = child.grid_info()
            if info['row'] == row and info['column'] == column:
                child.config(text=self.CPUcursor)
                self.board[row][column] = -1

    def do_for_rowValue(self, row_value_target):
        """ Used to counter a player's moves

        :param row_value_target: target of the rowValue that you want to detect (addition of all values in a row or column)
        :return:
        """
        for aRow in range(0, 3):
            rowValue = 0
            for aColumn in range(0, 3):
                rowValue += self.board[aRow][aColumn]
            if rowValue == row_value_target:
                for aColumn in range(0, 3):
                    if self.board[aRow][aColumn] == 0:
                        for child in Ct.all_children(self.w, "Button"):
                            info = child.grid_info()
                            if info['row'] == aRow and info['column'] == aColumn:
                                child.config(text=self.CPUcursor)
                                self.board[aRow][aColumn] = -1
                                return False

        for aColumn in range(0, 3):
            rowValue = 0
            for aRow in range(0, 3):
                rowValue += self.board[aRow][aColumn]
            if rowValue == row_value_target:
                for aRow in range(0, 3):
                    if self.board[aRow][aColumn] == 0:
                        for child in Ct.all_children(self.w, "Button"):
                            info = child.grid_info()
                            if info['row'] == aRow and info['column'] == aColumn:
                                child.config(text=self.CPUcursor)
                                self.board[aRow][aColumn] = -1
                                return False
        return True

    def CPUmove(self, lvl="Noob"):
        """ Script of the CPUmoves

        :param lvl: Difficulty level
        """
        if lvl == "Noob":
            r = Random()
            row = r.randint(0, 2)
            column = r.randint(0, 2)
            if self.board[row][column] == 0:
                for child in Ct.all_children(self.w, "Button"):
                    info = child.grid_info()
                    if info['row'] == row and info['column'] == column:
                        child.config(text=self.CPUcursor)
                        self.board[row][column] = -1
            else:
                self.CPUmove(self.lvl)

        elif lvl == "Easy":
            r = Random()
            row = r.randint(0, 2)
            column = r.randint(0, 2)

            top_left = True if self.board[0][0] == 1 else False
            top_right = True if self.board[0][2] == 1 else False
            middle = True if self.board[1][1] == 1 else False
            bottom_left = True if self.board[2][0] == 1 else False
            bottom_right = True if self.board[2][2] == 1 else False

            top_leftSelf = True if self.board[0][0] == -1 else False
            top_rightSelf = True if self.board[0][2] == -1 else False
            middleSelf = True if self.board[1][1] == -1 else False
            bottom_leftSelf = True if self.board[2][0] == -1 else False
            bottom_rightSelf = True if self.board[2][2] == -1 else False

            if top_left and middle and not bottom_rightSelf:
                self.do_at(2, 2)
            elif top_right and middle and not bottom_leftSelf:
                self.do_at(2, 0)
            elif middle and bottom_left and not top_rightSelf:
                self.do_at(0, 2)
            elif middle and bottom_right and not top_leftSelf:
                self.do_at(0, 0)
            elif top_right and bottom_left and not middleSelf:
                self.do_at(1, 1)
            elif top_left and bottom_right and not middleSelf:
                self.do_at(1, 1)
            else:
                for aRow in range(0, 3):
                    rowValue = 0
                    for aColumn in range(0, 3):
                        rowValue += self.board[aRow][aColumn]
                    if rowValue == 2:
                        for aColumn in range(0, 3):
                            if self.board[aRow][aColumn] == 0:
                                for child in Ct.all_children(self.w, "Button"):
                                    info = child.grid_info()
                                    if info['row'] == aRow and info['column'] == aColumn:
                                        child.config(text=self.CPUcursor)
                                        self.board[aRow][aColumn] = -1
                                        return

                for aColumn in range(0, 3):
                    rowValue = 0
                    for aRow in range(0, 3):
                        rowValue += self.board[aRow][aColumn]
                    if rowValue == 2:
                        for aRow in range(0, 3):
                            if self.board[aRow][aColumn] == 0:
                                for child in Ct.all_children(self.w, "Button"):
                                    info = child.grid_info()
                                    if info['row'] == aRow and info['column'] == aColumn:
                                        child.config(text=self.CPUcursor)
                                        self.board[aRow][aColumn] = -1
                                        return

                if self.board[row][column] == 0:
                    for child in Ct.all_children(self.w, "Button"):
                        info = child.grid_info()
                        if info['row'] == row and info['column'] == column:
                            child.config(text=self.CPUcursor)
                            self.board[row][column] = -1
                else:
                    self.CPUmove(self.lvl)

        elif lvl == "Normal":
            r = Random()
            row = r.randint(0, 2)
            column = r.randint(0, 2)

            top_left = True if self.board[0][0] == -1 else False
            top_right = True if self.board[0][2] == -1 else False
            middle = True if self.board[1][1] == -1 else False
            bottom_left = True if self.board[2][0] == -1 else False
            bottom_right = True if self.board[2][2] == -1 else False

            top_leftSelf = True if self.board[0][0] == 1 else False
            top_rightSelf = True if self.board[0][2] == 1 else False
            middleSelf = True if self.board[1][1] == 1 else False
            bottom_leftSelf = True if self.board[2][0] == 1 else False
            bottom_rightSelf = True if self.board[2][2] == 1 else False

            if top_left and middle and not bottom_rightSelf:
                self.do_at(2, 2)
            elif top_right and middle and not bottom_leftSelf:
                self.do_at(2, 0)
            elif middle and bottom_left and not top_rightSelf:
                self.do_at(0, 2)
            elif middle and bottom_right and not top_leftSelf:
                self.do_at(0, 0)
            elif top_right and bottom_left and not middleSelf:
                self.do_at(1, 1)
            elif top_left and bottom_right and not middleSelf:
                self.do_at(1, 1)
            if not self.do_for_rowValue(-2):
                return

            top_left = True if self.board[0][0] == 1 else False
            top_right = True if self.board[0][2] == 1 else False
            middle = True if self.board[1][1] == 1 else False
            bottom_left = True if self.board[2][0] == 1 else False
            bottom_right = True if self.board[2][2] == 1 else False

            top_leftSelf = True if self.board[0][0] == -1 else False
            top_rightSelf = True if self.board[0][2] == -1 else False
            middleSelf = True if self.board[1][1] == -1 else False
            bottom_leftSelf = True if self.board[2][0] == -1 else False
            bottom_rightSelf = True if self.board[2][2] == -1 else False

            if top_left and middle and not bottom_rightSelf:
                self.do_at(2, 2)
            elif top_right and middle and not bottom_leftSelf:
                self.do_at(2, 0)
            elif middle and bottom_left and not top_rightSelf:
                self.do_at(0, 2)
            elif middle and bottom_right and not top_leftSelf:
                self.do_at(0, 0)
            elif top_right and bottom_left and not middleSelf:
                self.do_at(1, 1)
            elif top_left and bottom_right and not middleSelf:
                self.do_at(1, 1)
            else:
                if not self.do_for_rowValue(2):
                    return

                if self.board[row][column] == 0:
                    for child in Ct.all_children(self.w, "Button"):
                        info = child.grid_info()
                        if info['row'] == row and info['column'] == column:
                            child.config(text=self.CPUcursor)
                            self.board[row][column] = -1
                else:
                    self.CPUmove(self.lvl)

    def reset(self):
        """ Used to reset the Board and update display """
        self.board = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]
        for button in self.buttonList:
            button.config(text="", bg="SystemButtonFace", fg="black")
        self.PpointsLabel.config(text=f"Player Points:  {self.Ppoints}")
        self.CPUpointsLabel.config(text=f"CPU Points:  {self.CPUpoints}")
        self.PcursorLabel.config(text=f"Player Cursor:  {self.Pcursor}")
        self.CPUcursorLabel.config(text=f"CPU Cursor:  {self.CPUcursor}")
        self.currDifficultyLabel.config(text=f"Current Difficulty:  {self.lvl}")
        self.tiesLabel.config(text=f"Number of Ties:  {self.ties}")

    def change_cursor(self):
        """ MessageBox to change cursor """
        msgBox = messagebox.askquestion(title="System.out", message="Change Cursor?")
        if msgBox == "yes":
            MorpionSolo(self.Ppoints, self.CPUpoints, self.ties, self.whooseTurn, self.lvl, self.w)

    def cursor_window(self):
        """ CursorChanging window """
        self.wChoose = Tk()
        self.wChoose.protocol("WM_DELETE_WINDOW", lambda: system.exit("User cancelation"))
        self.wChoose.title("Choisissez un curseur: ")
        self.wChoose.config(bg="lightgray")
        customFont = font.Font(size=20)
        ## get screen width and height
        ws = self.wChoose.winfo_screenwidth()
        hs = self.wChoose.winfo_screenheight()
        ## calculate x and y coordinates for the window to be opened at
        x = (ws / 2) - (500 / 2)
        y = (hs / 2) - (100 / 2)
        self.wChoose.geometry('%dx%d+%d+%d' % (510, 125, x, y))
        self.cursorList = self.baseCursorList
        rowMax = 9
        for e in self.cursorList:
            Button(self.wChoose, text=e, font=customFont, command=lambda el=e: self.setCursor(el)) \
                 .grid(row=self.cursorList.index(e) // rowMax, column=self.cursorList.index(e) % rowMax, sticky="nsew")
        self.wChoose.mainloop()

    def difficulty(self, lvl):
        """ Command to change difficulty """
        self.lvl = lvl
        self.currDifficultyLabel.config(text=f"Current Difficulty:  {self.lvl}")

    def switch(self):
        """ Switches to 2 Players mode """
        self.w.destroy()
        from src.games.MorpionMulti import MorpionMulti
        MorpionMulti()

    def _won(self, winner):
        """ Executed when someone won, takes in parameter who won

        :param winner: "Player" or "CPU"
        """
        _text = "You won!" if winner == "Player" else "CPU won!"
        msgBox = messagebox.askquestion(title=_text, message="Play again?")
        if msgBox == "yes":
            self.Ppoints += 1 if winner == "Player" else 0
            self.CPUpoints += 1 if winner == "CPU" else 0
            self.whooseTurn += 1
            self.change_cursor()
            self.reset()
            if (self.whooseTurn % 2) == 0:
                self.CPUmove(self.lvl)
        else:
            self.w.destroy()
            system.exit("User Cancelation")

    def board_full(self):
        """ Executed when the board is full """
        msgBox = messagebox.askquestion(title="Board is full!", message="Play again?")
        if msgBox == "yes":
            self.ties += 1
            self.change_cursor()
            self.reset()
            if (self.whooseTurn % 2) == 0:
                self.CPUmove(self.lvl)
        else:
            self.w.destroy()
            system.exit("User Cancelation")
