from __future__ import annotations

__all__: tuple[str, ...] = ("start_app",)

import functools

from typing import Sequence

import aiohttp
import alluka
import hikari
import miru
import tanjun

import scripty.config
import scripty.functions

import logging

logging.basicConfig(level=logging.DEBUG)


def create_client(
    bot: hikari.GatewayBot, datastore: scripty.functions.DataStore
) -> tanjun.Client:
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
        .set_type_dependency(scripty.functions.DataStore, datastore)
    )


def build_bot() -> tuple[hikari.GatewayBot, tanjun.Client]:
    """Build the bot"""
    datastore = scripty.functions.DataStore()
    on_bot_started_as_partial = functools.partial(on_bot_started, datastore=datastore)

    bot = hikari.GatewayBot(scripty.config.DISCORD_TOKEN)
    bot.subscribe(hikari.StartedEvent, on_bot_started_as_partial)

    client = create_client(bot, datastore)

    miru.load(bot)

    return bot, client


def start_app() -> None:
    """Start the application"""
    bot, _ = build_bot()
    bot.run()


async def on_client_starting(client: alluka.Injected[tanjun.Client]) -> None:
    """Setup to execute during client startup"""
    client.set_type_dependency(aiohttp.ClientSession, aiohttp.ClientSession())


async def on_client_closing(
    session: alluka.Injected[aiohttp.ClientSession | None],
) -> None:
    """Actions to perform while client shutdown"""
    if session:
        await session.close()


async def on_bot_started(
    _: hikari.StartingEvent, datastore: scripty.functions.DataStore
) -> None:
    """Called after bot is fully started"""
    datastore.start_time = scripty.functions.datetime_utcnow_aware()
