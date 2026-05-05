# Exercices — Chapitre 1

Ces exercices portent sur la **configuration** plus que sur le code. L'objectif est qu'à la fin, vous ayez un projet propre dans lequel rédiger la suite du tutoriel.

## Exercice 1.1 — Diagnostic d'installation

À faire dans un terminal, puis notez les réponses dans un fichier `diagnostic.md` à la racine du projet.

1. Quelle version retourne `python --version` ? Et `python3 --version` ?
2. Que donne `which python` (macOS/Linux) ou `where python` (Windows) ?
3. Que retourne `python -c "import sys; print(sys.executable)"` ?
4. Votre interpréteur actuel est-il celui du système, ou un autre ? Comment le savez-vous ?

## Exercice 1.2 — Créer un environnement virtuel

1. Créez un dossier `playground/` à l'écart du tutoriel.
2. Dans ce dossier, créez un `.venv` avec la méthode de votre choix (`uv`, `venv`).
3. Activez-le.
4. Prouvez qu'il est actif : `which python` doit pointer **dans** `.venv`.
5. Installez `requests` dedans.
6. Désactivez-le. Vérifiez que `python -c "import requests"` **échoue** hors du venv (si `requests` n'est pas installé globalement).

## Exercice 1.3 — `pyproject.toml` minimal

Dans `playground/`, créez un `pyproject.toml` qui :

- Déclare un projet nommé `playground`, version `0.1.0`
- Exige Python >= 3.12
- Dépend de `requests >= 2.31`
- Déclare `pytest` et `ruff` en dépendances de dev (`optional-dependencies`)

Puis installez votre propre projet en mode éditable :

```bash
uv pip install -e ".[dev]"
```

Vérifiez que `python -c "import requests"` fonctionne et que `pytest --version` est dispo.

## Exercice 1.4 — `python -m` vs `python script.py`

1. Créez un fichier `hello.py` qui contient simplement `print("hello")`.
2. Exécutez-le avec `python hello.py`. Ça marche.
3. Maintenant exécutez `python -m hello` (sans le `.py`). Expliquez la différence de comportement.
4. Lancez `python -m http.server 8000` dans un dossier et ouvrez `http://localhost:8000` dans votre navigateur. Qu'affiche-t-il ?

## Exercice 1.5 — Le bug classique

Simulons le bug "wrong Python" pour ne plus jamais y tomber.

1. Dans un shell **sans venv activé**, faites : `pip install cowsay`
2. Puis : `python -c "import cowsay"` — ça peut échouer. Pourquoi ?
3. Utilisez `python -m pip install cowsay` pour garantir que le `pip` utilisé est bien celui de `python`.
4. Retestez l'import.

Si tout "marche" dès le départ chez vous, c'est que `pip` et `python` sont cohérents — mais comprenez pourquoi ce n'est pas toujours le cas.

---

Les solutions sont dans `solutions/01_intro_installation/`.
