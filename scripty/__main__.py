from __future__ import annotations

import os

import scripty


if __name__ == "__main__":
    if os.name != "nt":
        import uvloop

        uvloop.install()

    scripty.start_app()
