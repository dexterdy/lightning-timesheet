from dataclasses import dataclass
from datetime import datetime


@dataclass
class Log:
    index: int
    ticket: int
    userStory: int | None
    description: str
    fromTime: datetime
    tillTime: datetime
    atOffice: bool
