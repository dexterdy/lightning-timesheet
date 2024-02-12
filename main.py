import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from githubIssuesModel import GithubIssuesModel
from githubWrapper import ensureAuthAndGlobals
from backend import createBackend, getBackend

ensureAuthAndGlobals()
createBackend()
app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.rootContext().setContextProperty("backend", getBackend())
engine.load("./qml/main.qml")

exitCode = app.exec()
sys.exit(exitCode)
