import typing
from PySide6.QtCore import QObject, Slot, Property


class Wrapper(QObject):
    def __init__(self, obj: typing.Any):
        super().__init__()
        self.obj = obj
