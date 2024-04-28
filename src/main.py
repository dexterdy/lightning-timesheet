from backend import createBackend, getBackend
from githubWrapper import ensureAuthAndGlobals

ensureAuthAndGlobals()
createBackend()

import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.rootContext().setContextProperty("backend", getBackend())
engine.load("./qml/main.qml")

exitCode = app.exec()
sys.exit(exitCode)
