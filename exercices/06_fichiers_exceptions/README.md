# Exercices — Chapitre 6

Deux parties : exercices ciblés (`exercices.py`) puis le **projet fil rouge** CLI `todo/`.

## Partie A — Exercices ciblés

Voir `exercices.py`.

## Partie B — Projet fil rouge : CLI `todo`

Le squelette se trouve dans le dossier `todo/`. Vous devez compléter les `TODO` pour obtenir une CLI fonctionnelle.

### Fonctionnalités à livrer

- `todo add "Titre" [--priorite bas|moyen|haut] [--tag T]`
- `todo list [--tag T] [--actives]`
- `todo done <id>`
- `todo remove <id>`

### Contraintes

1. Les tâches sont stockées en JSON dans `~/.todo.json` (utiliser `pathlib` et `Path.home()`).
2. Utiliser `logging` (pas `print`) pour les traces internes.
3. Définir au minimum les exceptions custom : `TaskNotFoundError`, `InvalidTaskError`.
4. En cas d'erreur attendue, afficher un message clair sur **stderr** et sortir avec un code non nul. **Jamais** de trace Python pour l'utilisateur final.
5. Installable via `uv pip install -e .` (ou `pip install -e .`), expose la commande `todo`.

### Installation et test

```bash
cd exercices/06_fichiers_exceptions/todo
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

todo add "Apprendre Python" --priorite haut --tag perso
todo list
todo done 1
todo remove 1
```

### Tests

```bash
pytest
```

Le corrigé (fonctionnel, avec tests) est dans `solutions/06_fichiers_exceptions/todo/`. Ne regardez qu'**après** avoir tenté.
