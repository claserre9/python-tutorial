# Chapitre 12 — Concurrence & async

Le chapitre que la plupart des tutos Python éludent ou bâclent. On va **comprendre le GIL** (pas juste le nommer), choisir entre `threading`, `multiprocessing` et `asyncio` en toute lucidité, et écrire du code asynchrone moderne avec `TaskGroup`.

## 1. Le GIL — ce qu'il est vraiment

Le **Global Interpreter Lock** est un mutex global dans CPython : **un seul thread Python exécute du bytecode à la fois**, même sur une machine multicœur. Les autres threads attendent.

**Pourquoi ?** Pour simplifier la gestion mémoire (refcounting) et garantir que l'état interne de l'interpréteur reste cohérent.

**Conséquence** : les threads Python ne parallélisent **pas** le CPU. Mais ils parallélisent **l'attente** (I/O réseau, fichier, DB), car un thread qui attend libère le GIL.

### Quand le GIL est libéré

- Pendant une opération I/O (read, write, socket, sleep).
- Pendant un calcul C natif qui a explicitement "relâché" le GIL (numpy, par exemple).
- Tous les ~5ms (approx.) pour laisser d'autres threads avancer.

### Résumé

| Type de charge | Threads Python | Solutions |
|---|---|---|
| **I/O-bound** (attente réseau/disque) | ✅ parallélise | `threading` ou `asyncio` |
| **CPU-bound** (calcul pur) | ❌ sérialisé par le GIL | `multiprocessing`, C extensions, `concurrent.futures.ProcessPoolExecutor` |

### Note : le GIL va disparaître

Python 3.13+ introduit un mode **"free-threaded"** (PEP 703) qui désactive le GIL. Encore expérimental et non activé par défaut. En 2026 on écrit encore du code "GIL-aware".

## 2. `threading` — pour l'I/O

```python
import threading
import time


def travail(n: int) -> None:
    time.sleep(1)          # simule de l'I/O
    print(f"fini {n}")


t0 = time.perf_counter()
threads = [threading.Thread(target=travail, args=(i,)) for i in range(5)]
for t in threads: t.start()
for t in threads: t.join()
print(f"total: {time.perf_counter() - t0:.1f}s")    # ~1s, pas 5
```

Sans threads : 5s. Avec : ~1s. Le GIL n'est pas un problème car pendant `time.sleep` il est libéré.

### `threading.Lock` — exclusion mutuelle

```python
compteur = 0
lock = threading.Lock()

def incremente():
    global compteur
    for _ in range(100_000):
        with lock:
            compteur += 1
```

Sans lock, la mutation `compteur += 1` (qui est read-modify-write, donc non atomique) peut perdre des updates en raison de context switches entre threads.

### Pièges

- **Deadlock** : deux threads s'attendent mutuellement.
- **Race conditions** : état partagé non synchronisé.
- **Coût du context switch** : ne lancez pas 10 000 threads. Utilisez un pool.

## 3. `concurrent.futures` — abstraction propre

Plutôt que gérer `Thread` à la main, utilisez les **executors**.

```python
from concurrent.futures import ThreadPoolExecutor


def telecharger(url: str) -> str:
    # ... I/O
    return response.text


urls = [...]

with ThreadPoolExecutor(max_workers=10) as pool:
    resultats = list(pool.map(telecharger, urls))
```

### `submit` + `as_completed`

Pour traiter les résultats dès qu'ils arrivent :

```python
from concurrent.futures import as_completed

with ThreadPoolExecutor(max_workers=10) as pool:
    futures = {pool.submit(telecharger, url): url for url in urls}
    for future in as_completed(futures):
        url = futures[future]
        try:
            contenu = future.result()
        except Exception as e:
            print(f"{url} : échec - {e}")
```

### `ProcessPoolExecutor` — pour le CPU

```python
from concurrent.futures import ProcessPoolExecutor


def calcul_lourd(x: int) -> int:
    return sum(i * i for i in range(x))


with ProcessPoolExecutor() as pool:
    resultats = list(pool.map(calcul_lourd, [10_000_000] * 8))
```

Chaque worker est un **processus Python distinct**, avec son propre GIL. Vrai parallélisme CPU.

**Contraintes** :
- Overhead de création de processus (~millisecondes).
- Les arguments et retours doivent être **picklables** (serialisables).
- Pas de partage d'état (utiliser `Queue` ou `Manager` si nécessaire).

## 4. `asyncio` — programmation asynchrone

**Principe** : un seul thread, mais des fonctions qui **suspendent** leur exécution pendant les I/O, permettant à d'autres fonctions de progresser.

Moins coûteux que `threading` (pas de context switch OS), à la mode depuis Python 3.5.

### Syntaxe de base

```python
import asyncio


async def saluer(nom: str, delai: float) -> None:
    await asyncio.sleep(delai)          # suspend, n'exécute PAS time.sleep
    print(f"bonjour {nom}")


async def main() -> None:
    await asyncio.gather(
        saluer("Alice", 1),
        saluer("Bob", 2),
        saluer("Carol", 0.5),
    )


asyncio.run(main())
# Total : ~2s (le plus lent), pas 3.5s séquentiel
```

### Concepts clés

- **`async def`** : définit une **coroutine**. Son appel retourne un objet coroutine, il ne s'exécute pas.
- **`await`** : attend une coroutine / future. Cède la main à l'event loop pendant l'attente.
- **event loop** : l'orchestrateur qui exécute les coroutines. Géré par `asyncio.run()`.
- **Task** : coroutine planifiée pour s'exécuter (via `asyncio.create_task(...)`).

### `TaskGroup` (3.11+) — la bonne façon

```python
async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(saluer("Alice", 1))
        tg.create_task(saluer("Bob", 2))
        tg.create_task(saluer("Carol", 0.5))
    # attend la fin de toutes les tasks à la sortie du with
```

Avantages sur `gather` :
- **Gestion d'erreurs propre** : si une task échoue, les autres sont annulées proprement (via `CancelledError`).
- **Pas d'oubli** : impossible de laisser une task orpheline.
- **ExceptionGroup** : les erreurs multiples sont rassemblées.

### `asyncio.gather`

Plus ancien, encore utilisé :

```python
results = await asyncio.gather(
    fetch(url1),
    fetch(url2),
    return_exceptions=True,    # retourne les exceptions au lieu de lever
)
```

### Timeouts

```python
# Ancien
try:
    await asyncio.wait_for(tache(), timeout=5)
except asyncio.TimeoutError:
    ...

# Moderne (3.11+)
try:
    async with asyncio.timeout(5):
        await tache()
except TimeoutError:
    ...
```

### Pièges courants

**Pas mélanger sync et async bloquant.**

```python
async def handler():
    time.sleep(5)           # ❌ BLOQUE l'event loop. Tout s'arrête.
    requests.get(...)       # ❌ pareil
```

Dans une coroutine, n'appelez **que** :
- d'autres coroutines (avec `await`)
- du code rapide non-bloquant
- **ou** wrappez le code bloquant dans `asyncio.to_thread(...)` ou `loop.run_in_executor(...)`.

```python
# Bonne façon : pousser le bloquant dans un thread
async def handler():
    data = await asyncio.to_thread(requests.get, url)
```

**Oublier `await`** :

```python
async def ping():
    return "pong"

async def main():
    ping()           # ❌ crée une coroutine jamais awaited (warning "coroutine never awaited")
    await ping()     # ✅
```

### Bibliothèques async

- **`httpx`** : remplaçant async de `requests`.
- **`aiofiles`** : I/O fichiers async.
- **`asyncpg`**, **`aiomysql`**, **SQLAlchemy 2.0 async** : DB async.
- **FastAPI** : web framework async (Ch. 15).

## 5. `asyncio.Queue` — producteur/consommateur

```python
async def producteur(queue: asyncio.Queue):
    for i in range(10):
        await queue.put(i)
        await asyncio.sleep(0.1)
    await queue.put(None)       # signal de fin


async def consommateur(queue: asyncio.Queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"traite {item}")


async def main():
    q = asyncio.Queue()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(producteur(q))
        tg.create_task(consommateur(q))
```

## 6. Async generators et context managers

```python
async def ligne_par_ligne(path):
    import aiofiles
    async with aiofiles.open(path, encoding="utf-8") as f:
        async for ligne in f:
            yield ligne.strip()


async def main():
    async for ligne in ligne_par_ligne("big.log"):
        print(ligne)
```

Les `async with` et `async for` sont des équivalents asynchrones de leurs versions synchrones.

## 7. Choisir sa stratégie — tableau de décision

| Charge | Volume de tâches | Solution |
|---|---|---|
| I/O-bound, < 1000 concurrents | | `threading` via `ThreadPoolExecutor` |
| I/O-bound, 1000+ concurrents | | `asyncio` |
| CPU-bound, calcul pur | | `multiprocessing` via `ProcessPoolExecutor` |
| CPU-bound avec numpy/pandas | | un seul thread suffit (le GIL est libéré) |
| Hybride | | `asyncio` + `to_thread` pour les blocs sync |

---

### Piège courant : boucle event loop existante

```python
async def main(): ...

asyncio.run(main())        # ✅ en script

# Dans un notebook Jupyter, la loop tourne déjà :
await main()               # ✅ direct, sans run()
```

Et si vous écrivez une lib, ne jamais appeler `asyncio.run()` à l'intérieur (votre appelant gère la loop).

---

### Sous le capot : coroutine ≈ générateur

Historiquement, `async def` est basé sur le même mécanisme que `yield` (Ch. 9). Une coroutine est un générateur spécial où `yield` est remplacé par `await`. Les vieilles versions de Python faisaient littéralement :

```python
@asyncio.coroutine
def f():
    yield from asyncio.sleep(1)
```

Maintenant `async def` + `await` sont des mots-clés dédiés, mais la mécanique sous-jacente est la même : **frame persistante**, **suspendre/reprendre**.

---

## À retenir

- GIL : sérialise le CPU Python, mais est libéré pendant l'I/O.
- I/O-bound : `threading` ou `asyncio`. CPU-bound : `multiprocessing`.
- `concurrent.futures` : API propre avec `map`, `submit`, `as_completed`.
- `asyncio.TaskGroup` > `gather` depuis 3.11.
- Ne **jamais** bloquer l'event loop : wrappez dans `asyncio.to_thread`.
- Oublier `await` = coroutine jamais exécutée (warning).

---

➡️ [Chapitre 13 — Métaprogrammation & introspection](../13_metaprogrammation/README.md)
