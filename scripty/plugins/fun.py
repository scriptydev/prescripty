import random

import aiohttp
import hikari
import lightbulb

from scripty import functions


fun = lightbulb.Plugin("Fun")


@fun.command()
@lightbulb.command("coin", "Flips a coin", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def coin(ctx: lightbulb.Context) -> None:
    coin = ["Heads", "Tails"]
    embed = hikari.Embed(
        title="Flip", description=random.choice(coin), color=functions.Color.blurple()
    )
    await ctx.respond(embed)


@fun.command()
@lightbulb.command("dice", "Rolls a die", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def dice(ctx: lightbulb.Context) -> None:
    dice = [1, 2, 3, 4, 5, 6]
    embed = hikari.Embed(
        title="Roll", description=random.choice(dice), color=functions.Color.blurple()
    )
    await ctx.respond(embed)


@fun.command()
@lightbulb.command("meme", "Fetches the hottest Reddit r/memes", auto_defer=True)
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


def load(bot: lightbulb.BotApp):
    bot.add_plugin(fun)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(fun)
