from typing import Any
from PySide6.QtCore import (
    QAbstractListModel,
    QModelIndex,
    Slot,
    Property,
    Signal,
    QObject,
)
from PySide6.QtQml import QmlElement
from datetime import date, datetime, timedelta
from backend import getBackend
from logType import Log

QML_IMPORT_NAME = "WeekDaysModel"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class WeekDaysModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        today = date.today()
        weekday = today.isoweekday()
        self.startDay = today - timedelta(days=weekday)
        self.backend = getBackend()
        self.days: list[list[Log]] = [[] for _ in range(7)]
        for log in self.backend.timeSheet:
            for day in range(7):
                if log.fromTime.weekday == day or log.tillTime.weekday == day:
                    self.days[day].append(log)

    def data(self, index: QModelIndex, role: int = 0) -> Any:
        if 0 <= index.row() < self.rowCount():
            day = self.startDay + timedelta(days=index.row())
            field = self.roleNames().get(role)
            if field:
                field = field.decode()
                if field == "weekday":
                    return day.strftime("%a")
                elif field == "dateStr":
                    return day.strftime("%d %b")
                elif field == "dayLogs":
                    return self.days[index.row()]

    def roleNames(self) -> dict[int, bytes]:
        d = {
            0: "weekday".encode(),
            1: "dateStr".encode(),
            2: "dayLogs".encode(),
        }
        return d

    def rowCount(self, index: QModelIndex | None = None) -> int:
        return len(self.days)


QML_IMPORT_NAME = "LogsModel"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class LogsModel(QAbstractListModel):
    logsChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._log = []

    def data(self, index: QModelIndex, role: int = 0) -> Any:
        if 0 <= index.row() < self.rowCount():
            issue = self._log[index.row()]
            field = self.roleNames().get(role)
            if field:
                return getattr(issue, field.decode())

    def roleNames(self) -> dict[int, bytes]:
        d = {}
        return d

    @Property(QObject, notify=logsChanged)  # type: ignore
    def logs(self) -> list[Log]:  # type: ignore
        return self._log

    @logs.setter
    def logs(self, logs: list[Log]):
        self._log = logs

    def rowCount(self, index: QModelIndex | None = None) -> int:
        return len(self._log)
