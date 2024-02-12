from dataclasses import dataclass
from re import T
from typing import Any, Dict
from PySide6.QtCore import (
    QAbstractListModel,
    QModelIndex,
    Slot,
)
from PySide6.QtQml import QmlElement
from datetime import date, datetime, timedelta
from backend import getBackend
from logType import Log

QML_IMPORT_NAME = "WeekDaysModel"
QML_IMPORT_MAJOR_VERSION = 1


@dataclass
class day:
    day: date
    logs: list[Log]


@QmlElement
class WeekDaysModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        today = date.today()
        weekday = today.isoweekday()
        start = today - timedelta(days=weekday)
        self.backend = getBackend()
        days = [start + timedelta(days=d) for d in range(7)]
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
