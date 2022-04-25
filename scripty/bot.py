__all__: list[str] = ["build_bot", "AppBot"]


import datetime
import pathlib

import aiohttp
import hikari
import miru
import tanjun

import scripty


class AppBot(hikari.GatewayBot):
    """A custom subclassed implementation of ``hikari.GatewayBot``"""

    def __init__(self) -> None:
        super().__init__(scripty.DISCORD_TOKEN)
        self._aiohttp_session: aiohttp.ClientSession
        self._uptime: datetime.datetime

    @property
    def aiohttp_session(self) -> aiohttp.ClientSession:
        return self._aiohttp_session

    @aiohttp_session.deleter
    async def aiohttp_session(self) -> None:
        await self._aiohttp_session.close()
        del self._aiohttp_session

    @property
    def uptime(self) -> datetime.datetime:
        return self._uptime

    @uptime.deleter
    def uptime(self) -> None:
        del self._uptime

    async def on_starting(self, event: hikari.StartingEvent) -> None:
        self._aiohttp_session = aiohttp.ClientSession()
        self._uptime = datetime.datetime.now(datetime.timezone.utc)

    async def on_stopping(self, event: hikari.StoppingEvent) -> None:
        del self.aiohttp_session
        del self.uptime

    def setup(self) -> None:
        create_client(self)
        miru.load(self)

    def run(self) -> None:
        self.setup()

        self.subscribe(hikari.StartingEvent, self.on_starting)
        self.subscribe(hikari.StoppingEvent, self.on_stopping)

        super().run(
            activity=hikari.Activity(
                name="v" + scripty.__version__,
                type=hikari.ActivityType.PLAYING,
            )
        )


def create_client(bot: AppBot) -> tanjun.Client:
    client = tanjun.Client.from_gateway_bot(
        bot,
        mention_prefix=True,
        declare_global_commands=True,
    )

    client.load_modules(*scripty.get_modules(pathlib.Path("scripty/modules")))

    return client


def build_bot() -> AppBot:
    return AppBot()
