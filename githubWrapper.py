from github import Auth, Github, GithubIntegration
from github.Issue import Issue
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
g = None


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


def getGithub():
    global g
    try:
        if g is None:
            g = Github(user_auth)
        g.get_repo("dexterdy/lightning-pipelines")  # just to test
    except:
        authenticate()
        g = Github(user_auth)
    return g


def getIssues() -> list[Issue]:
    g = getGithub()
    try:
        return list(g.get_repo("dexterdy/lightning-pipelines").get_issues())
    except:
        authenticate()
        g = Github(user_auth)
        return list(g.get_repo("dexterdy/lightning-pipelines").get_issues())
