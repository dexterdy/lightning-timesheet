import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from githubIssuesModel import GithubIssuesModel
from backend import backend


app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.rootContext().setContextProperty("backend", backend)
engine.load("./qml/main.qml")

exitCode = app.exec()
sys.exit(exitCode)
