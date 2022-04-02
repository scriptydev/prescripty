import asyncio

import hikari
import lightbulb


moderation = lightbulb.Plugin("Moderation")


@moderation.command()
@lightbulb.add_checks(
    lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES)
)
@lightbulb.option("amount", "Amount to delete", int, min_value=1)
@lightbulb.command("delete", "Purge messages", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def delete(ctx: lightbulb.Context) -> None:
    amount = ctx.options.amount
    channel = ctx.get_channel()
    try:
        if amount == 1:
            iterator = ctx.app.rest.fetch_messages(channel).limit(amount)
            async for messages in iterator.chunk(100):
                await ctx.app.rest.delete_messages(channel, messages)

            embed = hikari.Embed(
                title="Delete",
                description=f"`{amount} message` deleted",
                color=0x5865F2,
            )
            await ctx.respond(embed)
            return

        iterator = ctx.app.rest.fetch_messages(channel).limit(amount)
        async for messages in iterator.chunk(100):
            await ctx.app.rest.delete_messages(channel, messages)

        embed = hikari.Embed(
            title="Delete", description=f"`{amount} messages` deleted", color=0x5865F2
        )
        await ctx.respond(embed)
    except:  # Refactor later
        iterator = ctx.app.rest.fetch_messages(channel).limit(amount)
        async for messages in iterator:
            await ctx.app.rest.delete_message(channel, messages)
            await asyncio.sleep(1)

        embed = hikari.Embed(
            title="Delete", description=f"`{amount} messages` deleted", color=0x5865F2
        )
        await ctx.respond(embed)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(moderation)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(moderation)
