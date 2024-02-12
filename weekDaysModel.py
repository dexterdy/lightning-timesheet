from threading import Thread
from typing import Any, Dict
from PySide6.QtCore import (
    QAbstractListModel,
    QModelIndex,
    Slot,
)
from PySide6.QtQml import QmlElement
from thefuzz import process, fuzz
from githubWrapper import getIssues
from github.Issue import Issue

QML_IMPORT_NAME = "WeekDaysModel"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class WeekDaysModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.days = []

    def data(self, index: QModelIndex, role: int = 0) -> Any:
        if 0 <= index.row() < self.rowCount():
            day = self.days[index.row()]
            field = self.roleNames().get(role)
            if field:
                return getattr(day, field.decode())

    def roleNames(self) -> Dict[int, bytes]:
        d = {}
        return d

    def rowCount(self, index: QModelIndex | None = None) -> int:
        return len(self.days)
