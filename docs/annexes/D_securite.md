# Annexe D — Sécurité applicative

Les 10 erreurs de sécurité les plus fréquentes en Python, et comment ne pas les commettre.

## 1. Secrets en dur dans le code

```python
# ❌ JAMAIS
API_KEY = "sk_live_abc123"
DATABASE_PASSWORD = "admin123"
```

Ce qui se passe :
- Le secret part dans git, visible dans l'historique **à jamais**, même si vous le supprimez dans un commit ultérieur.
- Impossible à changer par environnement (dev/staging/prod).

### Solution

Variables d'environnement + `pydantic-settings` :

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_key: str
    database_url: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
```

`.env` en local (dans `.gitignore` !), variables d'env en prod (docker, systemd, k8s secrets).

### Si vous avez déjà committé un secret

**Révoquez-le immédiatement.** Réécrire l'historique git (`git filter-repo` / BFG) n'empêche pas les copies existantes. Supposer qu'il est compromis.

Outils pour pré-détecter :
- **`gitleaks`** / **`trufflehog`** : scannent l'historique git.
- **pre-commit hook** qui refuse les commits contenant des patterns (clés AWS, tokens...).

## 2. Injection SQL

Voir Annexe C. Règle absolue : **toujours** paramétriser. Jamais de f-string dans du SQL.

## 3. Command injection

```python
import os

# ❌ passer à travers un shell
fichier = input("fichier à compresser ? ")
os.system(f"gzip {fichier}")

# Input malicieux : "f; rm -rf /"
```

### Solution

`subprocess.run` avec `shell=False` (le défaut) et liste d'arguments :

```python
import subprocess

subprocess.run(["gzip", fichier], check=True)    # pas d'interprétation shell
```

**Ne jamais** passer `shell=True` avec une entrée utilisateur. Si vraiment nécessaire, validez strictement l'input.

## 4. `pickle` — code exécuté à la désérialisation

```python
import pickle

data = pickle.loads(donnees_reçues_du_reseau)   # ❌ exécute du code arbitraire
```

`pickle.loads` sur du data non-fiable = **RCE** (Remote Code Execution). Jamais sur des inputs externes.

### Solution

- `json` pour échanger du data.
- `msgpack` ou `cbor2` pour du binaire.
- `pickle` **uniquement** pour de l'inter-process Python contrôlé.

## 5. Parsing XML — XXE et bombes

```python
import xml.etree.ElementTree as ET

ET.fromstring(xml_externe)    # ❌ vulnérable à certaines attaques
```

Les parsers XML stdlib peuvent être abusés (XXE, milliard de lol) si exposés à de l'input externe.

### Solution

- `defusedxml` : wrappers sûrs des parsers stdlib.

```python
import defusedxml.ElementTree as ET
ET.fromstring(xml_externe)    # ✅
```

## 6. Hash de mots de passe

```python
import hashlib

# ❌ SHA256 n'est PAS fait pour les mots de passe
hashlib.sha256(password.encode()).hexdigest()
```

Les hashs cryptographiques rapides (SHA256, MD5) sont faits pour l'intégrité, pas pour les mots de passe. Un attaquant peut tester des milliards de candidats par seconde sur GPU.

### Solution

Utilisez un **KDF lent** : bcrypt, argon2, scrypt.

```python
from passlib.context import CryptContext

ctx = CryptContext(schemes=["bcrypt"])
hashed = ctx.hash("mon_mdp")
ctx.verify("mon_mdp", hashed)
```

Ou `argon2` (plus récent, recommandé par OWASP) :

```python
from argon2 import PasswordHasher

ph = PasswordHasher()
hashed = ph.hash("mon_mdp")
ph.verify(hashed, "mon_mdp")
```

## 7. `eval` / `exec` sur input utilisateur

```python
eval(input("expr : "))       # ❌ catastrophe
```

Évidemment dangereux. Si vous voulez évaluer une expression arithmétique contrôlée :

```python
# ast.literal_eval n'exécute pas de code, accepte seulement des littéraux
import ast
ast.literal_eval("[1, 2, {'a': 3}]")    # OK
ast.literal_eval("__import__('os').system('rm -rf /')")  # ValueError
```

Pour des expressions mathématiques : `sympy`, `numpy.safe_eval`, ou un vrai parser.

## 8. Validation d'input

Pour tout input externe (API, form, query string) : **valider** avec Pydantic (voir Ch. 15).

```python
class UserIn(BaseModel):
    email: EmailStr
    age: int = Field(ge=0, le=150)
    password: str = Field(min_length=8)
```

FastAPI rejette automatiquement les payloads invalides avec 422. Aucun code à écrire.

## 9. Audit de dépendances

Une dépendance tierce peut contenir une faille ou être compromise. Vérifier régulièrement :

```bash
uv pip install pip-audit
pip-audit                   # scanne les deps installées contre CVE
```

Alternative : `safety check`.

En CI (GitHub Actions) :

```yaml
- name: Audit
  run: uv run pip-audit
```

Pour détecter les **typosquats** et **paquets malicieux** : `pip-audit --requirement requirements.txt`.

## 10. Secrets dans les logs

```python
logger.info(f"authenticating user: {user.email}, password: {password}")  # ❌
```

Les logs sont partagés (Sentry, Datadog, fichiers partout). Ne jamais logger :
- Mots de passe, tokens, clés API
- Numéros de carte, SSN, infos médicales
- Clés privées

### Mécanisme : filtre sur les logs sensibles

```python
class RedactFilter(logging.Filter):
    SECRETS = ("password", "token", "api_key")
    def filter(self, record):
        msg = record.getMessage()
        for secret in self.SECRETS:
            if secret in msg.lower():
                record.msg = "[REDACTED]"
        return True

logger.addFilter(RedactFilter())
```

Mieux : **ne pas** mettre les secrets dans le message. Utiliser `extra` ou structurer.

---

## Ressources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/) (généralement applicable)
- [Python Security Guide](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [Bandit](https://bandit.readthedocs.io/) : linter de sécurité Python. Peut tourner en CI.

## Règles d'or

1. **Jamais de secrets** dans le code / git.
2. **Jamais d'interpolation** d'input utilisateur dans du SQL, du shell, ou du code.
3. **Toujours** paramétriser, valider, échapper.
4. **Toujours** hasher les mots de passe avec un KDF lent.
5. **Auditer** les dépendances en CI.
6. **Redacter** les secrets dans les logs.

La sécurité n'est pas une feature — c'est un **défaut**. Si vous avez un doute, c'est que ce n'est pas sûr.
