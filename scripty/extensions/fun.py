import random

import aiohttp
import hikari
import lightbulb
import miru

from scripty import functions


fun = lightbulb.Plugin("Fun")


@fun.command()
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


@fun.command()
@lightbulb.command("dice", "Roll a die", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def dice(ctx: lightbulb.Context) -> None:
    dice = [1, 2, 3, 4, 5, 6]
    embed = hikari.Embed(
        title="Dice",
        description=random.choice(dice),
        color=functions.Color.blurple(),
    )
    await ctx.respond(embed)


@fun.command()
@lightbulb.command("meme", "The hottest Reddit r/memes", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def meme(ctx: lightbulb.Context) -> None:
    async with aiohttp.ClientSession() as session:
        reddit_url = "https://reddit.com/r/memes/hot.json"
        async with session.get(reddit_url) as response:
            reddit = await response.json()

    submissions = []
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


@fun.command()
@lightbulb.command("rickroll", ";)", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def rickroll(ctx: lightbulb.Context) -> None:
    await ctx.respond("https://youtu.be/dQw4w9WgXcQ")


class RPSView(miru.View):
    RPS = ("Rock", "Paper", "Scissors")

    win = hikari.Embed(
        title="RPS",
        description="You won! You chose `{}` and Scripty chose `{}`",
        color=functions.Color.blurple(),
    )

    lose = hikari.Embed(
        title="RPS",
        description="You lost! You chose `{}` and Scripty chose `{}`",
        color=functions.Color.blurple(),
    )

    tie = hikari.Embed(
        title="RPS",
        description="You tied! You chose `{}` and Scripty chose `{}`",
        color=functions.Color.blurple(),
    )

    def __init__(self):
        super().__init__(timeout=30.0)
        self._rps = random.choice(self.RPS)

    @miru.button(label="Rock", style=hikari.ButtonStyle.PRIMARY)
    async def rock(self, button: miru.Button, ctx: miru.Context) -> None:
        RESPONSES = {
            "Rock": self.win,
            "Paper": self.lose,
            "Scissors": self.tie,
        }

        RESPONSES[self._rps].description = RESPONSES[self._rps].description.format(
            self.rock.label, self._rps
        )

        await ctx.edit_response(RESPONSES[self._rps], components=None)
        self.stop()

    @miru.button(label="Paper", style=hikari.ButtonStyle.DANGER)
    async def paper(self, button: miru.Button, ctx: miru.Context) -> None:
        RESPONSES = {
            "Rock": self.win,
            "Paper": self.tie,
            "Scissors": self.lose,
        }

        RESPONSES[self._rps].description = RESPONSES[self._rps].description.format(
            self.paper.label, self._rps
        )

        await ctx.edit_response(RESPONSES[self._rps], components=None)
        self.stop()

    @miru.button(label="Scissors", style=hikari.ButtonStyle.SUCCESS)
    async def scissors(self, button: miru.Button, ctx: miru.Context) -> None:
        RESPONSES = {
            "Rock": self.lose,
            "Paper": self.win,
            "Scissors": self.tie,
        }

        RESPONSES[self._rps].description = RESPONSES[self._rps].description.format(
            self.scissors.label, self._rps
        )

        await ctx.edit_response(RESPONSES[self._rps], components=None)
        self.stop()

    async def view_check(self, ctx: miru.Context) -> bool:
        if ctx.user != self.message.interaction.user:
            await ctx.respond("This isn't for you!", flags=hikari.MessageFlag.EPHEMERAL)
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

        await self.message.edit(components=self.build())


@fun.command()
@lightbulb.command("rps", "Play rock paper scissors", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def rps(ctx: lightbulb.Context) -> None:
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


def load(bot: lightbulb.BotApp):
    bot.add_plugin(fun)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(fun)
