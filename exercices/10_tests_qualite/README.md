# Exercices — Chapitre 10

## Partie A — Exercices ciblés (typage)

Voir `exercices.py`.

## Partie B — Projet fil rouge : parseur de logs

Dossier `logparser/`. Objectif : une lib de parsing de logs Nginx **entièrement typée** et **testée**.

### Contraintes

- `mypy --strict` doit passer
- Couverture pytest ≥ 80%
- `ruff check` et `ruff format --check` clean
- Pipeline interne basé sur des générateurs (lazy)

### Structure

Voir le cours. Squelettes pré-remplis dans `logparser/src/logparser/`.

### Installation & vérification

```bash
cd exercices/10_tests_qualite/logparser
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

pytest
mypy src/
ruff check .
```

### Fonctionnalités à livrer

1. `LogEntry` : dataclass frozen avec `ip`, `timestamp`, `method`, `path`, `status`, `size`, `referer`, `user_agent`.
2. `parse_line(line: str) -> LogEntry` — lève `ParseError` si invalide.
3. `parse_file(path: Path, *, skip_invalid: bool = True) -> Iterator[LogEntry]` — générateur, lazy.
4. Module `analytics` : `top_ips`, `status_counts`, `erreurs_5xx`, `volume_par_heure`.
5. `__main__.py` pour lancer en CLI : `python -m logparser access.log --top 10`.

Corrigé complet dans `solutions/10_tests_qualite/logparser/`.
