__all__: list[str] = ["load_component", "unload_component"]

import random

from typing import Any

import aiohttp
import alluka
import hikari
import miru
import tanchi
import tanjun

import scripty

component = tanjun.Component()

ACTIVITIES = {
    "Watch Together": "880218394199220334",
    "Poker Night": "755827207812677713",
    "Betrayal.io": "773336526917861400",
    "Fishington.io": "814288819477020702",
    "Chess In The Park": "832012774040141894",
    "Sketchy Artist": "879864070101172255",
    "Awkword": "879863881349087252",
    "Doodle Crew": "878067389634314250",
    "Sketch Heads": "902271654783242291",
    "Letter League": "879863686565621790",
    "Word Snacks": "879863976006127627",
    "SpellCast": "852509694341283871",
    "Checkers In The Park": "832013003968348200",
    "Blazing 8s": "832025144389533716",
    "Putt Party": "945737671223947305",
    "Land-io": "903769130790969345",
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


@component.with_command
@tanchi.as_slash_command()
async def activity(
    ctx: tanjun.abc.SlashContext,
    activity: tanchi.Autocompleted[activity_autocomplete],
    channel: hikari.GuildVoiceChannel,
    bot: alluka.Injected[hikari.GatewayBot],
) -> None:
    """Start a Discord Activity"""
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


animal = component.with_slash_command(
    tanjun.slash_command_group("animal", "Fun things related to animals")
)


@animal.with_command
@tanchi.as_slash_command()
async def cat(
    ctx: tanjun.abc.Context,
    session: alluka.Injected[aiohttp.ClientSession],
) -> None:
    """Get a random cat image"""
    async with session.get(
        "https://api.thecatapi.com/v1/images/search",
        headers={"x-api-key": scripty.THE_CAT_API_KEY},
    ) as response:
        data = await response.json()

    embed = scripty.Embed(title="Cat")
    embed.set_image(data[0]["url"])

    await ctx.respond(embed)


@animal.with_command
@tanchi.as_slash_command()
async def dog(
    ctx: tanjun.abc.Context,
    session: alluka.Injected[aiohttp.ClientSession],
) -> None:
    """Get a random dog image"""
    async with session.get("https://dog.ceo/api/breeds/image/random") as response:
        data = await response.json()

    embed = scripty.Embed(title="Dog")
    embed.set_image(data["message"])

    await ctx.respond(embed)


@component.with_command
@tanchi.as_slash_command()
async def coin(ctx: tanjun.abc.SlashContext) -> None:
    """Flip a coin"""
    await ctx.respond(
        scripty.Embed(
            title="Coin",
            description=random.choice(["Heads", "Tails"]),
        )
    )


@component.with_command
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
    async def next(self, _: miru.Button, ctx: miru.Context) -> None:  # type: ignore
        self.index += 1
        if self.index == len(self.submissions):
            self.index = 0

        embed = scripty.Embed(
            title=self.submissions[self.index]["title"],
            url=f"https://reddit.com{self.submissions[self.index]['permalink']}",
        )
        embed.set_image(self.submissions[self.index]["url"])
        await ctx.edit_response(embed)

    @miru.button(label="Stop", style=hikari.ButtonStyle.DANGER)
    async def stop_(self, _: miru.Button, ctx: miru.Context) -> None:  # type: ignore
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


@component.with_command
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
        title=submissions[index]["title"],
        url=f"https://reddit.com{submissions[index]['permalink']}",
    )
    embed.set_image(submissions[index]["url"])

    response = await ctx.respond(embed, ensure_result=True, components=view.build())

    view.start(response)
    await view.wait()


@component.with_command
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
    async def rock(self, _: miru.Button, ctx: miru.Context) -> None:  # type: ignore
        await ctx.edit_response(self.determine_outcome("Rock"), components=[])
        self.stop()

    @miru.button(label="Paper", style=hikari.ButtonStyle.SUCCESS)
    async def paper(self, _: miru.Button, ctx: miru.Context) -> None:  # type: ignore
        await ctx.edit_response(self.determine_outcome("Paper"), components=[])
        self.stop()

    @miru.button(label="Scissors", style=hikari.ButtonStyle.PRIMARY)
    async def scissors(self, _: miru.Button, ctx: miru.Context) -> None:  # type: ignore
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


@component.with_command
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


@tanjun.as_loader
def load_component(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())


@tanjun.as_unloader
def unload_component(client: tanjun.Client) -> None:
    client.remove_component_by_name(component.name)
