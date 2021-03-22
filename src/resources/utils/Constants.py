from enum import Enum
from PIL import Image, ImageTk


class Constants(Enum):

    @classmethod
    def new_board(cls):
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
    def all_children(cls, wid, child_type):
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

    @classmethod
    def remove_duplicates(cls, List):
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
    def get_img(cls, path, size=0):
        """ resources\\images\\XXX """
        img = Image.open(path)
        if size != 0:
            img = img.resize((size, size))
        photo = ImageTk.PhotoImage(img)
        return photo
