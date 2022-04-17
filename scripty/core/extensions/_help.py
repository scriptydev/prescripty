import typing

# import hikari
import lightbulb

# import miru

import scripty


class HelpCommand(lightbulb.BaseHelpCommand):
    async def send_bot_help(self, context: lightbulb.Context):
        await context.respond("This help command is currently in development.")

    async def send_plugin_help(
        self, context: lightbulb.Context, plugin: lightbulb.Plugin
    ):
        await context.respond("This help command is currently in development.")

    async def send_command_help(
        self, context: lightbulb.Context, command: lightbulb.Command
    ):
        await context.respond("This help command is currently in development.")

    async def send_group_help(
        self,
        context: lightbulb.Context,
        group: lightbulb.SlashCommandGroup
        | lightbulb.PrefixCommandGroup
        | lightbulb.SlashSubGroup
        | lightbulb.PrefixSubGroup,
    ):
        await context.respond("This help command is currently in development.")

    async def object_not_found(self, context: lightbulb.Context, obj: str):
        await context.respond("This help command is currently in development.")


def load(bot: scripty.core.BotApp):
    bot.d.old_help_command = bot.help_command
    bot.help_command = HelpCommand(bot)


def unload(bot: scripty.core.BotApp):
    bot.help_command = bot.d.old_help_command
    del typing.Any[bot.d.old_help_command]
