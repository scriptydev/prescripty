__all__: list[str] = ["Embed"]

import datetime

from typing import Any

import hikari

from .color import Color

DEFAULT_COLOR = Color.GRAY_EMBED.value


class Embed(hikari.Embed):
    """Represents an embed

    This class is a subclass of ``hikari.Embed`` with changes to the
    default color values
    """

    def __init__(
        self,
        *,
        title: Any = None,
        description: Any = None,
        url: str | None = None,
        color: hikari.Colorish | None = DEFAULT_COLOR,
        colour: hikari.Colorish | None = DEFAULT_COLOR,
        timestamp: datetime.datetime | None = None,
    ) -> None:
        super().__init__(
            title=title,
            description=description,
            url=url,
            color=color,
            colour=None if color else colour,
            timestamp=timestamp,
        )
