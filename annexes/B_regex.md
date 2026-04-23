# Annexe B — Regex en Python

Le module `re` est **toujours** en stdlib, très utile pour parser des logs, valider des formats, extraire des champs. Ses pièges méritent une annexe dédiée.

## 1. Fonctions principales

```python
import re

re.match(pattern, string)          # match au DÉBUT seulement
re.search(pattern, string)         # match n'importe où, 1ère occurrence
re.findall(pattern, string)        # toutes les occurrences → list
re.finditer(pattern, string)       # idem mais itérateur de match objects
re.sub(pattern, repl, string)      # remplace
re.split(pattern, string)          # split par pattern
```

## 2. Compiler pour réutilisation

```python
EMAIL_RE = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")

EMAIL_RE.findall(texte)            # plus rapide qu'appeler re.findall à chaque fois
```

Préférez **compiler** en constante de module si la regex est utilisée plusieurs fois.

## 3. `raw strings` obligatoires

```python
re.match("\d+", s)            # ❌ \d devient une séquence d'échappement, warning
re.match(r"\d+", s)           # ✅ r"..." : string raw, pas d'interprétation
```

**Toujours** préfixer les patterns avec `r`.

## 4. Métacaractères essentiels

| | Signification |
|---|---|
| `.` | n'importe quel caractère sauf `\n` (sans flag `re.DOTALL`) |
| `^` | début de string (ou de ligne avec `re.MULTILINE`) |
| `$` | fin de string (ou de ligne) |
| `\d`, `\D` | chiffre / non-chiffre |
| `\w`, `\W` | mot (alphanum+underscore) / non-mot |
| `\s`, `\S` | espace / non-espace |
| `\b` | frontière de mot |
| `[abc]` | un char parmi a, b, c |
| `[^abc]` | un char sauf a, b, c |
| `[a-z]` | plage |
| `a|b` | a OU b |
| `()` | groupe (capture) |
| `(?:...)` | groupe non capturant |
| `(?P<nom>...)` | groupe nommé |
| `?` | 0 ou 1 |
| `*` | 0 ou plus |
| `+` | 1 ou plus |
| `{n}` | exactement n |
| `{n,m}` | entre n et m |
| `*?`, `+?`, `??` | versions **non-greedy** (le moins possible) |

## 5. Greedy vs non-greedy

Par défaut `*` et `+` sont **greedy** : ils matchent le plus possible.

```python
re.search(r"<.+>", "<a> et <b>").group()      # '<a> et <b>'   ← greedy
re.search(r"<.+?>", "<a> et <b>").group()     # '<a>'          ← non-greedy
```

Règle mentale : `+?` = "le moins possible".

## 6. Groupes

```python
m = re.search(r"(\d{4})-(\d{2})-(\d{2})", "né le 1990-03-15")
m.group(0)        # '1990-03-15' (tout le match)
m.group(1)        # '1990'
m.group(2)        # '03'
m.groups()        # ('1990', '03', '15')

# Groupes nommés
m = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})", s)
m["year"]         # '1990'
m.groupdict()     # {'year': '1990', 'month': '03', 'day': '15'}
```

## 7. Substitution

```python
re.sub(r"\s+", " ", texte)                    # normalise les espaces
re.sub(r"(\w+)@", r"[\1]@", "a@b.com")        # '[a]@b.com'  — \1 = groupe 1
re.sub(r"(\d+)", lambda m: str(int(m[1]) * 2), "abc 5 xyz 10")   # 'abc 10 xyz 20'
```

## 8. Flags utiles

```python
re.match(r"python", "PYTHON", re.IGNORECASE)              # insensible à la casse
re.findall(r"^> .+$", texte, re.MULTILINE)                 # ^/$ par ligne
re.search(r"<.+>", texte, re.DOTALL)                        # . inclut \n
re.search(r"""
    (\d{3})      # préfixe
    -
    (\d{4})      # numéro
""", s, re.VERBOSE)                                         # regex commentée
```

On peut combiner avec `|` : `re.IGNORECASE | re.MULTILINE`.

## 9. Pièges

### Oublier d'échapper

```python
re.match(r"3.14", "3a14")        # ✅ matche ! car . = n'importe quoi
re.match(r"3\.14", "3a14")       # ❌ ne matche pas
```

Pour échapper un littéral dynamique :

```python
pattern = re.escape(user_input)      # échappe . * + etc.
```

### Regex infiniment exponentielle (**ReDoS**)

Certaines regex peuvent prendre des minutes sur des inputs crafted, bloquant votre app.

```python
re.match(r"(a+)+$", "a" * 30 + "!")        # ⚠️ très très lent
```

**Attention** aux regex issues d'inputs utilisateur. Pour valider des formats connus, préférez des parsers dédiés (email : `email-validator` ; URL : `urllib.parse`).

### `match` vs `search`

`re.match()` matche seulement **au début** de la string. Pour chercher n'importe où, `search()`. Confusion fréquente.

```python
re.match(r"python", "learn python")       # None !
re.search(r"python", "learn python")      # Match
```

## 10. Alternatives à regex

- **`str.startswith`, `.endswith`, `.split`, `in`, `find`** : pour des cas simples, plus lisibles.
- **`fnmatch`** : globs (`*.py`, `file?.txt`).
- **`pyparsing`** : pour de la vraie grammaire.
- Un vrai **parser** (JSON, XML, CSV) : **`json`**, **`csv`**, **`lxml`**.

Règle : **si votre regex dépasse 50 caractères ou 3 groupes, reconsidérez**. Un parser dédié ou une suite d'opérations simples est souvent plus maintenable.

## 11. Exemples pratiques

```python
# Extraction de chiffres dans un texte
re.findall(r"\d+", "paye 20€ le 3 avril")     # ['20', '3']

# Validation (basique) d'email
re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", "a@b.com")

# Parser un log ligne
PATTERN = re.compile(
    r"^(?P<ip>\S+) - - \[(?P<ts>[^\]]+)\] "
    r'"(?P<method>\S+) (?P<path>\S+) \S+" '
    r"(?P<status>\d+)"
)
m = PATTERN.match(ligne)
if m:
    entry = m.groupdict()

# Normaliser des espaces
re.sub(r"\s+", " ", texte).strip()
```

## Test interactif

`https://regex101.com/` (avec flavor Python) est indispensable pour construire des regex non triviales.
