import tkinter
from enum import Enum
from PIL import Image, ImageTk

from pathlib import Path


class ImgLoader:

    def __init__(self):
        self.path = Path(__file__).parent.parent.parent

    def load_img(self, relative_path) -> Image:
        img = Image.open(self.path.joinpath(relative_path))
        return img

    @classmethod
    def resize_img(cls, img, size, get_as_tk=True) -> ImageTk.PhotoImage:
        new_img = img.resize((size[0], size[1]))
        if get_as_tk:
            new_img = ImageTk.PhotoImage(new_img)
        return new_img

    @classmethod
    def crop(cls, img, rectangle):
        return img.crop(rectangle)

    @classmethod
    def get_as_TkImage(cls, img) -> ImageTk.PhotoImage:
        return ImageTk.PhotoImage(img)


class Position:

    def __init__(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]

    def __repr__(self):
        return f'{self.__class__.__name__} at ( x={self.x}, y={self.y} )'

    def get_position(self) -> tuple[int, int]:
        return self.x, self.y

    def add(self, args):
        args = args.split('+')
        for arg in args:
            value = 0
            try:
                name, value = arg.split('=')
            except ValueError:
                name = arg
            if name == 'x':
                self.x += int(value)
            elif name == 'y':
                self.y += int(value)
            else:
                raise AttributeError(f'unknows attribute {name} for class {self.__class__}')


class Constants(Enum):

    @classmethod
    def get_path(cls) -> Path:
        return Path(__file__).parent.parent.parent

    @classmethod
    def new_board(cls) -> list:
        return [
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

    @classmethod
    def all_children(cls, wid, child_type: str) -> list:
        """ Used to return a list of all the elements on a parent

        :param child_type: Type of the child to return, 'all' returns all types
        :param wid: Window to be executed on
        :return: List of elements on wid
        """
        _list = wid.winfo_children()
        for item in _list:
            if item.winfo_children():
                _list.extend(item.winfo_children())
        return _list if child_type.lower() == "all" else [child for child in _list if str(child.winfo_class()) == child_type]

    @classmethod
    def remove_duplicates(cls, List: list) -> list:
        """ Removes dupes from a given List
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

    @classmethod
    def get_img(cls, path, size=0) -> ImageTk.PhotoImage:
        """ resources\\images\\XXX """
        img = Image.open(path)
        if size != 0:
            img = img.resize((size, size))
        photo = ImageTk.PhotoImage(img)
        return photo

    @classmethod
    def regroup_list(cls, List: list, size_of_sublist: int) -> list[list]:
        return [List[n:n + size_of_sublist] for n in range(0, len(List), size_of_sublist)]

    @classmethod
    def print_matrice(cls, matrice, separator=', '):
        for row in matrice:
            line = ''
            for column in row:
                line += column + separator
            print(line)

    @classmethod
    def center(cls, win: tkinter.Tk):
        """
        centers a tkinter window
        :param win: the main window or Toplevel window to center
        """
        win.update_idletasks()
        width = win.winfo_reqwidth()
        height = win.winfo_reqheight()
        # width = self.root.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        # height = self.root.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()

    @classmethod
    def set_color(cls, root: tkinter.Tk, color: str, elements='All'):
        root['bg'] = color
        for element in cls.all_children(root, elements):
            element['bg'] = color

