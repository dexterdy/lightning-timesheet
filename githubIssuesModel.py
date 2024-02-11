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

QML_IMPORT_NAME = "GithubIssuesModel"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class GithubIssuesModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.issues = getIssues()
        self.filteredIssues = self.issues[:7]

    def data(self, index: QModelIndex, role: int = 0) -> Any:
        if 0 <= index.row() < self.rowCount():
            issue = self.filteredIssues[index.row()]
            field = self.roleNames().get(role)
            if field:
                return getattr(issue, field.decode())

    def roleNames(self) -> Dict[int, bytes]:
        d = {
            0: "title".encode(),
            1: "number".encode(),
        }
        return d

    def rowCount(self, index: QModelIndex | None = None) -> int:
        return len(self.filteredIssues)

    @Slot(str)
    def filterIssues(self, text: str):
        self.beginRemoveRows(QModelIndex(), 0, 6)
        self.filteredIssues = []
        self.endRemoveRows()
        self.beginInsertRows(QModelIndex(), 0, 6)
        if text == "":
            self.reset()
        else:
            result = process.extract(
                text,
                self.issues,
                limit=7,
                scorer=fuzz.partial_ratio,
                processor=(
                    lambda x: x.title.lower() if type(x) is Issue else x.lower()
                ),
            )
            self.filteredIssues = [x[0] for x in result]
        self.endInsertRows()

    @Slot()
    def updateIssues(self):
        def internal():
            self.issues = getIssues()
            self.beginRemoveRows(QModelIndex(), 0, 6)
            self.filteredIssues = []
            self.endRemoveRows()
            self.beginInsertRows(QModelIndex(), 0, 6)
            self.reset()
            self.endInsertRows()

        backgroundFetch = Thread(target=internal)
        backgroundFetch.start()

    def reset(self):
        self.filteredIssues = self.issues[:7]
