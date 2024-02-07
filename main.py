import sys

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtCore import QTimer, QObject, pyqtSignal, pyqtSlot
from github import Auth, GithubIntegration

app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.load("main.qml")

with open("./private_key.pem", "r") as pem_file:
    auth = Auth.AppAuth(820437, pem_file.read())

# check wether app we are authenticated
# if not, open the installation page and authenticate, then save it in a file
# if yes, get authentication details from saved file

gi = GithubIntegration(auth=auth)
ins = gi.get_installation("dexterdy", "lightning-timesheet")
g = ins.get_github_for_installation()

issues = g.get_repo("dexterdy/lightning-timesheet").get_issues()
print([s.title for s in issues])

sys.exit(app.exec())
