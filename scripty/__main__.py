import datetime
import os

from dotenv import load_dotenv

import hikari
import lightbulb


load_dotenv()


token = os.environ["TOKEN"]
guild_ids = [
    hikari.Snowflake(os.environ["GUILD_ID"]),
    hikari.Snowflake(os.environ["GUILD_ID_SECONDARY"]),
]


class BotApp(lightbulb.BotApp):
    def __init__(self):
        super().__init__(
            token=token,
            default_enabled_guilds=guild_ids,
            help_slash_command=True,
        )
        self.uptime = int(round(datetime.datetime.now().timestamp()))


def instantiate_bot() -> lightbulb.BotApp:
    bot = BotApp()
    bot.load_extensions_from("./scripty/plugins")

    return bot


if __name__ == "__main__":
    if os.name != "nt":
        import uvloop

        uvloop.install()

    instantiate_bot().run()
