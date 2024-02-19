from githubWrapper import getIssues


def getTicket(id: int):
    issues = getIssues()
    for i in issues:
        if i.number == id:
            return i
    raise Exception(f"Ticket {id} not found")
