from datetime import datetime
import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Property
import globals
from githubIssuesModel import GithubIssuesModel


class Backend(QObject):
    def __init__(self):
        super().__init__()
        self.selectedTicket: str | int | None = None
        self.selectedUserStory: str | int | None = None
        self.date: datetime = datetime.now()
        self.fromTime: datetime | None = None
        self.tillTime: datetime | None = None
        self.description: str = ""

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
            return "Could not set 'from' time. Please ensure the time is valid."

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
            return "Could not set 'till' time. Please ensure the time is valid."

    @Slot(str)
    def setDescription(self, description: str):
        self.description = description

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
            return "'Till' time must be later than 'from' time."
        return ""

    @Slot()
    def reset(self):
        self.selectedTicket = None
        self.selectedUserStory = None
        self.date = datetime.now()
        self.fromTime = None
        self.tillTime = None
        self.description = ""

    @Property(str, constant=True)  # type: ignore
    def defaultYear(self):
        return str(datetime.now().year)

    @Property(str, constant=True)  # type: ignore
    def defaultMonth(self):
        return str(datetime.now().month)

    @Property(str, constant=True)  # type: ignore
    def defaultDay(self):
        return str(datetime.now().day)


app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
backend = Backend()
engine.quit.connect(app.quit)
engine.rootContext().setContextProperty("backend", backend)
engine.load("main.qml")

sys.exit(app.exec())
