"""Génère le dossier `docs/` consommé par MkDocs depuis les sources (`cours/`, `annexes/`, README).

Le dossier `docs/` est volontairement gitignoré : unique source de vérité = les fichiers originaux.
"""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


def main() -> None:
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir()

    # Accueil
    shutil.copy(ROOT / "README.md", DOCS / "index.md")

    # Chapitres
    for chapter in sorted((ROOT / "cours").iterdir()):
        source = chapter / "README.md"
        if not source.exists():
            continue
        dest = DOCS / "cours" / chapter.name / "README.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(source, dest)

    # Annexes
    for annexe in sorted((ROOT / "annexes").glob("*.md")):
        if annexe.name == "README.md":
            continue
        dest = DOCS / "annexes" / annexe.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(annexe, dest)

    print(f"docs/ généré depuis {ROOT}")


if __name__ == "__main__":
    main()
