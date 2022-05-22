__all__: list[str] = ["AERO_API", "AERO_HEADERS", "INVITE_URL"]

from typing import Final

import hikari

from .config import AERO_API_KEY, CLIENT_ID
from .functions import generate_oauth

AERO_API: Final[str] = "https://ravy.org/api/v1"
AERO_HEADERS: Final[dict[str, str]] = {"Authorization": f"Ravy {AERO_API_KEY}"}
INVITE_URL: Final[str] = generate_oauth(
    CLIENT_ID, permissions=hikari.Permissions.ADMINISTRATOR
)
