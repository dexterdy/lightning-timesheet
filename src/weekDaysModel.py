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
from QtObjectWrapper import Wrapper
from backend import getBackend
from logType import Log

QML_IMPORT_NAME = "WeekDaysModel"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class WeekDaysModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        today = date.today()
        week = today.isocalendar().week
        weekday = today.isoweekday()
        self.startDay = today - timedelta(days=weekday)
        self.backend = getBackend()
        self.days: list[list[Log]] = [[] for _ in range(7)]
        for log in self.backend.timeSheet:
            for day in range(7):
                if (
                    log.fromTime.weekday() == day
                    and log.fromTime.isocalendar().week == week
                ) or (
                    log.tillTime.weekday() == day
                    and log.tillTime.isocalendar().week == week
                ):
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
                    return Wrapper(self.days[index.row()])

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
                date: datetime = getattr(issue, field.decode())
                return (date.time().hour + date.time().minute / 60.0) / 24

    def roleNames(self) -> dict[int, bytes]:
        d = {
            0: "fromTime".encode(),
            1: "tillTime".encode(),
        }
        return d

    @Property(QObject, notify=logsChanged)  # type: ignore
    def logs(self) -> QObject:  # type: ignore
        return Wrapper(self._log)

    @logs.setter
    def logs(self, logs: Wrapper):
        if len(self._log) > 0:
            self.beginRemoveRows(QModelIndex(), 0, len(self._log))
            self._log = []
            self.endRemoveRows()
            self.logsChanged.emit()
        self.beginInsertRows(QModelIndex(), 0, len(logs.obj))
        self._log = logs.obj
        self.endInsertRows()
        self.logsChanged.emit()

    def rowCount(self, index: QModelIndex | None = None) -> int:
        return len(self._log)
