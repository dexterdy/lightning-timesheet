from datetime import datetime, date
import typing
from PySide6.QtCore import QObject, Slot, Property
from githubWrapper import getIssues
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

    def convertDate(entry: dict[str, str]) -> Log:
        return Log(
            ticket=int(entry["ticket"]),
            userStory=int(entry["userStory"]) if entry["userStory"] else None,
            description=entry["description"],
            fromTime=datetime.fromisoformat(entry["fromTime"]),
            tillTime=datetime.fromisoformat(entry["tillTime"]),
            atOffice=bool(entry["atOffice"]),
        )

    return list(map(convertDate, timeSheet))


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
        self.selectedTicket: int | None = None
        self.selectedUserStory: int | None = None
        self.date: date = date.today()
        self.fromTime: datetime | None = None
        self.tillTime: datetime | None = None
        self.description: str = ""
        self.atOffice = True
        self.timeSheet = timeSheet

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
        self.timeSheet.append(
            Log(
                ticket=self.selectedTicket,
                userStory=self.selectedUserStory,
                fromTime=self.fromTime,
                tillTime=self.tillTime,
                description=self.description,
                atOffice=self.atOffice,
            )
        )
        storeJson(self.timeSheet)
        self.reset()
        return ""

    @Slot()
    def reset(self):
        self.selectedTicket = None
        self.selectedUserStory = None
        self.date = date.today()
        self.fromTime = None
        self.tillTime = None
        self.description = ""
        self.atOffice = False

    @Slot(int)
    def export(self, type: int):
        if type == 1:
            exportMD(self.timeSheet, getIssues())
        elif type == 2:
            exportExcel(self.timeSheet, getIssues())

    @Property(str, constant=True)  # type: ignore
    def defaultYear(self):
        return str(self.date.year)

    @Property(str, constant=True)  # type: ignore
    def defaultMonth(self):
        return "%02d" % self.date.month

    @Property(str, constant=True)  # type: ignore
    def defaultDay(self):
        return "%02d" % self.date.day


# I could implement some safety thing that makes sure only one backend exists, but meh.
def createBackend():
    global backend
    backend = Backend(loadJson())


# Same thing with checking for if backend actually has been created.
def getBackend() -> Backend:
    global backend
    return backend
