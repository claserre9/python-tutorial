from pathlib import Path

import pytest

from todo.errors import StorageError
from todo.models import Task
from todo import storage


def test_load_absent(tmp_path: Path) -> None:
    assert storage.load(tmp_path / "rien.json") == []


def test_save_then_load(tmp_path: Path) -> None:
    p = tmp_path / "t.json"
    tasks = [
        Task(id=1, titre="A", tags=["x"]),
        Task(id=2, titre="B", priorite="haut", terminee=True),
    ]
    storage.save(tasks, p)
    loaded = storage.load(p)
    assert loaded == tasks


def test_next_id_vide() -> None:
    assert storage.next_id([]) == 1


def test_next_id_max() -> None:
    tasks = [Task(id=3, titre="a"), Task(id=7, titre="b"), Task(id=5, titre="c")]
    assert storage.next_id(tasks) == 8


def test_load_corrompu(tmp_path: Path) -> None:
    p = tmp_path / "bad.json"
    p.write_text("{pas du json", encoding="utf-8")
    with pytest.raises(StorageError):
        storage.load(p)
