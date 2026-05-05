"""
Exercices — Chapitre 6 : I/O, exceptions, logging
"""
import json
import logging
from pathlib import Path


# =============================================================================
# 6.1 — pathlib
# =============================================================================
# Soit le chemin ci-dessous. Sans exécuter, prédisez le résultat de chaque
# attribut, puis vérifiez.

p = Path("/Users/alice/projets/monapp/src/utils.py")

# p.parent   -> ?
# p.name     -> ?
# p.stem     -> ?
# p.suffix   -> ?
# p.parts    -> ? (tuple)


# =============================================================================
# 6.2 — Lecture sûre avec fallback
# =============================================================================
# Écrivez `lire_config(chemin)` qui :
#  - retourne le dict JSON si le fichier existe et est valide
#  - retourne {} si le fichier n'existe pas
#  - LÈVE une ValueError si le fichier existe mais est invalide (chaînée avec from)

def lire_config(chemin: Path) -> dict:
    ...  # TODO


# Test : fichier absent
assert lire_config(Path("/tmp/inexistant_" + str(id({})) + ".json")) == {}

# Test : fichier valide
ok = Path("/tmp/ok.json")
ok.write_text('{"port": 8000}', encoding="utf-8")
assert lire_config(ok) == {"port": 8000}
ok.unlink()

# Test : fichier invalide
ko = Path("/tmp/ko.json")
ko.write_text("{pas du json", encoding="utf-8")
try:
    lire_config(ko)
except ValueError as e:
    assert e.__cause__ is not None, "utilisez `raise ... from e` pour chaîner"
finally:
    ko.unlink()


# =============================================================================
# 6.3 — Exception custom
# =============================================================================
# Définissez une hiérarchie d'exceptions :
# - AppError (racine)
# - ConfigError (hérite d'AppError)
# - ValidationError (hérite d'AppError) avec un attribut `field` et `message`

class AppError(Exception):
    ...  # TODO


class ConfigError(AppError):
    ...  # TODO


class ValidationError(AppError):
    # TODO : accepter field et message, appeler super().__init__
    ...


# Tests
try:
    raise ConfigError("fichier invalide")
except AppError as e:       # doit être attrapé par AppError
    assert str(e) == "fichier invalide"

try:
    raise ValidationError("email", "format invalide")
except ValidationError as e:
    assert e.field == "email"
    assert e.message == "format invalide"


# =============================================================================
# 6.4 — Logger configuré
# =============================================================================
# Configurez le logging pour :
#  - niveau INFO
#  - format : "YYYY-MM-DD HH:MM:SS | LEVEL | name | message"
#  - écrire à la fois sur stderr ET dans /tmp/test_logging.log
# Puis écrivez 3 messages (info, warning, error) et vérifiez que le fichier
# contient bien les 3.

# TODO : configurer logging.basicConfig(...)

log_path = Path("/tmp/test_logging.log")
if log_path.exists():
    log_path.unlink()

logger = logging.getLogger("demo")
# ... logger.info, warning, error

# À la fin :
# contenu = log_path.read_text(encoding="utf-8")
# assert "info msg" in contenu
# assert "warning msg" in contenu
# assert "error msg" in contenu


# =============================================================================
# 6.5 — EAFP vs LBYL
# =============================================================================
# Ré-écrivez cette fonction en style EAFP (try/except) :

def valeur_ou_defaut_lbyl(d: dict, cle: str, defaut):
    if cle in d and d[cle] is not None:
        return d[cle]
    return defaut


def valeur_ou_defaut_eafp(d: dict, cle: str, defaut):
    ...  # TODO : try/except KeyError, traiter aussi None


assert valeur_ou_defaut_eafp({"a": 1}, "a", 99) == 1
assert valeur_ou_defaut_eafp({"a": None}, "a", 99) == 99
assert valeur_ou_defaut_eafp({}, "a", 99) == 99


if __name__ == "__main__":
    print("Tous les tests passent ✅")
