__all__: list[str] = ["Attr", "build_bot"]


import datetime
import pathlib

import aiohttp
import alluka
import hikari
import miru
import tanjun

import scripty


class Attr:
    """Attributes for the bot

    This is setup ``on_starting()`` by setting a tanjun client DI type dependency
    """

    def __init__(self, bot: hikari.GatewayBotAware) -> None:
        self._bot: hikari.GatewayBotAware = bot
        self._start_time: datetime.datetime = scripty.datetime_utcnow_aware()

    @property
    def start_time(self) -> datetime.datetime:
        return self._start_time


async def on_starting(
    client: alluka.Injected[tanjun.abc.Client], bot: alluka.Injected[hikari.GatewayBot]
) -> None:
    """Setup to execute during startup"""
    client.set_type_dependency(Attr, Attr(bot))
    client.set_type_dependency(aiohttp.ClientSession, aiohttp.ClientSession())


async def on_closing(session: alluka.Injected[aiohttp.ClientSession | None]) -> None:
    """Actions to perform while shutdown"""
    if session:
        await session.close()


def create_client(bot: hikari.GatewayBot) -> tanjun.Client:
    """Create the tanjun client"""
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
    """Build the bot"""
    bot = hikari.GatewayBot(scripty.DISCORD_TOKEN)

    create_client(bot)
    miru.load(bot)

    return bot
