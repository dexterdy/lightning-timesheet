import sys
from typing import Any, Dict
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, QAbstractListModel, QModelIndex, Property, Signal
from github import Auth, Github, GithubIntegration
from dotenv import dotenv_values, set_key
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
from threading import Thread

cfg = dotenv_values(".env")
client_secret = cfg.get("CLIENT_SECRET")
user_auth = cfg.get("USER_AUTH")
ins_id = cfg.get("INS_ID")
client_id = "Iv1.d6a13760097bc4c6"
app_id = 820437
install_url = "https://github.com/apps/lightning-timesheets/installations/new"


class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<html><body><h1>Authenticated</h1></body></html>".encode())
        query = urllib.parse.urlparse(self.path).query
        query = urllib.parse.parse_qs(query)
        global ins_id
        ins_id = query["installation_id"][0]


def authenticate():
    global user_auth
    global ins_id
    if ins_id == "" or ins_id is None:
        webbrowser.open(install_url, new=0, autoraise=True)

        # handle response (ins_id is in query params)
        server = HTTPServer(("localhost", 9156), AuthHandler)
        th = Thread(target=server.serve_forever)
        th.start()
        while ins_id is None or ins_id == "":
            pass
        server.shutdown()
        th.join()

    # app auth, without user auth
    with open("./private_key.pem", "r") as pem_file:
        appAuth = Auth.AppAuth(820437, pem_file.read())
    gi = GithubIntegration(auth=appAuth)

    # get user access token
    user_auth = gi.get_access_token(int(ins_id)).token
    set_key(".env", "USER_AUTH", user_auth)
    set_key(".env", "INS_ID", ins_id)


if user_auth == "" or user_auth is None:
    authenticate()

try:
    g = Github(user_auth)
    g.get_repo("dexterdy/lightning-pipelines")
except:
    authenticate()
    g = Github(user_auth)


class IssuesList(QAbstractListModel):
    def __init__(self):
        super().__init__()
        self.issues = list(g.get_repo("dexterdy/lightning-pipelines").get_issues())

    def data(self, index: QModelIndex, role: int = 0) -> Any:
        if 0 <= index.row() < self.rowCount():
            issue = self.issues[index.row()]
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
        return len(self.issues)


class Backend(QObject):
    issuesChanged = Signal(QObject)

    def __init__(self):
        super().__init__()
        self._issues = IssuesList()

    @Property(QObject, notify=issuesChanged)  # type: ignore
    def issues(self):
        return self._issues


app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
backend = Backend()
engine.quit.connect(app.quit)
engine.rootContext().setContextProperty("backend", backend)
engine.load("main.qml")

sys.exit(app.exec())
