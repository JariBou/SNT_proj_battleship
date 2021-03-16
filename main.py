import tkinter as tk


def all_children(wid, child_type):
    """ Used to return a list of all the elements on a parent

    :param child_type: Type of the child to return, 'all' returns all types
    :param wid: Window to be executed on
    :return: List of elements on wid
    """
    _list = wid.winfo_children()
    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())
    return _list if child_type == "all" else [child for child in _list if str(child.winfo_class()) == child_type]


class Battleship_1v1:

    def __init__(self):
        self.root = tk.Tk("mainFrame - ALPHA - ")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.width, self.height = screen_width/1.25, screen_height/1.25
        ## calculate x and y coordinates for the window to be opened at
        x = (screen_width / 2) - (self.width / 2)
        y = (screen_height / 2) - (self.height / 2)
        self.root.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))
        self.root.title(f"mainFrame - ALPHA - width: {round(self.width)}, height: {round(self.height)} "
                        f"- pos: ({round(x)},{round(y)})")

        for i in range(0, 15):
            self.root.rowconfigure(i, minsize=50)
            self.root.columnconfigure(i, minsize=50)

        alpha = "abcdefghijklmnopqrstuvwxyz"
        for row in range(0, 10):
            tk.Label(self.root, text=str(row)).grid(row=row, column=10)
        for column in range(0, 10):
            tk.Label(self.root, text=alpha[column]).grid(row=10, column=column)

        for column in range(0, 10):
            for row in range(0, 10):
                a = tk.Button(self.root)
                a["command"] = lambda a=a: self.clicked(a)
                a.grid(row=row, column=column, sticky='nsew')

        self.rotate = tk.Button(self.root, text="Rotate", command=self.rotate)
        self.rotate.grid(row=0, column=13)

        self.p1_board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]

        self.p2_board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]

        self.boat = "5"
        self.boat_state = "horizontal"

        self.root.mainloop()

    def rotate(self):
        self.boat_state = "horizontal" if self.boat_state == "vertical" else "vertical"

    def clicked(self, button):
        b = button.grid_info()
        if self.can_place(self.boat, button):
            if self.boat == "3":
                button.config(bg="black")
                self.p1_board[b["row"]][b['column']] = 1
                if self.boat_state == "horizontal":
                    for child in all_children(self.root, "Button"):
                        info = child.grid_info()
                        if info['row'] == b["row"] and info['column'] == b["column"] - 1:
                            child.config(bg="black")
                            self.p1_board[b["row"]][b['column'] - 1] = 1
                        if info['row'] == b["row"] and info['column'] == b["column"] + 1:
                            child.config(bg="black")
                            self.p1_board[b["row"]][b['column'] + 1] = 1
                            break
                elif self.boat_state == "vertical":
                    for child in all_children(self.root, "Button"):
                        info = child.grid_info()
                        if info['row'] == b["row"] - 1 and info['column'] == b["column"]:
                            child.config(bg="black")
                            self.p1_board[b["row"] - 1][b['column']] = 1
                        if info['row'] == b["row"] + 1 and info['column'] == b["column"]:
                            child.config(bg="black")
                            self.p1_board[b["row"] + 1][b['column']] = 1
                            break
        else:
            print("Nope")

    def can_place(self, size, button):
        ## Pour les bateaux pairs, laisser choisir les deux carres centraux au joueur puis fill le reste TMTC pd bosse un peu
        ## ET si l'player peut pas beh tu restart donc pas besoin de bouton turn, en gros reset la rota a chaque bateau DUCON
        b = button.grid_info()
        size = int(size)
        arm = (size - 1) // 2 if size % 2 == 1 else size // 2
        if self.p1_board[b["row"]][b["column"]] == 1:
            return False
        if self.boat_state == "horizontal":
            for j in range(1, arm+1):
                try:
                    if b["column"] - j < 0 or b["column"] + j > len(self.p1_board[0]):
                        return False
                    elif self.p1_board[b["row"]][b["column"] - j] == 1:
                        return False
                    elif self.p1_board[b["row"]][b["column"] + j] == 1:
                        return False
                except IndexError:
                    print("out of bounds")
                    return False
            return True
        else:
            for j in range(1, round(arm+1)):
                try:
                    if b["row"] - j < 0 or b["row"] + j > len(self.p1_board[0]):
                        return False
                    elif self.p1_board[b["row"] - j][b["column"]] == 1:
                        return False
                    elif self.p1_board[b["row"] + j][b["column"]] == 1:
                        return False
                except IndexError:
                    print("out of bounds")
                    return False
            return True
        pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Battleship_1v1()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
