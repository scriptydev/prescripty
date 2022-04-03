import hikari
import lightbulb

from scripty import functions


misc = lightbulb.Plugin("Miscellaneous")


@misc.command()
@lightbulb.command("Avatar", "Retrieves user avatar", auto_defer=True)
@lightbulb.implements(lightbulb.UserCommand)
async def avatar(ctx: lightbulb.Context) -> None:
    user = ctx.options.target

    embed = hikari.Embed(
        title=f"Avatar",
        color=functions.Color.blurple(),
    )
    embed.set_author(name=str(user), icon=user.avatar_url)
    embed.set_image(user.avatar_url)

    await ctx.respond(embed)


@misc.command()
@lightbulb.option("text", "Text to repeat", str)
@lightbulb.command("echo", "Repeats user input", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def echo(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(
        title="Echo",
        description=f"{ctx.author.mention} said: ```{ctx.options.text}```",
        color=functions.Color.blurple(),
    )
    await ctx.respond(embed)


@misc.command()
@lightbulb.option("option_2", "Option 2", str)
@lightbulb.option("option_1", "Option 1", str)
@lightbulb.option("description", "Description of the embed", str, required=False)
@lightbulb.option("title", "Title of the embed", str)
@lightbulb.command("poll", "Creates a simple poll", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def poll(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(
        title=ctx.options.title,
        description=ctx.options.description,
        color=functions.Color.blurple(),
    )
    embed.add_field(value=f"1️⃣ {ctx.options.option_1}")
    embed.add_field(value=f"2️⃣ {ctx.options.option_2}")

    message = await ctx.respond(embed)

    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")


def load(bot: lightbulb.BotApp):
    bot.add_plugin(misc)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(misc)
