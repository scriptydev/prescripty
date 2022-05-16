__all__: list[str] = ["AERO_API", "INVITE_URL"]

from typing import Final

import hikari

import scripty.config
import scripty.functions

AERO_API: Final[str] = "https://ravy.org/api/v1"
INVITE_URL: Final[str] = scripty.functions.generate_oauth(
    scripty.config.CLIENT_ID, permissions=hikari.Permissions.ADMINISTRATOR
)
