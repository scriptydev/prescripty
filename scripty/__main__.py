import datetime
import os

import scripty


def instantiate_bot() -> scripty.BotApp:
    bot = scripty.BotApp()

    bot.d.uptime = int(datetime.datetime.now(datetime.timezone.utc).timestamp())

    return bot


if __name__ == "__main__":
    if os.name != "nt":
        import uvloop

        uvloop.install()

    instantiate_bot().run()
