__all__: tuple[str, ...] = ("loader_automod",)

import alluka
import hikari
import plane

# import tanchi
import tanjun

from scripty.functions import embeds, helpers

component = tanjun.Component(name="automod")

automod = tanjun.slash_command_group("automod", "Activate automatic content moderation")


# @automod.with_command
# @tanchi.as_slash_command("activate")
# async def shield_activate(ctx: tanjun.abc.SlashContext) -> None:
#     """Activate MagykMod automod"""
#     # TODO: Some database system here probably to store the activation status along
#     # with the guild ID. Then a on_message event listener somewhere to listen for
#     # messages, check the content for links, and run them through Aero.
#     await ctx.respond("Not implemented error")


# @automod.with_command
# @tanchi.as_slash_command("deactivate")
# async def shield_deactivate(ctx: tanjun.abc.SlashContext) -> None:
#     """Deactivate MagykMod automod"""
#     # TODO: Let's see how lazy I am and wait until Johan actually decides to implement
#     # audit logging and then add automod.
#     await ctx.respond("Not implemented error")


@component.with_listener(hikari.GuildMessageCreateEvent)
async def on_guild_message_create(
    event: hikari.GuildMessageCreateEvent,
    bot: alluka.Injected[hikari.GatewayBot],
    pc: alluka.Injected[plane.Client],
) -> None:
    if not event.content:
        return

    url = helpers.validate_and_encode_url(event.content)

    if url is None:
        return

    data = await pc.urls.get_website(url["encoded"])

    if not data.is_fraudulent:
        return

    await event.message.delete()
    await bot.rest.create_message(
        event.channel_id,
        embeds.Embed(
            title="AutoMod",
            description=f"Web threat blocked!\n`{url['input']}`",
        ),
    )


@component.with_listener(hikari.MemberCreateEvent)
async def on_member_create(
    event: hikari.MemberCreateEvent,
    bot: alluka.Injected[hikari.GatewayBot],
    pc: alluka.Injected[plane.Client],
) -> None:
    data = await pc.users.get_bans(event.user.id)

    if not data.bans:
        return

    await bot.rest.ban_user(
        event.guild_id, event.member, reason="Banned by Scripty AutoMod"
    )


# @component.with_command
# @tanchi.as_slash_command("url")
# async def analyze_url(
#     ctx: tanjun.abc.SlashContext,
#     pc: alluka.Injected[plane.Client],
#     url: str,
# ) -> None:
#     """
#     Analyze URL input for scams

#     Parameters
#     ----------
#     url : str
#         URL to analyze
#     """
#     url_parsed = helpers.validate_and_encode_url(url)

#     if url_parsed is None:
#         await ctx.respond(
#             embeds.Embed(
#                 title="Analyze Error",
#                 description=(
#                     "Provided URL is malformed!\nPlease check if complies with [DNS]"
#                     "(https://en.wikipedia.org/wiki/Domain_Name_System) structure"
#                 ),
#             )
#         )
#         return

#     try:
#         data = await pc.urls.get_website(url_parsed["encoded"])
#     except plane.HTTPError as e:
#         await ctx.respond(
#             embeds.Embed(
#                 title="Analyze Error",
#                 description="An error occurred while analyzing the URL",
#             )
#         )
#         raise e
#     else:
#         embed = (
#             embeds.Embed(
#                 title="Analyze",
#                 description=url_parsed["input"],
#             )
#             .add_field("Fraudulent", str(data.is_fraudulent), inline=True)
#             .add_field("Information", data.message, inline=True)
#         )
#         await ctx.respond(embed)


# @analyze.with_command
# @tanchi.as_slash_command("user")
# async def analyze_user(
#     ctx: tanjun.abc.SlashContext,
#     session: alluka.Injected[aiohttp.ClientSession],
#     user: hikari.User,
# ) -> None:
#     """
#     Analyze a user for fraudulency

#     Parameters
#     ----------
#     user : hikari.User
#         User to analyze
#     """
#     async with session.get(
#         f"{scripty.AERO_API}/users/{user.id}/bans", headers=scripty.AERO_HEADERS
#     ) as response:
#         data = await response.json()

#         if not response.ok:
#             await ctx.respond(
#                 embeds.Embed(
#                     title="Analyze Error",
#                     description="An error occurred while analyzing the user",
#                 )
#             )

#             raise scripty.HTTPError(
#                 f"The Aero Ravy API returned a mentally unok {response.status} status"
#                 f" with the following data: {data}"
#             )

#         # TODO: The rest of this:
#         embed = embeds.Embed(description=f"```json\n{data}\n```")

#         await ctx.respond(embed)


loader_automod = component.load_from_scope().make_loader()
