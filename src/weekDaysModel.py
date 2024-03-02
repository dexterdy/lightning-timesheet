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
from getIssueFromInt import getTicket
from logType import Log

QML_IMPORT_NAME = "WeekDaysModel"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class WeekDaysModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.backend = getBackend()
        self.days: list[list[Log]] = [[] for _ in range(7)]
        self.updateDays(self.backend.timeSheet, self.backend.startDay)
        self.backend.timesheetChanged.connect(
            lambda x: self.updateDays(x, self.backend.startDay)
        )
        self.backend.startDayChanged.connect(
            lambda x: self.updateDays(self.backend.timeSheet, x)
        )

    @Slot()
    def updateDays(self, timeSheet: Wrapper[list[Log]], startDay: Wrapper[date]):
        self.beginResetModel()
        week = startDay.obj.isocalendar().week
        self.days = [[] for _ in range(7)]
        for log in timeSheet.obj:
            if log.fromTime.isocalendar().week == week:
                self.days[log.fromTime.isocalendar().weekday - 1].append(log)
            if (
                log.tillTime.isocalendar().week == week
                and log.tillTime.date() != log.fromTime.date()
            ):
                self.days[log.tillTime.isocalendar().weekday - 1].append(log)
        self.endResetModel()

    def data(self, index: QModelIndex, role: int = 0) -> Any:
        if 0 <= index.row() < self.rowCount():
            day: date = self.backend.startDay.obj + timedelta(days=index.row())
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
        self._log: list[Log] = []

    def data(self, index: QModelIndex, role: int = 0) -> Any:
        if 0 <= index.row() < self.rowCount():
            log = self._log[index.row()]
            field = self.roleNames().get(role)
            if field:
                field = field.decode()
                if field == "fromTime" or field == "tillTime":
                    date: datetime = getattr(log, field)
                    return (date.time().hour + date.time().minute / 60.0) / 24
                elif field == "title":
                    issue = getTicket(log.ticket)
                    return getattr(issue, field)
                else:
                    return getattr(log, field)

    def roleNames(self) -> dict[int, bytes]:
        d = {
            0: "fromTime".encode(),
            1: "tillTime".encode(),
            2: "title".encode(),
            3: "index".encode(),
        }
        return d

    def get_logs(self) -> QObject:
        return Wrapper(self._log)

    def set_logs(self, logs: Wrapper[list[Log]]):
        self.beginResetModel()
        self._log = logs.obj
        self.logsChanged.emit()
        self.endResetModel()

    logs = Property(QObject, get_logs, set_logs, notify=logsChanged)  # type: ignore

    def rowCount(self, index: QModelIndex | None = None) -> int:
        return len(self._log)
