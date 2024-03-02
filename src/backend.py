from datetime import datetime, date
import typing
from PySide6.QtCore import QObject, Slot, Property, Signal
from QtObjectWrapper import Wrapper
from getIssueFromInt import getTicket
from githubWrapper import getIssues, syncIssues
import json
from export import exportMD, exportExcel
from logType import Log


def loadJson() -> list[Log]:
    try:
        with open("storedLogs.json", "r") as storeFile:
            timeSheet: list[dict[str, typing.Any]] = json.load(storeFile)["timeSheet"]
    except:
        with open("storedLogs.json", "w") as storeFile:
            storeFile.write('{"timeSheet": []}')
        with open("storedLogs.json", "r") as storeFile:
            timeSheet: list[dict[str, typing.Any]] = json.load(storeFile)["timeSheet"]

    def toLog(entry: dict[str, str], index: int) -> Log:
        return Log(
            index=index,
            ticket=int(entry["ticket"]),
            userStory=int(entry["userStory"]) if entry["userStory"] else None,
            description=entry["description"],
            fromTime=datetime.fromisoformat(entry["fromTime"]),
            tillTime=datetime.fromisoformat(entry["tillTime"]),
            atOffice=bool(entry["atOffice"]),
        )

    return list(map(lambda x: toLog(x[1], x[0]), enumerate(timeSheet)))


def storeJson(timeSheet: list[Log]):
    def convertDate(log: Log) -> dict[str, str]:
        entry = {
            "ticket": log.ticket,
            "userStory": log.userStory,
            "fromTime": log.fromTime.isoformat(),
            "tillTime": log.tillTime.isoformat(),
            "description": log.description,
            "atOffice": log.atOffice,
        }
        return entry

    timeSheetStr = list(map(convertDate, timeSheet))

    with open("storedLogs.json", "w") as storeFile:
        json.dump({"timeSheet": timeSheetStr}, storeFile)


class Backend(QObject):
    def __init__(self, timeSheet: list[Log]):
        super().__init__()
        # if not none, we are in editing mode. Otherwise, we are in write mode
        self.editingLog: int | None = None
        self.selectedTicket: int | None = None
        self.selectedUserStory: int | None = None
        self.date: date = date.today()
        self.fromTime: datetime | None = None
        self.tillTime: datetime | None = None
        self.description: str = ""
        self.atOffice = True
        self._timeSheet = timeSheet

    @Slot(int)
    def setEditMode(self, index: int):
        self.editingLog = index
        self.selectedTicket = self._timeSheet[index].ticket
        self.selectedUserStory = self._timeSheet[index].userStory
        self.date = self._timeSheet[index].fromTime.date()
        self.fromTime = self._timeSheet[index].fromTime
        self.tillTime = self._timeSheet[index].tillTime
        self.description = self._timeSheet[index].description
        self.atOffice = self._timeSheet[index].atOffice

    @Slot(int)
    def selectTicket(self, number: int):
        self.selectedTicket = number

    @Slot(int)
    def selectUserStory(self, number: int):
        self.selectedUserStory = number

    @Slot(int, int, int, result=str)
    def setDate(self, yyyy, mm, dd):
        try:
            self.date = datetime(yyyy, mm, dd)
            return ""
        except:
            return "Could not set date. Please ensure the date is valid."

    @Slot(int, int, result=str)
    def setFromTime(self, hh, mm):
        if not self.date:
            return "Date is not set. Please set the date first."
        try:
            self.fromTime = datetime(
                self.date.year, self.date.month, self.date.day, hh, mm
            )
            return ""
        except:
            return "Could not set 'From' time. Please ensure the time is valid."

    @Slot(int, int, result=str)
    def setTillTime(self, hh, mm):
        if not self.date:
            return "Date is not set. Please set the date first."
        try:
            self.tillTime = datetime(
                self.date.year, self.date.month, self.date.day, hh, mm
            )
            return ""
        except:
            return "Could not set 'Till' time. Please ensure the time is valid."

    @Slot(str)
    def setDescription(self, description: str):
        self.description = description

    @Slot(bool)
    def setAtOffice(self, atOffice: bool):
        self.atOffice = atOffice

    @Slot(result=str)
    def submit(self):
        if (
            not self.selectedTicket
            or not self.date
            or not self.fromTime
            or not self.tillTime
        ):
            return "All required fields must be set before submission."
        if self.tillTime <= self.fromTime:
            return "'Till' time must be later than 'From' time."
        if self.editingLog is not None:
            self._timeSheet[self.editingLog] = Log(
                self.editingLog,
                ticket=self.selectedTicket,
                userStory=self.selectedUserStory,
                fromTime=self.fromTime,
                tillTime=self.tillTime,
                description=self.description,
                atOffice=self.atOffice,
            )
            self.editingLog = None
        else:
            self._timeSheet.append(
                Log(
                    len(self._timeSheet),
                    ticket=self.selectedTicket,
                    userStory=self.selectedUserStory,
                    fromTime=self.fromTime,
                    tillTime=self.tillTime,
                    description=self.description,
                    atOffice=self.atOffice,
                )
            )
        storeJson(self._timeSheet)
        self.timesheetChanged.emit(self.timeSheet)
        self.reset()
        return ""

    @Slot()
    def reset(self):
        self.editingLog = None
        self.selectedTicket = None
        self.selectedUserStory = None
        self.date = date.today()
        self.fromTime = None
        self.tillTime = None
        self.description = ""
        self.atOffice = False

    @Slot(int)
    def export(self, type: int):
        if len(self._timeSheet) == 0 or not self._timeSheet:
            return
        if type == 1:
            exportMD(self._timeSheet, getIssues())
        elif type == 2:
            exportExcel(self._timeSheet, getIssues())

    @Slot(result=str)
    def initialYear(self):
        return str(self.date.year)

    @Slot(result=str)
    def initialMonth(self):
        return "%02d" % self.date.month

    @Slot(result=str)
    def initialDay(self):
        return "%02d" % self.date.day

    @Slot(result=str)
    def initialTicketText(self):
        if self.selectedTicket is None:
            return ""
        return getTicket(self.selectedTicket).title

    @Slot(result=str)
    def initialUserStoryText(self):
        if self.selectedUserStory is None:
            return ""
        return getTicket(self.selectedUserStory).title

    @Slot(result=str)
    def initialFromHour(self):
        if self.fromTime is None:
            return ""
        return "%02d" % self.fromTime.hour

    @Slot(result=str)
    def initialFromMinute(self):
        if self.fromTime is None:
            return ""
        return "%02d" % self.fromTime.minute

    @Slot(result=str)
    def initialTillHour(self):
        if self.tillTime is None:
            return ""
        return "%02d" % self.tillTime.hour

    @Slot(result=str)
    def initialTillMinute(self):
        if self.tillTime is None:
            return ""
        return "%02d" % self.tillTime.minute

    @Slot(result=str)
    def initialDescription(self):
        return self.description

    @Slot(result=bool)
    def initialAtOffice(self):
        return self.atOffice

    timesheetChanged = Signal(QObject)

    @Property(QObject, notify=timesheetChanged)  # type: ignore
    def timeSheet(self) -> QObject:
        return Wrapper(self._timeSheet)


# I could implement some safety thing that makes sure only one backend exists, but meh.
def createBackend():
    global backend
    backend = Backend(loadJson())


# Same thing with checking for if backend actually has been created.
def getBackend() -> Backend:
    global backend
    return backend
