"""
Solutions — Chapitre 12
"""
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


# 12.1 — Threads
def download(url: str) -> str:
    time.sleep(0.5)
    return f"contenu de {url}"


def telecharger_en_parallele(urls: list[str]) -> list[str]:
    with ThreadPoolExecutor(max_workers=10) as pool:
        return list(pool.map(download, urls))


# 12.2 — Processes
def somme_carres(n: int) -> int:
    return sum(i * i for i in range(n))


def somme_en_parallele(taches: list[int]) -> list[int]:
    with ProcessPoolExecutor() as pool:
        return list(pool.map(somme_carres, taches))


# 12.3 — gather
async def simul_fetch(url: str) -> str:
    await asyncio.sleep(0.5)
    return f"contenu de {url}"


async def fetch_all(urls: list[str]) -> list[str]:
    return await asyncio.gather(*(simul_fetch(u) for u in urls))


# 12.4 — TaskGroup
async def fetch_all_tg(urls: list[str]) -> list[str]:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(simul_fetch(u)) for u in urls]
    return [t.result() for t in tasks]


# 12.5 — async sleep
async def tache_correcte():
    await asyncio.sleep(1)
    return "ok"


# 12.6 — to_thread
def bloquant_sync(n: int) -> int:
    time.sleep(0.2)
    return n * 2


async def appeler_en_parallele(n_valeurs: list[int]) -> list[int]:
    return await asyncio.gather(
        *(asyncio.to_thread(bloquant_sync, n) for n in n_valeurs)
    )


# 12.7 — Queue
async def producteur(q: asyncio.Queue) -> None:
    for i in range(10):
        await q.put(i)
    await q.put(None)


async def consommateur(q: asyncio.Queue, sortie: list) -> None:
    while True:
        item = await q.get()
        if item is None:
            return
        sortie.append(item)


# Tests
if __name__ == "__main__":
    # Threads
    t0 = time.perf_counter()
    r = telecharger_en_parallele([f"u{i}" for i in range(10)])
    print(f"Threads : {time.perf_counter() - t0:.2f}s, {len(r)} résultats")

    # Async
    async def main():
        r = await fetch_all(["a", "b", "c"])
        assert len(r) == 3

        r2 = await fetch_all_tg(["a", "b"])
        assert len(r2) == 2

        r3 = await appeler_en_parallele([1, 2, 3])
        assert r3 == [2, 4, 6]

        q = asyncio.Queue()
        recu = []
        async with asyncio.TaskGroup() as tg:
            tg.create_task(producteur(q))
            tg.create_task(consommateur(q, recu))
        assert recu == list(range(10))

    asyncio.run(main())
    print("Toutes les solutions passent ✅")
