"""TODO : parser de logs Nginx format combined.

Implémentez :
- class ParseError(ValueError)
- parse_line(line: str) -> LogEntry
- parse_file(path: Path, *, skip_invalid: bool = True) -> Iterator[LogEntry]  (lazy, générateur)

Utilisez une regex pour matcher le format combined :
  IP - - [DATE] "METHOD PATH HTTP/VER" STATUS SIZE "REFERER" "UA"

Format timestamp : %d/%b/%Y:%H:%M:%S %z

Si size = "-", le convertir en 0.
"""
