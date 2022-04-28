__all__: list[str] = ["Color"]


import enum


class Color(enum.Enum):
    """An enum with color assigned to hex values"""

    BLURPLE = 0x5865F2
    GREEN = 0x57F287
    YELLOW = 0xFEE75C
    FUCHSIA = 0xEB459E
    RED = 0xED4245
    WHITE = 0xFFFFFF
    BLACK = 0x000000
    GRAY_EMBED = 0x2F3136
