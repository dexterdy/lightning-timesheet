import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject
import globals
from githubIssuesModel import GithubIssuesModel


class Backend(QObject):
    def __init__(self):
        super().__init__()


app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
backend = Backend()
engine.quit.connect(app.quit)
engine.rootContext().setContextProperty("backend", backend)
engine.load("main.qml")

sys.exit(app.exec())
