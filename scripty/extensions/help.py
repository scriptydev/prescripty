import hikari
import lightbulb
import miru


class ScriptyHelpCommand(lightbulb.BaseHelpCommand):
    async def send_bot_help(self, context):
        await context.respond("This help command is currently in development.")

    async def send_plugin_help(self, context, plugin):
        await context.respond("This help command is currently in development.")

    async def send_command_help(self, context, command):
        await context.respond("This help command is currently in development.")

    async def send_group_help(self, context, group):
        await context.respond("This help command is currently in development.")

    async def object_not_found(self, context, obj):
        await context.respond("This help command is currently in development.")


def load(bot):
    bot.d.old_help_command = bot.help_command
    bot.help_command = ScriptyHelpCommand(bot)


def unload(bot):
    bot.help_command = bot.d.old_help_command
    del bot.d.old_help_command
