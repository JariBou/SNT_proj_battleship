## Code Cleaned Up ##
import ctypes
import sys as system
import tkinter.font as font
from tkinter import *
from tkinter import messagebox

from src import run_main
from src.resources.utils.Constants import Constants as Ct


#####          STATIC METHODS          ####
def turnHelp():
    """ Used to display a HelpMessageBox """
    messagebox.showinfo(title="Help", message="A different player starts at \n"
                                              "every new turn")


def about():
    """ Used to display an about messageBox """
    messagebox.showinfo(title="About", message="Made by: Jari \n "
                                               "Version: Beta 2.3-2P")
####                                  ####


class MorpionMulti:
    def __init__(self, P1points=0, P2points=0, ties=0, pTurn=0, playerPlay="P1", previous=None):
        """ class Initialization """
        try:
            previous.destroy()
        except AttributeError:
            pass
        self.wChoose = Tk().destroy()  # Just so that PyCharms gives me a break
        self.baseCursorList = ["X", "O", "><", "@", "^^", "*", "~|~", "#", "}-{", "0_0", "~", "+", "[  ]", ":-:", "UwU",
                               "|/|\\|"]
        self.cursorList = self.baseCursorList
        self.Pcursor, self.Pcursor2 = "", ""
        self.cursor_window()
        self.P1points, self.P2points, self.ties, self.pTurn, self.playerPlay = P1points, P2points, ties, pTurn, playerPlay

        self.whooseTurn = 1
        self.path = Ct.get_path()

        self.playerPlay = "P1"

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
        self.w.title("Tic Tac Toe - 2 Players")
        self.menubar = Menu(self.w)
        self.w.config(menu=self.menubar, bg="lightgray")
        self.menubar.add_command(label="Help", command=turnHelp)
        self.menubar.add_command(label="About", command=about)
        self.menubar.add_command(label="SwitchGamemode", command=self.switch)
        self.menubar.add_command(label="Game Select Menu", command=lambda: [self.w.destroy(), run_main.run_main()])

        myappid = 'mjcorp.tictactoe.alphav2.5S'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.w.iconbitmap(self.path.joinpath('resources\\images\\TicTacToe\\icon.ico'))

        self.has_prev_key_release = None
        self.w.bind("<KeyPress-1>", self.on_key_press_repeat)
        self.w.bind("<KeyPress-2>", self.on_key_press_repeat)
        self.w.bind("<KeyPress-3>", self.on_key_press_repeat)
        self.w.bind("<KeyPress-4>", self.on_key_press_repeat)
        self.w.bind("<KeyPress-5>", self.on_key_press_repeat)
        self.w.bind("<KeyPress-6>", self.on_key_press_repeat)
        self.w.bind("<KeyPress-7>", self.on_key_press_repeat)
        self.w.bind("<KeyPress-8>", self.on_key_press_repeat)
        self.w.bind("<KeyPress-9>", self.on_key_press_repeat)

        self.board = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]

        for i in range(0, 3):
            self.w.columnconfigure(i, minsize=100)
        for i in range(3, 6):
            self.w.columnconfigure(i, minsize=150)
        for i in range(0, 3):
            self.w.rowconfigure(i, minsize=100)

        customFont = font.Font(size=25)
        customLabelFont = font.Font(size=10)

        self.PcursorLabel = Label(text=f"Player 1 Cursor:  {self.Pcursor}", fg="green", font=customLabelFont)
        self.PcursorLabel.grid(row=0, column=3, sticky='nsew')

        self.CPUcursorLabel = Label(text=f"Player 2 Cursor:  {self.P2points}", fg="red", font=customLabelFont)
        self.CPUcursorLabel.grid(row=1, column=3, sticky='nsew')

        self.PpointsLabel = Label(text=f"Player 1 Points:  {self.P1points}", fg="green", font=customLabelFont)
        self.PpointsLabel.grid(row=0, column=4, sticky='nsew')

        self.CPUpointsLabel = Label(text=f"Player 2 Points:  {self.P2points}", fg="red", font=customLabelFont)
        self.CPUpointsLabel.grid(row=1, column=4, sticky='nsew')

        self.currPlayerLabel = Label(text=f"Current Player:  ", font=customLabelFont)
        self.currPlayerLabel.grid(row=0, column=5, sticky='nsew')

        self.tiesLabel = Label(text=f"Number of Ties:  {self.ties}", fg="orange", font=customLabelFont)
        self.tiesLabel.grid(row=1, column=5, sticky='nsew')

        if self.pTurn % 2 == 0:
            self.currPlayerLabel.config(text="Current Player:  Player 1")
        else:
            self.currPlayerLabel.config(text="Current Player:  Player 2")

        for labels in Ct.all_children(self.w, "Label"):
            labels.config(bg="lightgray")
            labels.config(bd=8, relief=RIDGE)

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

        self.reset()

        self.w.mainloop()

    def setCursor(self, cursor):
        """ Used to choose the Player's cursor, switches automatically to P1 or P2

        :param cursor: Cursor choosen, same as the button text
        """
        if self.Pcursor == "":
            self.Pcursor = cursor
            self.cursorList.remove(self.Pcursor)
            self.wChoose.destroy()
            self.cursor_window()
        else:
            if cursor != self.Pcursor:
                self.Pcursor2 = cursor
                self.cursorList.remove(self.Pcursor2)
                self.wChoose.destroy()
                try:
                    self.reset()
                except AttributeError:
                    pass

    def _paint(self):
        """ Paints all Buttons in Gray with a Blue Foreground """
        for child in Ct.all_children(self.w, "Button"):
            if str(child.winfo_class()) == "Button":
                child.config(bg="gray", fg="blue")

    def check_win(self, who, bg="green", fg="black"):
        """ Used to check if the Player 1 or the Player 2 won

        :param who: "Player 1" or "Player 2"
        :param bg: Color to use for the background of winning cells if needed
        :param fg: Color to use for the foreground of winning cells if needed
        :return: boolean, True if 'who' won
        """
        _check = 1 if who == "Player 1" else -1

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
                                elif str(child.winfo_class()) == "Button":
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
                                elif str(child.winfo_class()) == "Button":
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
        """Used to execute mainscript, called at each button click, automatically switches between players

        :param button: Takes in parameter the button clicked
        """
        if button.cget('text') != "":
            return
        else:
            if (self.pTurn % 2) == 0:
                # Player 1
                self.pTurn += 1
                bInfo = button.grid_info()
                row = bInfo["row"]
                column = bInfo["column"]
                self.board[row][column] = 1
                button.config(text=self.Pcursor)
                if self.check_win("Player 1"):
                    self._won("Player 1")
                    return
                if self.board_isFull():
                    self.board_full()
                    return
                pass
            else:
                # Player 2
                self.pTurn += 1
                bInfo = button.grid_info()
                row = bInfo["row"]
                column = bInfo["column"]
                self.board[row][column] = -1
                button.config(text=self.Pcursor2)
                if self.check_win("Player 2", "red", "white"):
                    self._won("Player 2")
                    return
                if self.board_isFull():
                    self.board_full()
                    return
            if self.pTurn % 2 == 0:
                self.currPlayerLabel.config(text="Current Player:  Player 1")
            else:
                self.currPlayerLabel.config(text="Current Player:  Player 2")

    def reset(self):
        """ Used to reset the Board and update display """
        self.board = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]
        for button in self.buttonList:
            button.config(text="", bg="SystemButtonFace", fg="black")
        self.PpointsLabel.config(text=f"Player 1 Points:  {self.P1points}")
        self.CPUpointsLabel.config(text=f"Player 2 Points:  {self.P2points}")
        self.PcursorLabel.config(text=f"Player 1 Cursor:  {self.Pcursor}")
        self.CPUcursorLabel.config(text=f"Player 2 Cursor:  {self.Pcursor2}")
        self.tiesLabel.config(text=f"Number of Ties:  {self.ties}")
        if self.pTurn % 2 == 0:
            self.currPlayerLabel.config(text="Current Player:  Player 1")
        else:
            self.currPlayerLabel.config(text="Current Player:  Player 2")

    def change_cursor(self):
        """ MessageBox to change cursor """
        msgBox = messagebox.askquestion(title="System.out", message="Change Cursor?")
        if msgBox == "yes":
            MorpionMulti(self.P1points, self.P2points, self.ties, self.pTurn, self.playerPlay, self.w)

    def cursor_window(self):
        """ CursorChanging window """
        if self.Pcursor == "":
            self.cursorList = self.baseCursorList
        self.wChoose = Tk()
        self.wChoose.protocol("WM_DELETE_WINDOW", lambda: system.exit("User cancelation"))
        self.wChoose.config(bg="lightgray")
        self.wChoose.iconbitmap(Ct.get_path().joinpath('resources\\images\\TicTacToe\\icon.ico'))
        ## get screen width and height
        ws = self.wChoose.winfo_screenwidth()
        hs = self.wChoose.winfo_screenheight()
        ## calculate x and y coordinates for the window to be opened at
        x = (ws / 2) - (500 / 2)
        y = (hs / 2) - (100 / 2)
        self.wChoose.geometry('%dx%d+%d+%d' % (510, 125, x, y))
        nb = "1" if self.Pcursor == "" else "2"
        self.wChoose.title(f"Choose a cursor Player {nb}: ")
        customFont = font.Font(size=20)
        rowMax = 9
        for e in self.cursorList:
            Button(self.wChoose, text=e, font=customFont, command=lambda el=e: self.setCursor(el)) \
                .grid(row=self.cursorList.index(e) // rowMax, column=self.cursorList.index(e) % rowMax, sticky="nsew")
        self.wChoose.mainloop()

    def switch(self):
        """ Switches to SOLO mode (Player vs CPU) """
        self.w.destroy()
        from src.games.TicTacToe.MorpionSolo import MorpionSolo
        MorpionSolo()

    def _won(self, winner):
        """ Executed when someone won, takes in parameter who won

        :param winner: "Player 1" or "Player 2"
        """
        _text = "Player 1 won!" if winner == "Player 1" else "Player 2 won!"
        msgBox = messagebox.askquestion(title=_text, message="Play again?")
        if msgBox == "yes":
            self.P1points += 1 if winner == "Player 1" else 0
            self.P2points += 1 if winner == "Player 2" else 0
            if self.playerPlay == "P1":
                self.playerPlay = "P2"
                self.pTurn = 1
            else:
                self.playerPlay = "P1"
                self.pTurn = 0
            self.change_cursor()
            self.reset()
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
        else:
            self.w.destroy()
            system.exit("User Cancelation")

    def on_key_press(self, event):
        key_pressed = repr(event.char).replace("'", '', 2)
        if key_pressed == '7':
            self.button(self.button1)
        elif key_pressed == '8':
            self.button(self.button2)
        elif key_pressed == '9':
            self.button(self.button3)
        elif key_pressed == '4':
            self.button(self.button4)
        elif key_pressed == '5':
            self.button(self.button5)
        elif key_pressed == '6':
            self.button(self.button6)
        elif key_pressed == '1':
            self.button(self.button7)
        elif key_pressed == '2':
            self.button(self.button8)
        elif key_pressed == '3':
            self.button(self.button9)

    def on_key_press_repeat(self, event):
        if self.has_prev_key_release:
            self.w.after_cancel(self.has_prev_key_release)
            self.has_prev_key_release = None
            print("on_key_press_repeat", repr(event.char))
        else:
            self.on_key_press(event)
