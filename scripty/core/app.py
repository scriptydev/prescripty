import datetime

import hikari
import lightbulb
import miru

import scripty


class BotApp(lightbulb.BotApp):
    """A custom subclassed implementation of `lightbulb.BotApp` for Scripty"""

    def __init__(self) -> None:
        super().__init__(
            token=scripty.constants.TOKEN,
            default_enabled_guilds=scripty.constants.GUILD_IDS,
            help_slash_command=True,
        )

    def setup(self) -> None:
        """Load all Lightbulb extensions and setup Miru"""
        self.load_extensions_from(
            *["./scripty/core/extensions", "./scripty/extensions"]
        )

        miru.load(self)

    def run(self) -> None:
        """An override of `lightbulb.BotApp.run()` to add the additional `setup` function"""
        self.setup()

        super().run(
            activity=(
                hikari.Activity(
                    name=f"v{scripty.__version__}",
                    type=hikari.ActivityType.PLAYING,
                )
            )
        )


def run() -> None:
    """Instantiate the `BotApp` class and run the bot"""
    bot = BotApp()

    bot.d.uptime = int(datetime.datetime.now(datetime.timezone.utc).timestamp())

    bot.run()
