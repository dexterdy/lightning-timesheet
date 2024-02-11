import typing
from pytablewriter import AbstractTableWriter, MarkdownTableWriter, ExcelXlsxTableWriter
from datetime import datetime
from github.Issue import Issue


def _exportGeneric(
    logs: list[dict[str, typing.Any]],
    issues: list[Issue],
    writer: type,
    linkFormatter: typing.Callable[[Issue], str],
    filename: str,
):
    def mapLambda(x: dict[str, typing.Any]) -> list[typing.Any]:
        ticket = issues[x["ticket"] - 1]
        ticketStr = linkFormatter(ticket)
        if "userStory" in x:
            userStory = issues[x["userStory"] - 1]
            userStoryStr = linkFormatter(userStory)
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
    writer = writer(
        table_name="time sheet",
        headers=["ticket", "user story", "from", "till", "description", "duration"],
        value_matrix=matrix,
    )
    writer.dump(filename)


def exportMD(logs: list[dict[str, typing.Any]], issues: list[Issue]):
    _exportGeneric(
        logs,
        issues,
        MarkdownTableWriter,
        lambda ticket: f"[{ticket.title}]({ticket.url})",
        "timeSheet.md",
    )


def exportExcel(logs: list[dict[str, typing.Any]], issues: list[Issue]):
    _exportGeneric(
        logs,
        issues,
        ExcelXlsxTableWriter,
        lambda ticket: f'=HYPERLINK("{ticket.url}","{ticket.title}")',
        "timeSheet.xlsx",
    )
