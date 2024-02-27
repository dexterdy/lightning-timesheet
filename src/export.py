import typing
from pytablewriter import AbstractTableWriter, MarkdownTableWriter
import xlsxwriter
from datetime import datetime, timedelta
from github.Issue import Issue
from logType import Log

T = typing.TypeVar("T")


def _getMatrix(
    logs: list[Log],
    issues: list[Issue],
    linkFormatter: typing.Callable[[Issue], T],
):
    def mapLambda(
        x: Log,
    ) -> tuple[T, T | None, datetime, datetime, str, timedelta, bool]:
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
            userStoryStr = None

        return (
            ticketStr,
            userStoryStr,
            x.fromTime,
            x.tillTime,
            x.description,
            x.tillTime - x.fromTime,
            x.atOffice,
        )

    matrix = list(map(mapLambda, logs))
    matrix.sort(key=lambda x: x[2])
    return matrix


def _exportGeneric(
    logs: list[Log],
    issues: list[Issue],
    writer: type[AbstractTableWriter],
    linkFormatter: typing.Callable[[Issue], str],
    filename: str,
):
    matrix = _getMatrix(logs, issues, linkFormatter)
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
    workbook = xlsxwriter.Workbook("timeSheet.xlsx")
    worksheet = workbook.add_worksheet()
    matrix = _getMatrix(logs, issues, lambda x: (x.html_url, x.title))
    header_format = workbook.add_format(
        {
            "bold": True,
            "align": "center",
            "font_color": "white",
            "bg_color": "#2d8cff",
            "border": 2,
            "border_color": "black",
        }
    )

    column_widths = [
        (30, "ticket"),
        (30, "user story"),
        (16, "from"),
        (16, "till"),
        (60, "description"),
        (12, "duration"),
        (12, "at the office"),
    ]
    for i, (width, name) in enumerate(column_widths):
        worksheet.set_column(i, i, width)
        worksheet.write(0, i, name, header_format)

    date_format = workbook.add_format({"num_format": "yyyy-mm-dd hh:mm"})
    time_format = workbook.add_format({"num_format": "hh:mm"})
    text_format = workbook.add_format({"text_wrap": True})
    link_format = workbook.add_format(
        {"font_color": "#0066cc", "underline": True, "text_wrap": True}
    )

    for i, row in enumerate(matrix, start=1):
        for j, col in enumerate(row):
            if type(col) is tuple:
                worksheet.write_url(i, j, col[0], link_format, string=col[1])
            elif type(col) is datetime:
                worksheet.write_datetime(i, j, col, date_format)
            elif type(col) is timedelta:
                worksheet.write_datetime(i, j, col, time_format)
            elif col is not None:
                worksheet.write(i, j, col, text_format)
    workbook.close()
