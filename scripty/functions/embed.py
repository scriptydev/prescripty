__all__: list[str] = ["Embed"]


import datetime
import typing

import hikari


DEFAULT_COLOR = 0x2F3136


class Embed(hikari.Embed):
    """Represents an embed

    This class is a subclass of ``hikari.Embed`` with changes to the
    default color values
    """

    def __init__(
        self,
        *,
        title: typing.Any = None,
        description: typing.Any = None,
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
