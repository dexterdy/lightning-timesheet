import typing
from pytablewriter import MarkdownTableWriter
from datetime import datetime
from github.Issue import Issue


def exportMD(logs: list[dict[str, typing.Any]], issues: list[Issue]):
    def mapLambda(x: dict[str, typing.Any]) -> list[typing.Any]:
        ticket = issues[x["ticket"] - 1]
        ticketStr = f"[{ticket.title}]({ticket.url})"
        if "userStory" in x:
            userStory = issues[x["userStory"] - 1]
            userStoryStr = f"[{userStory.title}]({userStory.url})"
        else:
            userStoryStr = ""
        fromTime = x["fromTime"]
        tillTime = x["tillTime"]
        if "description" in x:
            description = x["description"]
        else:
            description = ""
        duration = datetime.fromisoformat(tillTime) - datetime.fromisoformat(fromTime)

        return [
            ticketStr,
            userStoryStr,
            fromTime,
            tillTime,
            description,
            duration,
        ]

    matrix = list(map(mapLambda, logs))
    matrix.sort(key=lambda x: datetime.fromisoformat(str(x[2])))
    writer = MarkdownTableWriter(
        table_name="time sheet",
        headers=["ticket", "user story", "from", "till", "description", "duration"],
        value_matrix=matrix,
    )
    writer.dump("timeSheet.md")
