import random
import typing

import aiohttp
import hikari
import lightbulb
import miru

import scripty
from scripty import functions


fun = lightbulb.Plugin("Fun")


@fun.command
@lightbulb.command("coin", "Flip a coin", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def coin(ctx: lightbulb.Context) -> None:
    coin = ["Heads", "Tails"]
    embed = hikari.Embed(
        title="Coin",
        description=random.choice(coin),
        color=functions.Color.blurple(),
    )
    await ctx.respond(embed)


@fun.command
@lightbulb.option(
    "sides", "The number of sides on the die", int, required=False, min_value=2
)
@lightbulb.command("dice", "Roll a die", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def dice(ctx: lightbulb.Context) -> None:
    sides: int = ctx.options.sides or 2
    embed = hikari.Embed(
        title="Dice",
        description=random.randint(1, sides),
        color=functions.Color.blurple(),
    )
    await ctx.respond(embed)


@fun.command
@lightbulb.command("meme", "The hottest Reddit r/memes", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def meme(ctx: lightbulb.Context) -> None:
    async with aiohttp.ClientSession() as session:
        reddit_url = "https://reddit.com/r/memes/hot.json"
        async with session.get(reddit_url) as response:
            reddit = await response.json()

    submissions: typing.Any = []
    for submission in range(len(reddit["data"]["children"])):
        submissions.append(reddit["data"]["children"][submission]["data"])
    random_submission = random.choice(submissions)

    if not random_submission["over_18"]:
        if random_submission["is_video"]:
            await ctx.respond(f"[]({random_submission['url']})")
        else:
            embed = hikari.Embed(
                title=random_submission["title"],
                url=f"https://reddit.com{random_submission['permalink']}",
                color=functions.Color.blurple(),
            )
            embed.set_image(random_submission["url"])
            await ctx.respond(embed)


@fun.command
@lightbulb.command("rickroll", ";)", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def rickroll(ctx: lightbulb.Context) -> None:
    await ctx.respond("https://youtu.be/dQw4w9WgXcQ")


class RPSView(miru.View):
    rps: dict[str, int] = {"Rock": 0, "Paper": 1, "Scissors": 2}

    def __init__(self):
        super().__init__(timeout=30.0)
        self._rps = random.choice((0, 1, 2))

    def get_value(self, key: str) -> int:
        return self.rps[key]

    def get_key(self, value: int) -> str:
        if not 0 <= value <= 2:
            raise ValueError("Invalid value")

        return tuple(k for k, v in self.rps.items() if v == value)[0]

    def generate_embed(self, message: str) -> hikari.Embed:
        return hikari.Embed(
            title="RPS",
            description=message,
            color=functions.Color.blurple(),
        )

    def determine_outcome(self, player_choice: str) -> hikari.Embed:
        player_value = self.get_value(player_choice)
        computer_choice = self.get_key(self._rps)

        if (player_value + 1) % 3 == self._rps:
            return self.generate_embed(
                f"You lost! `{computer_choice}` beats `{player_choice}`"
            )

        elif player_value == self._rps:
            return self.generate_embed(f"You tied! Both chose `{player_choice}`")

        else:
            return self.generate_embed(
                f"You won! `{player_choice}` beats `{computer_choice}`"
            )

    @miru.button(label="Rock", style=hikari.ButtonStyle.DANGER)
    async def rock(self, button: miru.Button, ctx: miru.Context) -> None:  # type: ignore
        await ctx.edit_response(
            self.determine_outcome("Rock"), components=hikari.UNDEFINED
        )
        self.stop()

    @miru.button(label="Paper", style=hikari.ButtonStyle.SUCCESS)
    async def paper(self, button: miru.Button, ctx: miru.Context) -> None:  # type: ignore
        await ctx.edit_response(
            self.determine_outcome("Paper"), components=hikari.UNDEFINED
        )
        self.stop()

    @miru.button(label="Scissors", style=hikari.ButtonStyle.PRIMARY)
    async def scissors(self, button: miru.Button, ctx: miru.Context) -> None:  # type: ignore
        await ctx.edit_response(
            self.determine_outcome("Scissors"), components=hikari.UNDEFINED
        )
        self.stop()

    async def view_check(self, context: miru.Context) -> bool:
        assert self.message is not None
        assert self.message.interaction is not None

        if context.user != self.message.interaction.user:
            embed = hikari.Embed(
                title="Error",
                description="This command was not invoked by you!",
                color=functions.Color.blurple(),
            )
            await context.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
            return False
        else:
            return True

    async def on_timeout(self) -> None:
        self.rock.disabled = True
        self.paper.disabled = True
        self.scissors.disabled = True
        self.add_item(
            miru.Button(
                style=hikari.ButtonStyle.SECONDARY, label="Timed out", disabled=True
            )
        )

        assert self.message is not None, "Message is None"
        await self.message.edit(components=self.build())


@fun.command
@lightbulb.command("rps", "Play rock paper scissors", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def rps(ctx: lightbulb.SlashContext) -> None:
    view = RPSView()

    embed = hikari.Embed(
        title="RPS",
        description="Click on the button options to continue the game!",
        color=functions.Color.blurple(),
    )

    await ctx.respond(embed=embed, components=view.build())

    message = await ctx.interaction.fetch_initial_response()
    view.start(message)
    await view.wait()


def load(bot: scripty.BotApp):
    bot.add_plugin(fun)


def unload(bot: scripty.BotApp):
    bot.remove_plugin(fun)
