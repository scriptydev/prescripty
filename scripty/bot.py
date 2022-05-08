__all__: list[str] = ["build_bot"]

import pathlib

import aiohttp
import alluka
import hikari
import miru
import tanjun

import scripty.config
import scripty.functions

datastore = scripty.functions.DataStore()


def create_client(bot: hikari.GatewayBot) -> tanjun.Client:
    """Create the tanjun client"""
    return (
        tanjun.Client.from_gateway_bot(
            bot,
            mention_prefix=True,
            declare_global_commands=True,
        )
        .load_modules(*scripty.functions.get_modules(pathlib.Path("scripty/modules")))
        .add_client_callback(tanjun.ClientCallbackNames.STARTING, on_starting)
        .add_client_callback(tanjun.ClientCallbackNames.CLOSING, on_closing)
        .set_type_dependency(scripty.functions.DataStore, datastore)
    )


def build_bot() -> hikari.GatewayBot:
    """Build the bot"""
    bot = hikari.GatewayBot(scripty.config.DISCORD_TOKEN)
    bot.subscribe(hikari.StartedEvent, on_started)

    create_client(bot)
    miru.load(bot)

    return bot


async def on_starting(client: alluka.Injected[tanjun.Client]) -> None:
    """Setup to execute during client startup"""
    client.set_type_dependency(aiohttp.ClientSession, aiohttp.ClientSession())


async def on_started(event: hikari.StartingEvent) -> None:
    """Called after bot is fully started"""
    datastore.start_time = scripty.functions.datetime_utcnow_aware()


async def on_closing(session: alluka.Injected[aiohttp.ClientSession | None]) -> None:
    """Actions to perform while client shutdown"""
    if session:
        await session.close()
