import datetime
import os

from dotenv import load_dotenv

import hikari
import lightbulb
import miru

import scripty


load_dotenv()


token = os.environ["TOKEN"]
guild_ids = (
    hikari.Snowflake(os.environ["GUILD_ID_PRIMARY"]),
    hikari.Snowflake(os.environ["GUILD_ID_SECONDARY"]),
)


class ScriptyBotApp(lightbulb.BotApp):
    def __init__(self) -> None:
        super().__init__(
            token=token,
            default_enabled_guilds=guild_ids,
            help_slash_command=True,
        )

    def setup(self) -> None:
        self.load_extensions_from("./scripty/extensions")
        miru.load(self)

    def run(self) -> None:
        self.setup()
        super().run(
            activity=(
                hikari.Activity(
                    name=f"Version {scripty.__version__}",
                    type=hikari.ActivityType.PLAYING,
                )
            )
        )


def instantiate_bot() -> ScriptyBotApp:
    bot = ScriptyBotApp()

    bot.uptime = int(round(datetime.datetime.now(datetime.timezone.utc).timestamp()))

    return bot


if __name__ == "__main__":
    if os.name != "nt":
        import uvloop

        uvloop.install()

    instantiate_bot().run()
