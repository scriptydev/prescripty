import datetime
import pathlib
import unittest

from typing import Generator

import scripty


class TestHelpers(unittest.TestCase):
    def test_datetime_utcnow_aware(self) -> None:
        self.assertIsInstance(scripty.datetime_utcnow_aware(), datetime.datetime)

        self.assertAlmostEqual(
            scripty.datetime_utcnow_aware(),
            datetime.datetime.now(datetime.timezone.utc),
        )

    def test_get_modules(self) -> None:
        self.assertIsInstance(scripty.get_modules("."), Generator)
        self.assertIsInstance(scripty.get_modules(pathlib.Path(".")), Generator)


class TestHelpersAsync(unittest.IsolatedAsyncioTestCase):
    async def test_parse_to_future_datetime(self) -> None:
        self.assertIsInstance(
            await scripty.parse_to_future_datetime("1 week"), datetime.datetime
        )

        self.assertIsNone(await scripty.parse_to_future_datetime("1 day ago"))
        self.assertIsNone(
            await scripty.parse_to_future_datetime(
                "Scripty is the Best Discord Bot 1234567890"
            )
        )

    async def test_parse_to_timedelta_from_now(self) -> None:
        self.assertIsInstance(
            await scripty.parse_to_timedelta_from_now("1 week"), datetime.timedelta
        )

        self.assertEqual(
            await scripty.parse_to_timedelta_from_now("22 hrs"),
            datetime.timedelta(hours=22),
        )

        self.assertIsNone(await scripty.parse_to_timedelta_from_now("1 day ago"))
        self.assertIsNone(
            await scripty.parse_to_timedelta_from_now(
                "Scripty is the Best Discord Bot 1234567890"
            )
        )


if __name__ == "__main__":
    unittest.main()
