from __future__ import annotations

__all__: tuple[str, ...] = ("loader_fun",)

import random

from typing import Any

import aiohttp
import alluka
import hikari
import miru
import tanchi
import tanjun

import scripty

animal = tanjun.slash_command_group("animal", "Fun things related to animals")


@tanjun.as_user_menu("Birthday")
async def birthday(
    ctx: tanjun.abc.MenuContext,
    user: hikari.User | hikari.InteractionMember,
) -> None:
    """Wish user a happy birthday"""
    await user.send(
        scripty.Embed(
            title="Birthday",
            description=f"{ctx.author} wished you a happy birthday, {user}!",
        )
    )

    await ctx.respond(
        scripty.Embed(
            title="Birthday",
            description=f"Birthday wish sent to {user}!",
        )
    )


ACTIVITIES = {
    "Poker Night": "755827207812677713",
    "Chess In The Park": "832012774040141894",
    "Letter League": "879863686565621790",
    "SpellCast": "852509694341283871",
    "Watch Together": "880218394199220334",
    "Checkers In The Park": "832013003968348200",
    "Word Snacks": "879863976006127627",
    "Blazing 8s": "832025144389533716",
    "Sketch Heads": "902271654783242291",
    "Land-io": "903769130790969345",
    # "Awkword": "879863881349087252",
    "Betrayal.io": "773336526917861400",
    "Fishington.io": "814288819477020702",
    "Putt Party": "945737671223947305",
    # "Sketchy Artist": "879864070101172255",
}


class ActivityView(miru.View):
    def __init__(self, invite: str, activity: str) -> None:
        super().__init__()
        self.add_item(
            miru.Button(
                label=f"Launch {activity}",
                url=invite,
            )
        )


async def activity_autocomplete(
    ctx: tanjun.abc.AutocompleteContext,
    activity: str,
) -> None:
    """Autocomplete for Discord Activities"""
    activity_map: dict[str, str] = {}

    for k, v in ACTIVITIES.items():
        if len(activity_map) == 10:
            break
        if activity.lower() in k.lower() or activity.lower() in v.lower():
            activity_map[k] = v

    await ctx.set_choices(activity_map)


@tanjun.with_own_permission_check(hikari.Permissions.CREATE_INSTANT_INVITE)
@tanchi.as_slash_command("activity")
async def activity_(
    ctx: tanjun.abc.SlashContext,
    bot: alluka.Injected[hikari.GatewayBot],
    activity: tanchi.Autocompleted[activity_autocomplete],
    channel: hikari.GuildVoiceChannel,
) -> None:
    """Start a Discord Activity

    Parameters
    ----------
    activity : str
        Activity to start
    channel : hikari.GuildVoiceChannel
        Channel for activity
    """
    if activity not in ACTIVITIES.values():
        await ctx.respond(
            scripty.Embed(
                title="Activity Error",
                description="Unable to find activity from autocomplete options",
            )
        )
        return

    invite = await bot.rest.create_invite(
        channel,
        target_type=hikari.TargetType.EMBEDDED_APPLICATION,
        target_application=int(activity),
    )

    for k, v in ACTIVITIES.items():
        if v == activity:
            activity = k

    view = ActivityView(str(invite), activity)

    await ctx.respond(components=view.build())


@animal.with_command
@tanchi.as_slash_command()
async def cat(
    ctx: tanjun.abc.SlashContext,
    session: alluka.Injected[aiohttp.ClientSession],
) -> None:
    """Get a random cat image"""
    async with session.get(
        "https://api.thecatapi.com/v1/images/search",
        headers={"x-api-key": scripty.THE_CAT_API_KEY},
    ) as response:
        data = await response.json()

    embed = scripty.Embed(title="Cat").set_image(data[0]["url"])

    await ctx.respond(embed)


@animal.with_command
@tanchi.as_slash_command()
async def httpcat(
    ctx: tanjun.abc.SlashContext,
    status_code: int,
) -> None:
    """Cats for HTTP status codes

    Parameters
    ----------
    status_code : int
        HTTP status code
    """
    await ctx.respond(
        scripty.Embed(title="HTTPCat").set_image(f"https://http.cat/{status_code}")
    )


@animal.with_command
@tanchi.as_slash_command()
async def dog(
    ctx: tanjun.abc.SlashContext,
    session: alluka.Injected[aiohttp.ClientSession],
) -> None:
    """Get a random dog image"""
    async with session.get("https://dog.ceo/api/breeds/image/random") as response:
        data = await response.json()

    embed = scripty.Embed(title="Dog").set_image(data["message"])

    await ctx.respond(embed)


@tanchi.as_slash_command()
async def coin(ctx: tanjun.abc.SlashContext) -> None:
    """Flip a coin"""
    await ctx.respond(
        scripty.Embed(
            title="Coin",
            description=random.choice(("Heads", "Tails")),
        )
    )


@tanchi.as_slash_command()
async def dice(
    ctx: tanjun.abc.SlashContext,
    sides: tanchi.Range[2, ...] = 6,
) -> None:
    """Roll a die

    Parameters
    ----------
    sides : tanchi.Range[int, ...]
        Number of sides on the die
    """
    await ctx.respond(
        scripty.Embed(
            title="Dice",
            description=random.randint(1, sides),
        )
    )


class MemeView(miru.View):
    def __init__(
        self, tanjun_ctx: tanjun.abc.Context, submissions: Any, index: int
    ) -> None:
        super().__init__(timeout=30.0)
        self.tanjun_ctx = tanjun_ctx
        self.submissions = submissions
        self.index = index

    @miru.button(label="Next", style=hikari.ButtonStyle.SECONDARY)
    async def next(self, _: miru.Button[Any], ctx: miru.Context) -> None:
        self.index += 1
        if self.index == len(self.submissions):
            self.index = 0

        embed = scripty.Embed(
            title=self.submissions[self.index]["title"],
            url=f"https://reddit.com{self.submissions[self.index]['permalink']}",
        ).set_image(self.submissions[self.index]["url"])

        await ctx.edit_response(embed)

    @miru.button(label="Stop", style=hikari.ButtonStyle.DANGER)
    async def stop_(self, _: miru.Button[Any], ctx: miru.Context) -> None:
        for item in self.children:
            item.disabled = True

        await ctx.edit_response(components=self.build())

        self.stop()

    async def view_check(self, ctx: miru.Context) -> bool:
        if self.message is None:
            raise AssertionError

        if ctx.user == self.tanjun_ctx.author:
            return True

        embed = scripty.Embed(
            title="Error",
            description="This command was not invoked by you!",
        )
        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return False

    async def on_timeout(self) -> None:
        if self.message is None:
            return

        for item in self.children:
            item.disabled = True

        self.add_item(
            miru.Button(
                style=hikari.ButtonStyle.SECONDARY,
                label="Timed out",
                disabled=True,
            )
        )

        await self.message.edit(components=self.build())


@tanchi.as_slash_command()
async def meme(
    ctx: tanjun.abc.SlashContext,
    session: alluka.Injected[aiohttp.ClientSession],
) -> None:
    """The hottest Reddit r/memes"""
    reddit_url = "https://reddit.com/r/memes/hot.json"

    async with session.get(reddit_url, headers={"User-Agent": "Scripty"}) as response:
        reddit = await response.json()

    submissions: Any = [
        reddit["data"]["children"][submission]["data"]
        for submission in range(len(reddit["data"]["children"]))
        if not reddit["data"]["children"][submission]["data"]["over_18"]
        and not reddit["data"]["children"][submission]["data"]["is_video"]
        and reddit["data"]["children"][submission]["data"]["post_hint"] == "image"
    ]

    random.shuffle(submissions)

    index = 0

    view = MemeView(ctx, submissions, index)

    embed = scripty.Embed(
        title=submissions[index]["title"][:255] + "\U00002026"
        if len(submissions[index]["title"]) > 256
        else submissions[index]["title"],
        url=f"https://reddit.com{submissions[index]['permalink']}",
    ).set_image(submissions[index]["url"])

    response = await ctx.respond(embed, ensure_result=True, components=view.build())

    view.start(response)
    await view.wait()


@tanchi.as_slash_command()
async def rickroll(ctx: tanjun.abc.SlashContext) -> None:
    """;)"""
    await ctx.respond("https://youtu.be/dQw4w9WgXcQ")


class RPSView(miru.View):
    rps: dict[str, int] = {"Rock": 0, "Paper": 1, "Scissors": 2}

    def __init__(self, tanjun_ctx: tanjun.abc.Context) -> None:
        super().__init__(timeout=30.0)
        self._rps = random.choice((0, 1, 2))
        self.tanjun_ctx = tanjun_ctx

    def get_value(self, key: str) -> int:
        return self.rps[key]

    def get_key(self, value: int) -> str:
        if not 0 <= value <= 2:
            raise ValueError("invalid value")

        return tuple(k for k, v in self.rps.items() if v == value)[0]

    @staticmethod
    def generate_embed(message: str) -> scripty.Embed:
        return scripty.Embed(
            title="RPS",
            description=message,
        )

    def determine_outcome(self, player_choice: str) -> scripty.Embed:
        player_value = self.get_value(player_choice)
        computer_choice = self.get_key(self._rps)

        if (player_value + 1) % 3 == self._rps:
            return self.generate_embed(
                f"You lost! `{computer_choice}` beats `{player_choice}`"
            )

        if player_value == self._rps:
            return self.generate_embed(f"You tied! Both chose `{player_choice}`")

        return self.generate_embed(
            f"You won! `{player_choice}` beats `{computer_choice}`"
        )

    @miru.button(label="Rock", style=hikari.ButtonStyle.DANGER)
    async def rock(self, _: miru.Button[Any], ctx: miru.Context) -> None:
        await ctx.edit_response(self.determine_outcome("Rock"), components=[])
        self.stop()

    @miru.button(label="Paper", style=hikari.ButtonStyle.SUCCESS)
    async def paper(self, _: miru.Button[Any], ctx: miru.Context) -> None:
        await ctx.edit_response(self.determine_outcome("Paper"), components=[])
        self.stop()

    @miru.button(label="Scissors", style=hikari.ButtonStyle.PRIMARY)
    async def scissors(self, _: miru.Button[Any], ctx: miru.Context) -> None:
        await ctx.edit_response(self.determine_outcome("Scissors"), components=[])
        self.stop()

    async def view_check(self, ctx: miru.Context) -> bool:
        if self.message is None:
            raise AssertionError

        if ctx.user == self.tanjun_ctx.author:
            return True

        embed = scripty.Embed(
            title="Error",
            description="This command was not invoked by you!",
        )
        await ctx.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
        return False

    async def on_timeout(self) -> None:
        if self.message is None:
            return

        for item in self.children:
            item.disabled = True

        self.add_item(
            miru.Button(
                style=hikari.ButtonStyle.SECONDARY,
                label="Timed out",
                disabled=True,
            )
        )

        await self.message.edit(components=self.build())


@tanchi.as_slash_command()
async def rps(ctx: tanjun.abc.SlashContext) -> None:
    """Play rock paper scissors"""
    view = RPSView(ctx)

    embed = scripty.Embed(
        title="RPS",
        description="Click on the button options to continue the game!",
    )

    response = await ctx.respond(embed, ensure_result=True, components=view.build())

    view.start(response)
    await view.wait()


@tanchi.as_slash_command()
async def quote(
    ctx: tanjun.abc.SlashContext, session: alluka.Injected[aiohttp.ClientSession]
) -> None:
    """Responds with a random quote"""
    async with session.get(
        "https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en"
    ) as response:
        data = await response.json()

        embed = scripty.Embed(
            title="Quote",
            description=data["quoteText"],
        ).set_author(name=data["quoteAuthor"])

        await ctx.respond(embed)


loader_fun = tanjun.Component(name="fun").load_from_scope().make_loader()
