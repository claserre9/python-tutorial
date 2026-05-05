# Annexe A — Debug

`print` partout est un antipattern. Un vrai debugger est plus rapide dès que le bug n'est pas trivial.

## 1. `breakpoint()` — built-in depuis 3.7

```python
def ma_fonction(x):
    result = calcul(x)
    breakpoint()           # stoppe ici, ouvre pdb
    return result * 2
```

Au `breakpoint()`, le programme s'arrête, vous êtes dans un REPL pdb interactif :

| Commande | Effet |
|---|---|
| `n` (next) | ligne suivante, sans descendre dans les appels |
| `s` (step) | descend dans l'appel suivant |
| `c` (continue) | reprend l'exécution |
| `l` (list) | affiche les 11 lignes autour du point courant |
| `ll` (long list) | toute la fonction |
| `p expr` | évalue et affiche |
| `pp expr` | pretty-print |
| `w` (where) | stack trace |
| `u`, `d` | remonte/descend dans la pile |
| `b N` | breakpoint ligne N |
| `q` (quit) | quitter |
| `h` (help) | aide |

Vous pouvez aussi exécuter n'importe quel code Python : `p user.__dict__`, `p [x for x in items if x.active]`, etc.

## 2. Désactiver `breakpoint()` globalement

Variable d'env :

```bash
PYTHONBREAKPOINT=0 python mon_script.py       # ignore tous les breakpoints
```

Ou pointer vers un autre debugger :

```bash
PYTHONBREAKPOINT=ipdb.set_trace python mon_script.py
```

## 3. `ipdb` — pdb enrichi

```bash
uv pip install ipdb
```

Remplace pdb avec coloration syntaxique, complétion, `??` pour voir le source.

## 4. Post-mortem

Si votre programme a planté avec une exception, `pdb.pm()` démarre pdb sur la frame de l'exception :

```bash
python -m pdb mon_script.py
# ... script plante ...
(Pdb) pm    # post-mortem sur la dernière exception
```

Ou dans le code :

```python
try:
    risque()
except Exception:
    import pdb; pdb.post_mortem()
```

## 5. Debuggers IDE

### PyCharm

- **Points d'arrêt** : clic dans la marge.
- Lancez avec le bouton "Debug" (bug avec punaise).
- Panneau **Debug** : frames, variables, console, évaluer expression.
- **Évaluer / Modifier** : `Alt+F8` pour tester une expression dans le contexte courant.
- **Breakpoints conditionnels** : clic droit sur un breakpoint → condition `x > 100`.

### VS Code

Créer `.vscode/launch.json` :

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Fichier courant",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    }
  ]
}
```

Puis F5 pour lancer. Breakpoints dans la marge.

## 6. Astuces

### `traceback.print_exc()`

```python
import traceback

try:
    risque()
except Exception:
    traceback.print_exc()       # log la trace sans crasher
```

### `pprint.pprint`

```python
from pprint import pprint
pprint(structure_complexe)      # indentation lisible
```

### `dis` pour comprendre le bytecode

```python
import dis
dis.dis(ma_fonction)            # affiche le bytecode
```

Utile pour des questions de performance ou comprendre un comportement surprenant.

### `logging` au niveau DEBUG

Les messages `logger.debug(...)` sont silencieux par défaut. Temporairement, passez le niveau à `DEBUG` pour les voir :

```python
logging.getLogger().setLevel(logging.DEBUG)
```

Plus systématique qu'ajouter/retirer des `print`.

## 7. Bugs async — traces qui sortent du contexte

Dans `asyncio`, une exception dans une task non awaited peut disparaître silencieusement (sauf warning). Toujours :

```python
task = asyncio.create_task(ma_coro())
# ... plus tard
await task             # OU gérer l'exception
```

Ou utiliser `TaskGroup` (Ch. 12) qui gère ça proprement.

## Règle de travail

1. Reproduire le bug (test qui échoue = idéal).
2. Poser un `breakpoint()` **au point de symptôme**.
3. Remonter la stack (`u`) jusqu'à trouver la cause.
4. Fixer, puis écrire un test de non-régression.
