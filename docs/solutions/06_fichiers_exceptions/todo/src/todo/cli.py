"""Point d'entrée CLI."""
import argparse
import logging
import sys

from .errors import AppError, InvalidTaskError, TaskNotFoundError
from .models import Task
from . import storage

logger = logging.getLogger(__name__)


def _configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def cmd_add(titre: str, priorite: str, tags: list[str]) -> None:
    if not titre.strip():
        raise InvalidTaskError("le titre ne peut pas être vide")
    tasks = storage.load()
    task = Task(id=storage.next_id(tasks), titre=titre.strip(), priorite=priorite, tags=tags)
    tasks.append(task)
    storage.save(tasks)
    print(f"Tâche #{task.id} ajoutée.")


def cmd_list(tag: str | None, actives_seulement: bool) -> None:
    tasks = storage.load()
    if actives_seulement:
        tasks = [t for t in tasks if not t.terminee]
    if tag is not None:
        tasks = [t for t in tasks if tag in t.tags]

    if not tasks:
        print("(aucune tâche)")
        return

    for t in tasks:
        check = "[x]" if t.terminee else "[ ]"
        tags_str = f" #{' #'.join(t.tags)}" if t.tags else ""
        print(f"{check} {t.id:>3}. ({t.priorite}) {t.titre}{tags_str}")


def cmd_done(task_id: int) -> None:
    tasks = storage.load()
    for t in tasks:
        if t.id == task_id:
            t.terminee = True
            storage.save(tasks)
            print(f"Tâche #{task_id} marquée terminée.")
            return
    raise TaskNotFoundError(f"tâche {task_id} introuvable")


def cmd_remove(task_id: int) -> None:
    tasks = storage.load()
    restantes = [t for t in tasks if t.id != task_id]
    if len(restantes) == len(tasks):
        raise TaskNotFoundError(f"tâche {task_id} introuvable")
    storage.save(restantes)
    print(f"Tâche #{task_id} supprimée.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="todo", description="Gestionnaire de tâches.")
    parser.add_argument("-v", "--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Ajouter une tâche")
    add.add_argument("titre")
    add.add_argument("--priorite", choices=["bas", "moyen", "haut"], default="moyen")
    add.add_argument("--tag", action="append", default=[], dest="tags")

    ls = sub.add_parser("list", help="Lister les tâches")
    ls.add_argument("--tag", default=None)
    ls.add_argument("--actives", action="store_true")

    done = sub.add_parser("done", help="Marquer une tâche terminée")
    done.add_argument("id", type=int)

    rm = sub.add_parser("remove", help="Supprimer une tâche")
    rm.add_argument("id", type=int)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    _configure_logging(args.verbose)

    try:
        match args.command:
            case "add":
                cmd_add(args.titre, args.priorite, args.tags)
            case "list":
                cmd_list(args.tag, args.actives)
            case "done":
                cmd_done(args.id)
            case "remove":
                cmd_remove(args.id)
    except AppError as e:
        print(f"Erreur : {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
