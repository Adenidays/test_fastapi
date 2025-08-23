import sys
from typing import TYPE_CHECKING

from hypercorn.__main__ import main as hypercorn_main

from app.config import HOST, PORT

if TYPE_CHECKING:
    from collections.abc import Sequence


class Config:
    worker_class = "asyncio"
    workers = 2


hypercorn_config: Config = Config()


def run(args: list[str] | None = None) -> int:
    host = HOST
    port = PORT
    bind = f"{host}:{port}"
    argv: "Sequence[str]" = args if args is not None else sys.argv[1:]
    return hypercorn_main(
        [
            "app.main:app",
            f"--bind={bind}",
            "--config=python:app.web.hypercorn.hypercorn_config",
            *argv,
        ]
    )


if __name__ == "__main__":
    sys.exit(run())
