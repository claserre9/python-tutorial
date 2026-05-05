from collections import Counter, defaultdict
from collections.abc import Iterable

from .models import LogEntry


def top_ips(entries: Iterable[LogEntry], n: int = 10) -> list[tuple[str, int]]:
    return Counter(e.ip for e in entries).most_common(n)


def status_counts(entries: Iterable[LogEntry]) -> dict[int, int]:
    return dict(Counter(e.status for e in entries))


def erreurs_5xx(entries: Iterable[LogEntry]) -> Iterable[LogEntry]:
    return (e for e in entries if 500 <= e.status < 600)


def volume_par_heure(entries: Iterable[LogEntry]) -> dict[int, int]:
    """Nombre de requêtes par heure (0-23, tous jours confondus)."""
    par_heure: dict[int, int] = defaultdict(int)
    for e in entries:
        par_heure[e.timestamp.hour] += 1
    return dict(par_heure)
