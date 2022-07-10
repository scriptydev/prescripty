import datetime
import pathlib
import unittest

from typing import Generator

import dateparser

from scripty.functions import helpers


class TestHelpers(unittest.TestCase):
    def test_datetime_utcnow_aware(self) -> None:
        self.assertIsInstance(helpers.datetime_utcnow_aware(), datetime.datetime)

        self.assertAlmostEqual(
            helpers.datetime_utcnow_aware(),
            datetime.datetime.now(datetime.timezone.utc),
            delta=datetime.timedelta(seconds=1),
        )

    def test_get_modules(self) -> None:
        self.assertIsInstance(helpers.get_modules("."), Generator)
        self.assertIsInstance(helpers.get_modules(pathlib.Path(".")), Generator)


class TestHelpersAsync(unittest.IsolatedAsyncioTestCase):
    async def test_parse_to_future_datetime(self) -> None:
        self.assertIsInstance(
            await helpers.parse_to_future_datetime("1 week"), datetime.datetime
        )

        scripty_parse = await helpers.parse_to_future_datetime("22 hrs")
        dateparser_parse = dateparser.parse(
            "22 hrs",
            settings={
                "RETURN_AS_TIMEZONE_AWARE": True,
                "PREFER_DATES_FROM": "future",
                "STRICT_PARSING": True,
            },
        )

        if scripty_parse is None or dateparser_parse is None:
            raise AssertionError

        self.assertAlmostEqual(
            scripty_parse, dateparser_parse, delta=datetime.timedelta(seconds=1)
        )

        self.assertIsNone(await helpers.parse_to_future_datetime("1 day ago"))
        self.assertIsNone(
            await helpers.parse_to_future_datetime(
                "Scripty is the Best Discord Bot 1234567890"
            )
        )

    async def test_parse_to_timedelta_from_now(self) -> None:
        self.assertIsInstance(
            await helpers.parse_to_timedelta_from_now("1 week"), datetime.timedelta
        )

        self.assertEqual(
            await helpers.parse_to_timedelta_from_now("22 hrs"),
            datetime.timedelta(hours=22),
        )

        self.assertIsNone(await helpers.parse_to_timedelta_from_now("1 day ago"))
        self.assertIsNone(
            await helpers.parse_to_timedelta_from_now(
                "Scripty is the Best Discord Bot 1234567890"
            )
        )


if __name__ == "__main__":
    unittest.main()
