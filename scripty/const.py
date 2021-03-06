__all__: tuple[str, ...] = ("AERO_API", "AERO_HEADERS", "INVITE_URL")

from typing import Final

import hikari

from scripty import config
from scripty.functions import helpers

AERO_API: Final[str] = "https://ravy.org/api/v1"
AERO_HEADERS: Final[dict[str, str]] = {"Authorization": f"Ravy {config.AERO_API_KEY}"}
INVITE_URL: Final[str] = helpers.generate_oauth(
    config.CLIENT_ID, permissions=hikari.Permissions.ADMINISTRATOR
)
