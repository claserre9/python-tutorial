from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class LogEntry:
    """Une entrée de log Nginx format combined."""

    ip: str
    timestamp: datetime
    method: str
    path: str
    status: int
    size: int
    referer: str
    user_agent: str
