__all__: list[str] = ["start_app"]

import pathlib

import aiohttp
import alluka
import hikari
import miru
import tanjun

import scripty.config
import scripty.functions


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
        .set_type_dependency(scripty.functions.DataStore, scripty.functions.DataStore())
    )


def build_bot() -> tuple[hikari.GatewayBot, tanjun.Client]:
    """Build the bot"""
    bot = hikari.GatewayBot(scripty.config.DISCORD_TOKEN)
    bot.subscribe(hikari.StartedEvent, on_started)

    client = create_client(bot)

    miru.load(bot)

    return bot, client


def start_app() -> None:
    """Start the application"""
    bot, _ = build_bot()
    bot.run()


async def on_starting(
    client: alluka.Injected[tanjun.Client], 
    datastore: alluka.Injected[scripty.functions.DataStore]
) -> None:
    """Setup to execute during client startup"""
    client.set_type_dependency(aiohttp.ClientSession, aiohttp.ClientSession())
    datastore.start_time = scripty.functions.datetime_utcnow_aware()


async def on_closing(session: alluka.Injected[aiohttp.ClientSession | None]) -> None:
    """Actions to perform while client shutdown"""
    if session:
        await session.close()
