import datetime

import hikari
import lightbulb
import miru

import scripty
from scripty.constants import TOKEN, GUILD_IDS


class BotApp(lightbulb.BotApp):
    """A subclassed implementation of `lightbulb.BotApp`"""

    def __init__(self) -> None:
        super().__init__(
            token=TOKEN,
            default_enabled_guilds=GUILD_IDS,
            help_slash_command=True,
        )

    def setup(self) -> None:
        self.load_extensions_from("./scripty/extensions")
        self.load_extensions("scripty.core.errors")
        self.load_extensions("scripty.core.help")

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


def run() -> None:
    bot = BotApp()

    bot.d.uptime = int(datetime.datetime.now(datetime.timezone.utc).timestamp())

    bot.run()
