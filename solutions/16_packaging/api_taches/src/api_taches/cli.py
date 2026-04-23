import argparse

import uvicorn


def main() -> int:
    parser = argparse.ArgumentParser(prog="api-taches")
    sub = parser.add_subparsers(dest="cmd", required=True)

    serve = sub.add_parser("serve", help="Lance le serveur")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)
    serve.add_argument("--reload", action="store_true")

    args = parser.parse_args()

    if args.cmd == "serve":
        uvicorn.run(
            "api_taches.app:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
