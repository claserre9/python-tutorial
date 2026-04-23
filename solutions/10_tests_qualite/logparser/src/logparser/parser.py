import logging
import re
from collections.abc import Iterator
from datetime import datetime
from pathlib import Path

from .models import LogEntry

logger = logging.getLogger(__name__)


class ParseError(ValueError):
    """Ligne de log illisible."""


# Format Nginx "combined" :
# IP - - [DATE] "METHOD PATH HTTP/VER" STATUS SIZE "REFERER" "UA"
_LINE_RE = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ '
    r'\[(?P<ts>[^\]]+)\] '
    r'"(?P<method>\S+) (?P<path>\S+) \S+" '
    r'(?P<status>\d+) (?P<size>\d+|-) '
    r'"(?P<referer>[^"]*)" "(?P<ua>[^"]*)"'
)


def parse_line(line: str) -> LogEntry:
    """Parse une ligne. Lève ParseError si la ligne est invalide."""
    m = _LINE_RE.match(line.strip())
    if not m:
        raise ParseError(f"ligne illisible: {line!r}")

    try:
        ts = datetime.strptime(m["ts"], "%d/%b/%Y:%H:%M:%S %z")
        size = 0 if m["size"] == "-" else int(m["size"])
    except ValueError as e:
        raise ParseError(f"champs invalides: {line!r}") from e

    return LogEntry(
        ip=m["ip"],
        timestamp=ts,
        method=m["method"],
        path=m["path"],
        status=int(m["status"]),
        size=size,
        referer=m["referer"],
        user_agent=m["ua"],
    )


def parse_file(path: Path, *, skip_invalid: bool = True) -> Iterator[LogEntry]:
    """Lit un fichier ligne par ligne. Lazy.

    Si skip_invalid=True, log un warning et saute ; sinon remonte ParseError.
    """
    with path.open(encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                yield parse_line(line)
            except ParseError:
                if skip_invalid:
                    logger.warning("ligne %d ignorée dans %s", n, path)
                    continue
                raise
