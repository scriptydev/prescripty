from __future__ import annotations

import os

from scripty import bot

if __name__ == "__main__":
    if os.name != "nt":
        import uvloop

        uvloop.install()

    bot.start_app()
