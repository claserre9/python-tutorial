"""Point d'entrée CLI."""
import argparse
import logging
import sys

from .errors import AppError, InvalidTaskError, TaskNotFoundError
from .models import Task
from . import storage

logger = logging.getLogger(__name__)


def _configure_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def cmd_add(titre: str, priorite: str, tags: list[str]) -> None:
    # TODO :
    # - valider titre non vide -> sinon raise InvalidTaskError
    # - charger les tâches
    # - créer une Task avec next_id
    # - sauver
    # - print un message utilisateur sur stdout ("Tâche #N ajoutée.")
    ...


def cmd_list(tag: str | None, actives_seulement: bool) -> None:
    # TODO : filtrer et afficher proprement
    ...


def cmd_done(task_id: int) -> None:
    # TODO : trouver la tâche, marquer terminee=True, sauver
    # si pas trouvée -> raise TaskNotFoundError(f"tâche {task_id} introuvable")
    ...


def cmd_remove(task_id: int) -> None:
    # TODO : retirer la tâche, sauver
    ...


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
