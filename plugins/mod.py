import hikari
import lightbulb

mod = lightbulb.Plugin("Mod")


@mod.command()
@lightbulb.option("amount", "Amount to delete", int)
@lightbulb.command("delete", "Purge messages", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def delete(ctx: lightbulb.Context) -> None:
    amount = ctx.options.amount
    await ctx.get_channel.delete_messages(amount)
    embed = hikari.Embed(
        title="Delete", description=f"Deleted `{amount}` messages!", color=0x5865F2
    )
    await ctx.respond(embed)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(mod)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(mod)
