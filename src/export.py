import typing
from pytablewriter import AbstractTableWriter, MarkdownTableWriter, ExcelXlsxTableWriter
from datetime import datetime
from github.Issue import Issue
from logType import Log


def _exportGeneric(
    logs: list[Log],
    issues: list[Issue],
    writer: type[AbstractTableWriter],
    linkFormatter: typing.Callable[[Issue], str],
    filename: str,
):
    def mapLambda(x: Log) -> list[typing.Any]:
        def getTicket(id: int):
            for i in issues:
                if i.number == id:
                    return i
            raise Exception(f"Ticket {id} not found")

        ticket = getTicket(x.ticket)
        ticketStr = linkFormatter(ticket)

        if x.userStory is not None:
            userStory = getTicket(x.userStory)
            userStoryStr = linkFormatter(userStory)
        else:
            userStoryStr = ""

        return [
            ticketStr,
            userStoryStr,
            x.fromTime,
            x.tillTime,
            x.description,
            x.tillTime - x.fromTime,
            x.atOffice,
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


def exportMD(logs: list[Log], issues: list[Issue]):
    _exportGeneric(
        logs,
        issues,
        MarkdownTableWriter,
        lambda ticket: f"[{ticket.title}]({ticket.html_url})",
        "timeSheet.md",
    )


def exportExcel(logs: list[Log], issues: list[Issue]):
    _exportGeneric(
        logs,
        issues,
        ExcelXlsxTableWriter,
        lambda ticket: f'=HYPERLINK("{ticket.html_url}";"{ticket.title}")',
        "timeSheet.xlsx",
    )
