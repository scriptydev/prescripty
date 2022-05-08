import os

from scripty import build_bot


if __name__ == "__main__":
    if os.name != "nt":
        import uvloop

        uvloop.install()

    bot, client = build_bot()
    bot.run()
