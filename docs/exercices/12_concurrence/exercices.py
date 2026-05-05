"""
Exercices — Chapitre 12 : Concurrence & async
"""
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


# =============================================================================
# 12.1 — Thread pool pour I/O
# =============================================================================
# Avec ThreadPoolExecutor, téléchargez (simulation via sleep) 10 "URLs" EN PARALLÈLE.
# Chaque download prend 0.5s. Le total doit être < 1s (sans threads : 5s).

def download(url: str) -> str:
    time.sleep(0.5)      # simule I/O
    return f"contenu de {url}"


def telecharger_en_parallele(urls: list[str]) -> list[str]:
    ...  # TODO : utiliser ThreadPoolExecutor


urls = [f"https://ex.com/{i}" for i in range(10)]
t0 = time.perf_counter()
results = telecharger_en_parallele(urls)
elapsed = time.perf_counter() - t0

assert len(results) == 10
assert elapsed < 1.5, f"trop lent : {elapsed:.2f}s"


# =============================================================================
# 12.2 — CPU-bound : ProcessPoolExecutor
# =============================================================================
# Le calcul ci-dessous est purement CPU. Les threads ne serviront à rien (GIL).
# Ré-implémentez `somme_en_parallele` avec ProcessPoolExecutor.
# (Nota : sur très petits inputs, overhead > gain. Ne pas s'en formaliser.)

def somme_carres(n: int) -> int:
    return sum(i * i for i in range(n))


def somme_en_parallele(taches: list[int]) -> list[int]:
    ...  # TODO : utiliser ProcessPoolExecutor


# On ne teste pas le temps car dépend machine et overhead
results = somme_en_parallele([100, 200, 300, 400])
assert results == [somme_carres(n) for n in [100, 200, 300, 400]]


# =============================================================================
# 12.3 — Async : gather
# =============================================================================
# Implémentez `fetch_all(urls)` : fait `simul_fetch` en parallèle avec gather.
# Le total doit être ~0.5s (pas 5 * 0.5).

async def simul_fetch(url: str) -> str:
    await asyncio.sleep(0.5)
    return f"contenu de {url}"


async def fetch_all(urls: list[str]) -> list[str]:
    ...  # TODO : asyncio.gather


async def _test_gather():
    t0 = time.perf_counter()
    results = await fetch_all([f"url{i}" for i in range(5)])
    elapsed = time.perf_counter() - t0
    assert len(results) == 5
    assert elapsed < 1.0, f"trop lent : {elapsed:.2f}s"


asyncio.run(_test_gather())


# =============================================================================
# 12.4 — Async : TaskGroup (3.11+)
# =============================================================================
# Réécrivez fetch_all avec TaskGroup.

async def fetch_all_tg(urls: list[str]) -> list[str]:
    ...  # TODO : utiliser asyncio.TaskGroup et create_task


async def _test_tg():
    results = await fetch_all_tg([f"url{i}" for i in range(3)])
    assert len(results) == 3


asyncio.run(_test_tg())


# =============================================================================
# 12.5 — Piège : bloquer l'event loop
# =============================================================================
# Le code ci-dessous est cassé : il BLOQUE l'event loop car time.sleep est
# synchrone. Réécrivez-le avec asyncio.sleep.

async def tache_cassee():
    time.sleep(1)      # ❌
    return "ok"


async def tache_correcte():
    ...  # TODO : utiliser asyncio.sleep


# =============================================================================
# 12.6 — to_thread pour code sync bloquant
# =============================================================================
# Vous devez appeler une fonction SYNC qui bloque (ex: requests.get).
# Utilisez asyncio.to_thread pour ne pas bloquer l'event loop.

def bloquant_sync(n: int) -> int:
    time.sleep(0.2)
    return n * 2


async def appeler_en_parallele(n_valeurs: list[int]) -> list[int]:
    ...  # TODO : asyncio.gather d'appels asyncio.to_thread(bloquant_sync, n)


async def _test_to_thread():
    t0 = time.perf_counter()
    res = await appeler_en_parallele([1, 2, 3, 4, 5])
    elapsed = time.perf_counter() - t0
    assert res == [2, 4, 6, 8, 10]
    assert elapsed < 0.6, f"séquentiel : {elapsed:.2f}s"


asyncio.run(_test_to_thread())


# =============================================================================
# 12.7 — Async Queue
# =============================================================================
# Producteur/consommateur avec asyncio.Queue.
# Le producteur met les nombres 0..9 dans la queue, puis un None.
# Le consommateur stocke tout dans une liste reçus jusqu'au None.

async def producteur(q: asyncio.Queue) -> None:
    ...  # TODO


async def consommateur(q: asyncio.Queue, sortie: list) -> None:
    ...  # TODO


async def _test_queue():
    q = asyncio.Queue()
    recu = []
    async with asyncio.TaskGroup() as tg:
        tg.create_task(producteur(q))
        tg.create_task(consommateur(q, recu))
    assert recu == list(range(10))


asyncio.run(_test_queue())


if __name__ == "__main__":
    print("Tous les tests passent ✅")
