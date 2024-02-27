import typing
from PySide6.QtCore import QObject, Slot, Property

T = typing.TypeVar("T")


class Wrapper(QObject, typing.Generic[T]):
    def __init__(self, obj: T):
        super().__init__()
        self.obj = obj
