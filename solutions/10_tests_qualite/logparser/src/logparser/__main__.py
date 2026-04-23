import argparse
import logging
import sys
from pathlib import Path

from .analytics import top_ips, status_counts
from .parser import parse_file


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyse un fichier de logs Nginx.")
    parser.add_argument("fichier", type=Path)
    parser.add_argument("--top", type=int, default=10, help="top N IPs")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.WARNING,
        format="[%(levelname)s] %(message)s",
    )

    if not args.fichier.exists():
        print(f"Erreur : {args.fichier} introuvable", file=sys.stderr)
        return 1

    entries = list(parse_file(args.fichier))
    print(f"{len(entries)} entrées lues.")
    print()
    print(f"Top {args.top} IPs :")
    for ip, n in top_ips(entries, args.top):
        print(f"  {n:>6}  {ip}")
    print()
    print("Status codes :")
    for code, n in sorted(status_counts(entries).items()):
        print(f"  {code}: {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
