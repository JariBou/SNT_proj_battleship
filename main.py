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


def remove_duplicates(List):
    """ Removes dupes from lista given List
    :param List: List to remove dupes from
    :return: Initial list without the duplicates
    """
    already_appeared = []
    value = []
    for e in List:
        if e not in already_appeared:
            already_appeared.append(e)
            value.append(e)
    return value



class Battleship_1v1:

    def __init__(self):
        self.root = tk.Tk("mainFrame - ALPHA - ")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.width, self.height = screen_width / 1.25, screen_height / 1.25
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
        tk.Label(self.root, bg="black", fg="white").grid(row=10, column=10, sticky='nsew')
        for row in range(0, 10):
            tk.Label(self.root, text=str(row), bg="blue", fg="white").grid(row=row, column=10, sticky='nsew')
        for column in range(0, 10):
            tk.Label(self.root, text=alpha[column], bg="blue", fg="white").grid(row=10, column=column, sticky='nsew')

        for column in range(0, 10):
            for row in range(0, 10):
                a = tk.Button(self.root)
                a["command"] = lambda a=a: self.clicked(a)
                a.grid(row=row, column=column, sticky='nsew')

        self.rotate = tk.Button(self.root, bg="white", text="Rotate", command=self.rotate)
        self.rotate.grid(row=0, column=13, sticky='nsew')
        self.curr_rotation = tk.Label(self.root, text='Horizontal')
        self.curr_rotation.grid(row=0, column=14, sticky='nsew')

        self.size_2 = tk.Button(self.root, bg="white", text="Size: 2", command=lambda: self.size(self.size_2, "2"))
        self.size_2.grid(row=1, column=13, sticky='nsew')
        self.size_3 = tk.Button(self.root, bg="white", text="Size: 3", command=lambda: self.size(self.size_3, "3"))
        self.size_3.grid(row=2, column=13, sticky='nsew')
        self.size_4 = tk.Button(self.root, bg="white", text="Size: 4", command=lambda: self.size(self.size_4, "4"))
        self.size_4.grid(row=3, column=13, sticky='nsew')
        self.size_5 = tk.Button(self.root, bg="white", text="Size: 5", command=lambda: self.size(self.size_5, "5"))
        self.size_5.grid(row=4, column=13, sticky='nsew')

        self.console_out = tk.Button(self.root, bg="white", text="print_board", command=self.print_console)
        self.console_out.grid(row=6, column=13, sticky='nsew')

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

        self.boat = "3"
        self.boat_state = "horizontal"

        self.defaultbg = self.root.cget('bg')
        self.last_clicked = None

        self.root.mainloop()

    def rotate(self):
        self.boat_state = "horizontal" if self.boat_state == "vertical" else "vertical"
        self.curr_rotation.config(text='Vertical') if self.curr_rotation.cget('text') == 'Horizontal' else self.curr_rotation.config(text='Horizontal')

    def clicked(self, button):
        if self.can_place(self.boat, button):
            if self.boat == "3":
                self.draw_boat(1, button)
            elif self.boat == "5":
                self.draw_boat(3, button)
            elif self.boat == "2":
                ## To detect and make different boats create a class boat that takes in the boards coordinates
                ## and then check every turn if their coordinates are downed or not.

                b = button.grid_info()
                button.config(bg="black")
                if self.last_clicked is not None:
                    b_last = self.last_clicked.grid_info()
                    if abs(b_last["row"] - b["row"]) == 0 and abs(b_last["column"] - b["column"]) == 1:
                        print("Horizontal")
                        self.p1_board[b_last["row"]][b_last['column']] = 1
                        self.p1_board[b["row"]][b['column']] = 1
                        self.last_clicked = None
                        return
                        # HORIZONTAL

                    elif abs(b_last["row"] - b["row"]) == 1 and abs(b_last["column"] - b["column"]) == 0:
                        print("Vertical")
                        self.p1_board[b_last["row"]][b_last['column']] = 1
                        self.p1_board[b["row"]][b['column']] = 1
                        self.last_clicked = None
                        return
                        # VERTICAL

                    else:
                        self.last_clicked.config(bg=self.defaultbg)
                        button.config(bg=self.defaultbg)
                        self.last_clicked = None
                        return
                self.last_clicked = button if self.last_clicked is None else self.last_clicked

            elif self.boat == "4":
                ## To detect and make different boats create a class boat that takes in the boards coordinates
                ## and then check every turn if their coordinates are downed or not.

                b = button.grid_info()
                button.config(bg="black")
                if self.last_clicked is not None:
                    b_last = self.last_clicked.grid_info()
                    if abs(b_last["row"] - b["row"]) == 0 and abs(b_last["column"] - b["column"]) == 1:
                        # HORIZONTAL
                        if b_last['column'] == 0 or b['column'] == 0 or b_last['column'] == 9 or b['column'] == 9:
                            self.last_clicked.config(bg=self.defaultbg)
                            button.config(bg=self.defaultbg)
                            self.last_clicked = None
                            return

                        if (self.p1_board[b_last["row"]][b_last['column'] + 1] == 0 and
                            self.p1_board[b_last["row"]][b_last['column'] - 1] == 0) and \
                                (self.p1_board[b["row"]][b['column'] - 1] == 0 and
                                 self.p1_board[b["row"]][b['column'] + 1] == 0):

                            self.p1_board[b_last["row"]][b_last['column'] - 1] = 1
                            self.p1_board[b_last["row"]][b_last['column'] + 1] = 1
                            self.p1_board[b["row"]][b['column'] - 1] = 1
                            self.p1_board[b["row"]][b['column'] + 1] = 1
                            self.last_clicked = None

                            for child in all_children(self.root, "Button"):
                                b2 = child.grid_info()
                                if (b2["column"] == b_last["column"] - 1 or b2["column"] == b_last["column"] + 1 or
                                    b2["column"] == b["column"] - 1 or b2["column"] == b["column"] + 1) and \
                                        b2['row'] == b['row']:
                                    child.config(bg='black')

                            return
                        else:
                            self.last_clicked.config(bg=self.defaultbg)
                            button.config(bg=self.defaultbg)
                            self.last_clicked = None
                            return

                    elif abs(b_last["row"] - b["row"]) == 1 and abs(b_last["column"] - b["column"]) == 0:
                        print("Vertical")
                        # VERTICAL
                        if b_last['row'] == 0 or b['row'] == 0 or b_last['row'] == 9 or b['row'] == 9:
                            self.last_clicked.config(bg=self.defaultbg)
                            button.config(bg=self.defaultbg)
                            self.last_clicked = None
                            return

                        elif (self.p1_board[b_last["row"] + 1][b_last['column']] == 0 and
                              self.p1_board[b_last["row"] - 1][b_last['column']] == 0) and \
                                (self.p1_board[b["row"] - 1][b['column']] == 0 and
                                 self.p1_board[b["row"] + 1][b['column']] == 0):

                            new_boat_coord = []

                            self.p1_board[b_last["row"] - 1][b_last['column']] = 1
                            self.p1_board[b_last["row"] + 1][b_last['column']] = 1
                            self.p1_board[b["row"] - 1][b['column']] = 1
                            self.p1_board[b["row"] + 1][b['column']] = 1
                            self.last_clicked = None

                            new_boat_coord.append([b_last["row"] - 1][b_last['column']])
                            new_boat_coord.append([b_last["row"] + 1][b_last['column']])
                            new_boat_coord.append([b_last["row"]][b_last['column'] - 1])
                            new_boat_coord.append([b_last["row"]][b_last['column'] + 1])

                            for child in all_children(self.root, "Button"):
                                b2 = child.grid_info()
                                if (b2["row"] == b_last["row"] - 1 or b2["row"] == b_last["row"] + 1 or
                                    b2["row"] == b["row"] - 1 or b2["row"] == b["row"] + 1) and b2['column'] == b[
                                    'column']:
                                    child.config(bg='black')

                            ##TODO: Create a new Boat class

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
                pass


        else:
            print("Nope")

    def can_place(self, size, button):
        ## Pour les bateaux pairs, laisser choisir les deux carres centraux au joueur puis fill le reste TMTC pd bosse un peu
        ## ET si l'player peut pas beh tu restart donc pas besoin de bouton turn, en gros reset la rota a chaque bateau DUCON
        b = button.grid_info()
        size = int(size)
        if size == 2:
            arm = 0
        elif size == 4:
            return self.p1_board[b["row"]][b["column"]] == 0
        else:
            arm = (size - 1) // 2 if size % 2 == 1 else size // 2
        if self.p1_board[b["row"]][b["column"]] == 1:
            return False
        if self.boat_state == "horizontal":
            for j in range(1, arm + 1):
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
            for j in range(1, round(arm + 1)):
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

    def draw_boat(self, arm_size, button):
        """ !USE ONLY WITH NON EVEN NUMBERS!
        :param arm_size: Size of the boat -1 and divided by 2
        :param button: button clicked
        """
        arm_size = 2 if arm_size == 1 else arm_size
        b = button.grid_info()
        button.config(bg="black")
        self.p1_board[b["row"]][b['column']] = 1
        if self.boat_state == "horizontal":
            for child in all_children(self.root, "Button"):
                info = child.grid_info()
                for j in range(1, arm_size):
                    if info['row'] == b["row"] and info['column'] == b["column"] - j:
                        child.config(bg="black")
                        self.p1_board[b["row"]][b['column'] - j] = 1
                    if info['row'] == b["row"] and info['column'] == b["column"] + j:
                        child.config(bg="black")
                        self.p1_board[b["row"]][b['column'] + j] = 1
        elif self.boat_state == "vertical":
            for child in all_children(self.root, "Button"):
                info = child.grid_info()
                for j in range(1, arm_size):
                    if info['row'] == b["row"] - j and info['column'] == b["column"]:
                        child.config(bg="black")
                        self.p1_board[b["row"] - j][b['column']] = 1
                    if info['row'] == b["row"] + j and info['column'] == b["column"]:
                        child.config(bg="black")
                        self.p1_board[b["row"] + j][b['column']] = 1

    def size(self, button, size):
        self.boat = size
        for child in all_children(self.root, "Button"):
            info = child.grid_info()
            if info["column"] == 13:
                child.config(bg="white")
        button.config(bg="green")

    def print_console(self):
        for k in self.p1_board:
            print(str(k))


class Boat:

    def __init__(self, coordinates, size):
        self.is_alive = True
        self.coordinates = coordinates
        self.size = size


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Battleship_1v1()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
