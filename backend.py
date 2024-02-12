from datetime import datetime, date
import typing
from PySide6.QtCore import QObject, Slot, Property
from githubWrapper import getIssues
import json
from export import exportMD, exportExcel

try:
    with open("storedLogs.json", "r") as storeFile:
        timeSheet: list[dict[str, typing.Any]] = json.load(storeFile)["timeSheet"]
except:
    with open("storedLogs.json", "w") as storeFile:
        storeFile.write('{"timeSheet": []}')
    with open("storedLogs.json", "r") as storeFile:
        timeSheet: list[dict[str, typing.Any]] = json.load(storeFile)["timeSheet"]


class Backend(QObject):
    def __init__(self):
        super().__init__()
        self.selectedTicket: str | int | None = None
        self.selectedUserStory: str | int | None = None
        self.date: date = date.today()
        self.fromTime: datetime | None = None
        self.tillTime: datetime | None = None
        self.description: str = ""
        self.atOffice = True

    @Slot(int)
    def selectTicket(self, number: int):
        self.selectedTicket = number

    @Slot(int)
    def selectUserStory(self, number: int):
        self.selectedUserStory = number

    @Slot(str)
    def setTicketDescription(self, description: str):
        self.selectedTicket = description

    @Slot(str)
    def setUserStoryDescription(self, description: str):
        self.selectedUserStory = description

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
        timeSheet.append(
            {
                "ticket": self.selectedTicket,
                "userStory": self.selectedUserStory,
                "fromTime": self.fromTime.isoformat(),
                "tillTime": self.tillTime.isoformat(),
                "description": self.description,
                "atOffice": self.atOffice,
            }
        )
        with open("storedLogs.json", "w") as storeFile:
            json.dump({"timeSheet": timeSheet}, storeFile)
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
            exportMD(timeSheet, getIssues())
        elif type == 2:
            exportExcel(timeSheet, getIssues())

    @Property(str, constant=True)  # type: ignore
    def defaultYear(self):
        return str(self.date.year)

    @Property(str, constant=True)  # type: ignore
    def defaultMonth(self):
        return "%02d" % self.date.month

    @Property(str, constant=True)  # type: ignore
    def defaultDay(self):
        return "%02d" % self.date.day


backend = Backend()
