"""Persistence JSON des tâches."""
import json
import logging
from pathlib import Path

from .errors import StorageError
from .models import Task

logger = logging.getLogger(__name__)

DEFAULT_STORAGE = Path.home() / ".todo.json"


def load(path: Path = DEFAULT_STORAGE) -> list[Task]:
    """Charge la liste des tâches. Retourne [] si le fichier n'existe pas."""
    # TODO :
    # - si path n'existe pas -> []
    # - lire en utf-8
    # - parser JSON (list de dicts) -> list[Task] via Task.from_dict
    # - en cas de JSONDecodeError : raise StorageError(...) from e
    ...


def save(tasks: list[Task], path: Path = DEFAULT_STORAGE) -> None:
    """Écrit la liste des tâches en JSON (indenté, utf-8)."""
    # TODO :
    # - sérialiser chaque Task via .to_dict()
    # - path.write_text(json.dumps(..., indent=2, ensure_ascii=False), encoding="utf-8")
    ...


def next_id(tasks: list[Task]) -> int:
    """Retourne le prochain ID disponible (max + 1, ou 1 si vide)."""
    # TODO
    ...
