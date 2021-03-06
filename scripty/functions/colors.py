from __future__ import annotations

__all__: tuple[str, ...] = ("Color",)

import enum


class Color(enum.IntEnum):
    """An enum with color assigned to hex values"""

    BLURPLE = 0x5865F2
    GREEN = 0x57F287
    YELLOW = 0xFEE75C
    FUCHSIA = 0xEB459E
    RED = 0xED4245
    WHITE = 0xFFFFFF
    BLACK = 0x000000
    INVISIBLE = 0x2F3136
