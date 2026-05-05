# Chapitre 6 — I/O, exceptions, logging

Trois sujets indissociables d'un programme robuste : lire/écrire des fichiers proprement (avec `pathlib`), gérer les erreurs sans s'arrêter brutalement, et journaliser avec `logging` plutôt qu'avec `print`. Ce chapitre se termine par le **projet fil rouge du Niveau 1** : une CLI de gestion de tâches.

## 1. `pathlib` — finies les strings

Oubliez `os.path.join`, `os.makedirs`, `os.path.exists`. Depuis Python 3.4, `pathlib` encapsule tout ça dans un objet `Path` manipulable.

```python
from pathlib import Path

p = Path("data") / "users.json"     # composition
p.parent                            # Path('data')
p.name                              # 'users.json'
p.stem                              # 'users'
p.suffix                            # '.json'
p.suffixes                          # ['.json']
p.exists()                          # False
p.is_file()                         # False
p.is_dir()                          # False
```

### Création, lecture, écriture

```python
p = Path("notes.txt")

# Écriture (crée ou écrase)
p.write_text("première ligne\nseconde", encoding="utf-8")

# Lecture
contenu = p.read_text(encoding="utf-8")

# Pour du binaire
p.write_bytes(b"\x00\x01\x02")
data = p.read_bytes()
```

### Parcours de dossiers

```python
dossier = Path("mon_projet")

# Tous les .py récursivement
for fichier in dossier.rglob("*.py"):
    print(fichier)

# Niveau unique
for fichier in dossier.glob("*.py"):
    ...

# Créer un dossier (avec les parents, silencieux si existe)
Path("data/exports/2026").mkdir(parents=True, exist_ok=True)
```

### Opérations fichiers

```python
p.rename("nouveau_nom.txt")
p.unlink()                    # supprime (comme rm)
p.unlink(missing_ok=True)     # silencieux si absent
```

## 2. `open()` et le bloc `with`

Pour lire/écrire un fichier "à la main" (plus de contrôle que `read_text`) :

```python
with open("log.txt", "r", encoding="utf-8") as f:
    for ligne in f:              # lit ligne par ligne (lazy)
        print(ligne.rstrip())
```

### Modes d'ouverture

| Mode | Effet |
|---|---|
| `"r"` | lecture (défaut) |
| `"w"` | écriture, **écrase** si existe |
| `"a"` | append (ajoute à la fin) |
| `"x"` | écriture, **échoue** si existe |
| `"b"` | binaire (à combiner : `"rb"`, `"wb"`) |
| `"+"` | lecture **et** écriture |

### Toujours spécifier `encoding`

```python
open("f.txt", "r", encoding="utf-8")   # ✅
open("f.txt", "r")                     # ❌ dépend de l'OS (UTF-8 sur Linux/macOS, cp1252 sur Windows)
```

Python 3.15 rendra `utf-8` le défaut universel (PEP 686). En attendant : explicitez.

### Pourquoi le `with`

Le `with` garantit la **fermeture** du fichier même en cas d'exception. Équivalent à :

```python
f = open("log.txt")
try:
    ...
finally:
    f.close()
```

Tout objet qui implémente `__enter__` et `__exit__` peut être utilisé avec `with` (voir Ch. 9 pour les écrire).

## 3. JSON : sérialisation standard

```python
import json

data = {"nom": "Alice", "tags": ["python", "web"]}

# Sérialiser en string
s = json.dumps(data, indent=2, ensure_ascii=False)

# Sérialiser directement dans un fichier
Path("user.json").write_text(json.dumps(data, indent=2), encoding="utf-8")

# Parser
obj = json.loads(s)

# Depuis un fichier
obj = json.loads(Path("user.json").read_text(encoding="utf-8"))
```

**`ensure_ascii=False`** : garde les caractères Unicode lisibles (`"é"` au lieu de `"é"`).

### Limites de `json`

- Pas de `datetime`, `set`, `Decimal`, `Path` : il faut un converter.
- Pour un format plus riche : `pickle` (Python only, insécurisé pour du data externe), ou des lib comme `pydantic` (Ch. 15).

## 4. Exceptions : gérer les erreurs

### Syntaxe

```python
try:
    risque()
except ValueError:
    print("valeur invalide")
except (IOError, OSError) as e:
    print(f"problème d'I/O : {e}")
except Exception as e:
    print(f"erreur inconnue : {e}")
else:
    print("aucune exception")     # exécuté si PAS d'exception
finally:
    cleanup()                      # toujours exécuté
```

### Hiérarchie (simplifiée)

```
BaseException
 ├── SystemExit           (sys.exit)
 ├── KeyboardInterrupt    (Ctrl+C)
 └── Exception            ← on attrape à partir d'ici
      ├── ArithmeticError
      │    └── ZeroDivisionError
      ├── LookupError
      │    ├── IndexError
      │    └── KeyError
      ├── ValueError
      ├── TypeError
      ├── OSError
      │    ├── FileNotFoundError
      │    ├── PermissionError
      │    └── TimeoutError
      └── ...
```

**Règle** : attrapez le type **le plus spécifique possible**. Attraper `Exception` masque des bugs.

### Règles d'or

```python
# ❌ NE JAMAIS faire
try:
    risque()
except:            # attrape tout, y compris KeyboardInterrupt et SystemExit
    pass

# ❌ MAUVAIS
try:
    risque()
except Exception:
    pass           # échec silencieux

# ✅ BON
try:
    risque()
except ValueError as e:
    logger.warning(f"valeur invalide: {e}")
    return defaut
```

### Lever une exception

```python
if age < 0:
    raise ValueError(f"âge invalide: {age}")
```

### Chaînage d'exceptions

Quand vous re-levez une exception dans un `except`, Python garde le contexte (`__context__`). Pour **expliciter** la cause :

```python
try:
    config = json.loads(Path("config.json").read_text())
except json.JSONDecodeError as e:
    raise ConfigError("config.json invalide") from e
```

Le `from e` donne une trace claire : "ConfigError a été causée par JSONDecodeError". Pour **masquer** la cause : `raise X() from None`.

### Exceptions custom

```python
class ConfigError(Exception):
    """Erreur de configuration applicative."""

class ValidationError(Exception):
    def __init__(self, field: str, message: str):
        super().__init__(f"{field}: {message}")
        self.field = field
```

Bonnes pratiques :
- Nom en `...Error`.
- Héritez de `Exception`, pas de `BaseException`.
- Créez une classe racine par domaine (`class AppError(Exception): ...`) pour permettre `except AppError:` global.

### `try/except/else`

```python
try:
    valeur = int(s)
except ValueError:
    print("pas un nombre")
else:
    # exécuté seulement si PAS d'exception
    # séparer le code "post-traitement" évite d'attraper des exceptions inattendues
    utiliser(valeur)
```

## 5. `logging` — pourquoi pas `print`

`print` envoie sur stdout. Pas de niveau, pas de fichier de log, pas de format, pas de filtrage. Inexploitable en production.

`logging` vous donne :
- Des **niveaux** : DEBUG, INFO, WARNING, ERROR, CRITICAL.
- Des **handlers** : console, fichier, rotation, syslog, réseau, etc.
- Un **format** configurable (timestamp, module, pid, ...).
- Une **configuration centralisée** (pas éparpillée en `print`).

### Utilisation basique

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

logger.debug("détail interne")       # invisible avec level=INFO
logger.info("démarrage")
logger.warning("fichier absent, utilisation du défaut")
logger.error("échec de la requête")
logger.exception("échec critique")   # inclut la stack trace courante
```

### Pattern recommandé par module

```python
# mon_module.py
import logging

logger = logging.getLogger(__name__)   # hérite de la config parente

def traiter():
    logger.info("traitement démarré")
```

Dans l'application principale, configurez une seule fois :

```python
# main.py
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
```

### `logger.exception`

Dans un bloc `except`, préférez `logger.exception("contexte")` à `logger.error(str(e))`. `exception` ajoute la stack trace automatiquement.

```python
try:
    traiter()
except Exception:
    logger.exception("échec du traitement")
    raise
```

## 6. `argparse` — CLI propre

Pour exposer votre programme en ligne de commande :

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="Gestionnaire de tâches.")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="Ajouter une tâche")
    add.add_argument("titre", help="Le titre de la tâche")
    add.add_argument("--priorite", choices=["bas", "moyen", "haut"], default="moyen")

    list_cmd = sub.add_parser("list", help="Lister les tâches")
    list_cmd.add_argument("--tous", action="store_true")

    args = parser.parse_args()

    match args.command:
        case "add":
            ajouter(args.titre, args.priorite)
        case "list":
            lister(inclure_termines=args.tous)


if __name__ == "__main__":
    main()
```

`argparse` génère `-h`/`--help` automatiquement.

---

## 7. Projet fil rouge — CLI de gestion de tâches

### Cahier des charges

Une CLI `todo` qui :

- `todo add "Titre" [--priorite P] [--tag T]` : ajoute une tâche
- `todo list [--tag T] [--actives]` : liste les tâches (filtrable)
- `todo done <id>` : marque comme terminée
- `todo remove <id>` : supprime

Les données sont persistées dans `~/.todo.json`. Le programme doit :

- Utiliser `pathlib` pour le fichier.
- Utiliser `logging` (pas `print` pour les logs).
- Lever des exceptions custom (`TaskNotFoundError`, `InvalidTaskError`) attrapées proprement au niveau de la CLI.
- Afficher un message utilisateur clair en cas d'erreur, **sans trace Python**.
- Être un paquet installable (`pip install -e .`) avec point d'entrée `todo`.

### Architecture suggérée

```
todo/
├── pyproject.toml
├── src/
│   └── todo/
│       ├── __init__.py
│       ├── cli.py          # argparse, handlers par sous-commande
│       ├── storage.py      # load/save JSON, Path
│       ├── models.py       # dataclass Task
│       └── errors.py       # exceptions custom
└── tests/
    └── test_storage.py
```

Un squelette est fourni dans `exercices/06_fichiers_exceptions/`. La solution complète est dans `solutions/06_fichiers_exceptions/`.

Ce projet consolide **tout** le Niveau 1 : types, fonctions, structures de données, I/O, exceptions, logging, modules, CLI.

---

### Piège courant : `open` sans encoding

```python
with open("data.txt") as f:              # ❌
    ...
```

Sur Windows, ça ouvre en cp1252 par défaut. Vos accents/emojis cassent. **Toujours** spécifier `encoding="utf-8"` (sauf cas exotique).

---

### Piège courant : attraper `Exception`

```python
try:
    risque()
except Exception:     # attrape ValueError, KeyError, ConnectionError, ...
    print("oups")
```

Vous masquez des bugs de programmation (typos, AttributeError) qui devraient remonter en crash et être corrigés. Attrapez ce que vous savez gérer.

---

### Sous le capot : exceptions et performance

Lever une exception en Python est **coûteux** (trace à construire). Ne pas en abuser pour du contrôle de flux. Exception légitime : `StopIteration` qui termine les générateurs (Ch. 9).

La règle historique "EAFP" (Easier to Ask Forgiveness than Permission) reste vraie :

```python
# Pythonique (EAFP)
try:
    valeur = d[cle]
except KeyError:
    valeur = defaut

# Moins pythonique (LBYL = Look Before You Leap)
if cle in d:
    valeur = d[cle]
else:
    valeur = defaut
```

En pratique, `d.get(cle, defaut)` est encore mieux pour ce cas précis.

---

## À retenir

- `pathlib` partout, `os.path` plus jamais.
- `open(..., encoding="utf-8")`, toujours.
- `with` pour la gestion des ressources.
- Attrapez des exceptions **spécifiques**, jamais `Exception:` ou `except:` nu.
- `raise ... from e` pour chaîner proprement.
- `logging` pour les logs, `print` pour parler à l'utilisateur final.
- `argparse` pour exposer une CLI digne.

---

➡️ [Chapitre 7 — POO : bases solides](../07_poo_bases/README.md)
