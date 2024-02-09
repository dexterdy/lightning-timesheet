import os
import sys

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QTimer, QObject, Signal, Slot
from github import Auth, Github, GithubIntegration
from dotenv import load_dotenv
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
from threading import Thread

load_dotenv(".env")
client_secret = os.getenv("CLIENT_SECRET")
user_auth = os.getenv("USER_AUTH")
ins_id = os.getenv("INS_ID")
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


if user_auth == "" or user_auth is None:
    webbrowser.open(install_url, new=0, autoraise=True)

    # handle response (ins_id is in query params)
    server = HTTPServer(("localhost", 9156), AuthHandler)
    th = Thread(target=server.serve_forever)
    th.start()
    while ins_id is None:
        pass
    server.shutdown()
    th.join()

    # app auth, without user auth
    with open("./private_key.pem", "r") as pem_file:
        appAuth = Auth.AppAuth(820437, pem_file.read())
    gi = GithubIntegration(auth=appAuth)

    # get user access token
    user_auth = gi.get_access_token(int(ins_id)).token
    with open(".env", "a") as f:
        f.write(f"\nUSER_AUTH={user_auth}\nINS_ID={ins_id}\n")

g = Github(user_auth)


class Backend(QObject):
    def __init__(self):
        super().__init__()


app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
backend = Backend()
engine.quit.connect(app.quit)
engine.load("main.qml")
engine.rootObjects()[0].setProperty("backend", backend)

sys.exit(app.exec())
