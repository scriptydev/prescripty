from __future__ import annotations

__all__: tuple[str, ...] = ("HTTPError", "on_error")

import tanjun

from scripty.functions import embeds


class HTTPError(Exception):
    """A default exception to be raised when an error with a HTTP request occurs"""


async def on_error(ctx: tanjun.abc.Context, exc: Exception) -> None:
    """Global error handler

    Parameters
    ----------
    ctx : tanjun.abc.Context
        The command context this error was raised for.
    exc : Exception
        The error which was raised.

    Returns
    -------
    bool | None
        The return type indicates whether this hook wants the error to be
        suppressed where `True` indicates that it should be suppressed,
        `False` indicates that it should be re-raised and `None` indicates
        no decision.
        This value will be considered along with the results of any other hooks
        being called during execution by a majority rule system and if all
        hooks return `None` then the error will be raised.
    """
    await ctx.respond(
        embeds.Embed(
            title="Error",
            description=f"This interaction failed!\n```{exc}```",
        )
    )
