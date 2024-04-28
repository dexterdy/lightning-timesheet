import typing
from PySide6.QtCore import QObject

T = typing.TypeVar("T")


class Wrapper(QObject, typing.Generic[T]):
    def __init__(self, obj: T):
        super().__init__()
        self.obj = obj
