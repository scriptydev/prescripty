__all__: list[str] = ["loader_dev"]

import pathlib

import alluka
import tanjun

import scripty


@tanjun.with_owner_check(error_message=None)
@tanjun.with_argument("module")
@tanjun.as_message_command("load")
async def load(
    ctx: tanjun.abc.MessageContext,
    client: alluka.Injected[tanjun.Client],
    module: str,
) -> None:
    """Load module

    Parameters
    ----------
    module : str
        Module to load
    """
    await client.reload_modules_async(pathlib.Path(f"scripty/modules/{module}.py"))
    await ctx.respond(
        scripty.Embed(
            title="Load",
            description=f"`{module}` module loaded",
        )
    )


@tanjun.with_owner_check(error_message=None)
@tanjun.with_argument("module")
@tanjun.as_message_command("reload")
async def reload(
    ctx: tanjun.abc.MessageContext,
    client: alluka.Injected[tanjun.Client],
    module: str,
) -> None:
    """Reload module

    Parameters
    ----------
    module : str
        Module to reload
    """
    await client.reload_modules_async(pathlib.Path(f"scripty/modules/{module}.py"))
    await ctx.respond(
        scripty.Embed(
            title="Load",
            description=f"`{module}` module reloaded",
        )
    )


@tanjun.with_owner_check(error_message=None)
@tanjun.as_message_command("sync")
async def sync(
    ctx: tanjun.abc.MessageContext,
    client: alluka.Injected[tanjun.Client],
) -> None:
    """Sync global application commands"""
    await client.declare_global_commands()
    await ctx.respond(
        scripty.Embed(
            title="Sync",
            description="Successfully synced global application commands",
        )
    )


@tanjun.with_owner_check(error_message=None)
@tanjun.with_argument("module")
@tanjun.as_message_command("unload")
async def unload(
    ctx: tanjun.abc.MessageContext,
    client: alluka.Injected[tanjun.Client],
    module: str,
) -> None:
    """Unload module

    Parameters
    ----------
    module : str
        Module to unload
    """
    if "dev" in module:
        await ctx.respond(
            scripty.Embed(
                title="Unload Error",
                description=f"`{module}` cannot be unloaded!",
            )
        )
        return

    client.unload_modules(pathlib.Path(f"scripty/modules/{module}.py"))
    await ctx.respond(
        scripty.Embed(
            title="Unload",
            description=f"`{module}` module unloaded",
        )
    )


loader_dev = tanjun.Component(name="dev").load_from_scope().make_loader()
