"""Persistence JSON des tâches."""
import json
import logging
from pathlib import Path

from .errors import StorageError
from .models import Task

logger = logging.getLogger(__name__)

DEFAULT_STORAGE = Path.home() / ".todo.json"


def load(path: Path = DEFAULT_STORAGE) -> list[Task]:
    if not path.exists():
        logger.debug("fichier %s absent, retour liste vide", path)
        return []
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise StorageError(f"{path} corrompu") from e
    return [Task.from_dict(d) for d in raw]


def save(tasks: list[Task], path: Path = DEFAULT_STORAGE) -> None:
    data = [t.to_dict() for t in tasks]
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    logger.debug("%d tâches sauvegardées dans %s", len(tasks), path)


def next_id(tasks: list[Task]) -> int:
    return max((t.id for t in tasks), default=0) + 1
