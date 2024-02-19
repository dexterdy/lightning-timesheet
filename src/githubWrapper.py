from github import Auth, Github, GithubIntegration
from github.Issue import Issue
from dotenv import dotenv_values, set_key
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
from threading import Thread


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


def getGithub():
    global g
    try:
        g.get_repo("dexterdy/lightning-pipelines")  # just to test
    except:
        authenticate()
        g = Github(user_auth)
    return g


def syncIssues() -> list[Issue]:
    g = getGithub()
    global issues
    issues = list(g.get_repo("dexterdy/lightning-pipelines").get_issues(state="all"))
    return issues


def getIssues() -> list[Issue]:
    global issues
    return issues


# has to be run once at the start of the program.
# safetey guarantees and checks? Meh
def ensureAuthAndGlobals():
    global cfg
    cfg = dotenv_values(".env")

    global client_secret
    client_secret = cfg.get("CLIENT_SECRET")

    global user_auth
    user_auth = cfg.get("USER_AUTH")

    global ins_id
    ins_id = cfg.get("INS_ID")

    global client_id
    client_id = "Iv1.d6a13760097bc4c6"

    global app_id
    app_id = 820437

    global install_url
    install_url = "https://github.com/apps/lightning-timesheets/installations/new"

    if user_auth == "" or user_auth is None:
        authenticate()

    global g
    g = Github(user_auth)

    global issues
    issues = syncIssues()
