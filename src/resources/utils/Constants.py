import copy
import tkinter
from PIL import Image, ImageTk

from pathlib import Path
from typing import Optional, Union


# -------- Helper classes by Jari_Bou -------- #

class ImgLoader:

    def __init__(self):
        self.path = Path(__file__).parent.parent.parent

    def load_img(self, relative_path: str) -> Image:
        img = Image.open(self.path.joinpath(relative_path))
        return img

    @classmethod
    def resize_img(cls, img, size: Union[list[int, int], tuple[int, int]], get_as_tk=True) -> ImageTk.PhotoImage:
        new_img = img.resize((size[0], size[1]))
        if get_as_tk:
            new_img = ImageTk.PhotoImage(new_img)
        return new_img

    @classmethod
    def crop(cls, img, rectangle: tuple[int, int, int, int]):
        return img.crop(rectangle)

    @classmethod
    def get_as_TkImage(cls, img) -> ImageTk.PhotoImage:
        return ImageTk.PhotoImage(img)


class Position:

    def __init__(self, coordinates: Union[list[int, int], tuple[int, int]]):
        self.x = coordinates[0]
        self.y = coordinates[1]

    def __repr__(self):
        return f'<{self.__class__.__name__} at (x={self.x}, y={self.y})>'

    def get_position(self) -> tuple[int, int]:
        return self.x, self.y

    def add(self, args: str = '', **kwargs):
        if args == '':  ##This is just for fun
            x, y = 0, 0
            for key in kwargs.keys():
                if key not in ['x', 'y']:
                    raise AttributeError(f"unknows attribute '{key}' for class {self.__class__}")
                else:
                    try:
                        if key == 'x':
                            x = int(kwargs.get('x', 0))
                        elif key == 'y':
                            y = int(kwargs.get('y', 0))
                    except ValueError:
                        raise ValueError(f'invalid integer value {int(kwargs.get(key, 0))} for attribute {key}')
            self.x += x
            self.y += y
            return

        args = args.split('+')
        for arg in args:
            value = 0
            try:
                name, value = arg.split('=')
            except ValueError:
                name = arg
            try:
                if name == 'x':
                    self.x += int(value)
                elif name == 'y':
                    self.y += int(value)
                else:
                    raise AttributeError(f'unknows attribute {name} for class {self.__class__}')
            except ValueError:
                raise ValueError(f'invalid integer {value} for attribute {name}')


class Constants:

    @classmethod
    def get_path(cls) -> Path:
        return Path(__file__).parent.parent.parent

    @classmethod
    def new_board(cls) -> list[list[int]]:
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
    def all_children(cls, wid: tkinter.Tk, child_type: str) -> list:
        """ Used to return a list of all the elements on a parent

        :param child_type: Type of the child to return, 'all' returns all types
        :param wid: Window to be executed on
        :return: List of elements on wid
        """
        _list = wid.winfo_children()
        for item in _list:
            if item.winfo_children():
                _list.extend(item.winfo_children())
        return _list if child_type.lower() == "all" else [child for child in _list if
                                                          str(child.winfo_class()) == child_type]

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
    def get_img(cls, path: Union[Path, str], size: int = 0) -> ImageTk.PhotoImage:
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
    def convert_str_to_list(cls, str_list: str) -> list[Union[float, str]]:
        str_list.strip()
        if not (str_list[0] == '[' and str_list[len(str_list) - 1] == ']'):
            raise ValueError(f'Cannot convert {str_list} to list')
        values = str_list[1:-1].split(',')
        L = []
        for val in values:
            try:
                L.append(float(val))
            except ValueError:
                L.append(val.strip())
        return L

    @classmethod
    def print_matrice(cls, matrice: list[list[any, any]], separator=', '):
        for row in matrice:
            line = ''
            for column in row:
                line += str(column) + separator
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

    @classmethod
    def get_flattened(cls, seq) -> list:
        se = copy.deepcopy(seq)
        flattened_list = []
        for sub in se:
            t = type(sub)
            if t is tuple or t is list:
                for sub2 in cls.get_flattened(sub):
                    flattened_list.append(sub2)
            else:
                flattened_list.append(sub)
        return flattened_list
