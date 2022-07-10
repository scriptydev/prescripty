from __future__ import annotations

__all__: tuple[str, ...] = ("start_app",)

import functools

import aiohttp
import alluka
import hikari
import miru
import plane
import tanjun

from scripty import config, errors
from scripty.functions import datastore, helpers


def create_client(bot: hikari.GatewayBot, ds: datastore.DataStore) -> tanjun.Client:
    """Create the tanjun client"""
    return (
        tanjun.Client.from_gateway_bot(
            bot,
            mention_prefix=True,
            declare_global_commands=True,
        )
        .load_modules("scripty.modules")
        .add_client_callback(tanjun.ClientCallbackNames.STARTING, on_client_starting)
        .add_client_callback(tanjun.ClientCallbackNames.CLOSING, on_client_closing)
        .set_type_dependency(datastore.DataStore, ds)
        .set_hooks(tanjun.AnyHooks().set_on_error(errors.on_error))
    )


def build_bot() -> tuple[hikari.GatewayBot, tanjun.Client]:
    """Build the bot"""
    ds = datastore.DataStore()
    on_bot_started_as_partial = functools.partial(on_bot_started, ds=ds)

    bot = hikari.GatewayBot(config.DISCORD_TOKEN)
    bot.subscribe(hikari.StartedEvent, on_bot_started_as_partial)

    client = create_client(bot, ds)

    miru.load(bot)

    return bot, client


def start_app() -> None:
    """Start the application"""
    bot, _ = build_bot()
    bot.run()


async def on_client_starting(client: alluka.Injected[tanjun.Client]) -> None:
    """Setup to execute during client startup"""
    client.set_type_dependency(aiohttp.ClientSession, aiohttp.ClientSession())
    client.set_type_dependency(plane.Client, plane.Client(config.AERO_API_KEY))


async def on_client_closing(
    session: alluka.Injected[aiohttp.ClientSession],
    plane_client: alluka.Injected[plane.Client],
) -> None:
    """Actions to perform while client shutdown"""
    await session.close()
    await plane_client.close()


async def on_bot_started(_: hikari.StartingEvent, ds: datastore.DataStore) -> None:
    """Called after bot is fully started"""
    ds.start_time = helpers.datetime_utcnow_aware()
