__all__: list[str] = ["build_bot"]

import pathlib

import aiohttp
import alluka
import hikari
import miru
import tanjun

from .config import DISCORD_TOKEN
from .functions import DataStore, datetime_utcnow_aware, get_modules


def create_client(bot: hikari.GatewayBot) -> tanjun.Client:
    """Create the tanjun client"""
    return (
        tanjun.Client.from_gateway_bot(
            bot,
            mention_prefix=True,
            declare_global_commands=True,
        )
        .load_modules(*get_modules(pathlib.Path("scripty/modules")))
        .add_client_callback(tanjun.ClientCallbackNames.STARTING, on_starting)
        .add_client_callback(tanjun.ClientCallbackNames.CLOSING, on_closing)
        .set_type_dependency(DataStore, DataStore())
    )


def build_bot() -> hikari.GatewayBot:
    """Build the bot"""
    bot = hikari.GatewayBot(DISCORD_TOKEN)

    create_client(bot)
    miru.load(bot)

    return bot


async def on_starting(
    client: alluka.Injected[tanjun.Client],
    datastore: alluka.Injected[DataStore],
) -> None:
    """Setup to execute during startup"""
    client.set_type_dependency(aiohttp.ClientSession, aiohttp.ClientSession())
    datastore.start_time = datetime_utcnow_aware()


async def on_closing(session: alluka.Injected[aiohttp.ClientSession | None]) -> None:
    """Actions to perform while shutdown"""
    if session:
        await session.close()
