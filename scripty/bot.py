__all__: list[str] = ["Attrs", "build_bot"]


import datetime
import pathlib

import aiohttp
import alluka
import hikari
import miru
import tanjun

import scripty


class Attrs:
    """Attributes for the bot
    
    This is setup ``on_starting`` by setting a tanjun client DI type dependency
    """
    def __init__(self) -> None:
        self._uptime = datetime.datetime.now(datetime.timezone.utc)

    @property
    def uptime(self) -> datetime.datetime:
        return self._uptime


async def on_starting(client: alluka.Injected[tanjun.abc.Client]) -> None:
    client.set_type_dependency(aiohttp.ClientSession, aiohttp.ClientSession())
    client.set_type_dependency(Attrs, Attrs())


async def on_closing(session: alluka.Injected[aiohttp.ClientSession | None]) -> None:
    if session:
        await session.close()


def create_client(bot: hikari.GatewayBot) -> tanjun.Client:
    """Setup the tanjun client"""
    return (
        tanjun.Client.from_gateway_bot(
            bot,
            mention_prefix=True,
            declare_global_commands=True,
        )
        .load_modules(*scripty.get_modules(pathlib.Path("scripty/modules")))
        .add_client_callback(tanjun.ClientCallbackNames.STARTING, on_starting)
        .add_client_callback(tanjun.ClientCallbackNames.CLOSING, on_closing)
    )


def build_bot() -> hikari.GatewayBot:
    bot = hikari.GatewayBot(scripty.DISCORD_TOKEN)

    create_client(bot)
    miru.load(bot)

    return bot
