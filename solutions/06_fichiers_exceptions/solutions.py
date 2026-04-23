"""
Solutions — Chapitre 6
"""
import json
import logging
from pathlib import Path


# 6.1 — pathlib
# p = Path("/Users/alice/projets/monapp/src/utils.py")
# p.parent  -> Path('/Users/alice/projets/monapp/src')
# p.name    -> 'utils.py'
# p.stem    -> 'utils'
# p.suffix  -> '.py'
# p.parts   -> ('/', 'Users', 'alice', 'projets', 'monapp', 'src', 'utils.py')


# 6.2 — Lecture sûre
def lire_config(chemin: Path) -> dict:
    if not chemin.exists():
        return {}
    try:
        return json.loads(chemin.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ValueError(f"fichier invalide : {chemin}") from e


# 6.3 — Exceptions custom
class AppError(Exception):
    pass


class ConfigError(AppError):
    pass


class ValidationError(AppError):
    def __init__(self, field: str, message: str):
        super().__init__(f"{field}: {message}")
        self.field = field
        self.message = message


try:
    raise ConfigError("fichier invalide")
except AppError as e:
    assert str(e) == "fichier invalide"

try:
    raise ValidationError("email", "format invalide")
except ValidationError as e:
    assert e.field == "email"
    assert e.message == "format invalide"


# 6.4 — Logging configuré
log_path = Path("/tmp/test_logging.log")
if log_path.exists():
    log_path.unlink()

# Réinitialiser les handlers (utile si ce fichier est re-importé)
for h in list(logging.root.handlers):
    logging.root.removeHandler(h)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_path, encoding="utf-8"),
    ],
)

logger = logging.getLogger("demo")
logger.info("info msg")
logger.warning("warning msg")
logger.error("error msg")

# On s'assure que les handlers ont flushé
logging.shutdown()

contenu = log_path.read_text(encoding="utf-8")
assert "info msg" in contenu
assert "warning msg" in contenu
assert "error msg" in contenu


# 6.5 — EAFP
def valeur_ou_defaut_eafp(d: dict, cle: str, defaut):
    try:
        v = d[cle]
    except KeyError:
        return defaut
    return v if v is not None else defaut


assert valeur_ou_defaut_eafp({"a": 1}, "a", 99) == 1
assert valeur_ou_defaut_eafp({"a": None}, "a", 99) == 99
assert valeur_ou_defaut_eafp({}, "a", 99) == 99


print("Toutes les solutions passent ✅")
