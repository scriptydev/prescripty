__all__: list[str] = ["Color"]


class Color:
    """A class for color functions that return hex colors"""

    @staticmethod
    def blurple():
        """Hexadecimal code for Discord blurple color

        Returns
        -------
        0x5865F2
        """
        return 0x5865F2

    @staticmethod
    def green():
        """Hexadecimal code for Discord green color

        Returns
        -------
        0x57F287
        """
        return 0x57F287

    @staticmethod
    def yellow():
        """Hexadecimal code for Discord yellow color

        Returns
        -------
        0xFEE75C
        """
        return 0xFEE75C

    @staticmethod
    def fuchsia():
        """Hexadecimal code for Discord fuchsia color

        Returns
        -------
        0xEB459E
        """
        return 0xEB459E

    @staticmethod
    def red():
        """Hexadecimal code for Discord red color

        Returns
        -------
        0xED4245
        """
        return 0xED4245

    @staticmethod
    def white():
        """Hexadecimal code for Discord white color

        Returns
        -------
        0xFFFFFF
        """
        return 0xFFFFFF

    @staticmethod
    def black():
        """Hexadecimal code for Discord black color

        Returns
        -------
        0x000000
        """
        return 0x000000

    @staticmethod
    def background_secondary():
        """Hexadecimal code for Discord background secondary gray color

        Returns
        -------
        0x2F3136
        """
        return 0x2F3136

    @staticmethod
    def dark_embed():
        """Alias for ``~.Color.background_secondary()``"""
        return Color.background_secondary()
