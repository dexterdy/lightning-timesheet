import typing
from pytablewriter import AbstractTableWriter, MarkdownTableWriter, ExcelXlsxTableWriter
from datetime import datetime
from github.Issue import Issue


def _exportGeneric(
    logs: list[dict[str, typing.Any]],
    issues: list[Issue],
    writer: type[AbstractTableWriter],
    linkFormatter: typing.Callable[[Issue], str],
    filename: str,
):
    def mapLambda(x: dict[str, typing.Any]) -> list[typing.Any]:
        ticket = issues[x["ticket"] - 1]
        ticketStr = linkFormatter(ticket)

        if "userStory" in x and x["userStory"] is not None:
            userStory = issues[x["userStory"] - 1]
            userStoryStr = linkFormatter(userStory)
        else:
            userStoryStr = ""

        fromTime = x["fromTime"]
        tillTime = x["tillTime"]
        duration = datetime.fromisoformat(tillTime) - datetime.fromisoformat(fromTime)

        if "description" in x and x["description"] is not None:
            description = x["description"]
        else:
            description = ""

        atOffice = x["atOffice"]

        return [
            ticketStr,
            userStoryStr,
            fromTime,
            tillTime,
            description,
            duration,
            atOffice,
        ]

    matrix = list(map(mapLambda, logs))
    matrix.sort(key=lambda x: datetime.fromisoformat(str(x[2])))
    writerInstance = writer(
        table_name="time sheet",
        headers=[
            "ticket",
            "user story",
            "from",
            "till",
            "description",
            "duration",
            "at the office",
        ],
        value_matrix=matrix,
    )
    writerInstance.dump(filename, close_after_write=True)


def exportMD(logs: list[dict[str, typing.Any]], issues: list[Issue]):
    _exportGeneric(
        logs,
        issues,
        MarkdownTableWriter,
        lambda ticket: f"[{ticket.title}]({ticket.html_url})",
        "timeSheet.md",
    )


def exportExcel(logs: list[dict[str, typing.Any]], issues: list[Issue]):
    _exportGeneric(
        logs,
        issues,
        ExcelXlsxTableWriter,
        lambda ticket: f'=HYPERLINK("{ticket.html_url}";"{ticket.title}")',
        "timeSheet.xlsx",
    )
