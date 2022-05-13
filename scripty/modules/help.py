__all__: list[str] = ["load_component", "unload_component"]

import miru
import tanchi
import tanjun

import scripty

component = tanjun.Component()


class HelpView(miru.View):
    def __init__(self):
        super().__init__()
        self.add_item(
            miru.Button(
                label="Website",
                url="https://scriptybot.web.app/",
            )
        )
        self.add_item(
            miru.Button(
                label="Docs",
                url="https://scriptydev.github.io/prescripty/",
            )
        )
        self.add_item(
            miru.Button(
                label="Commands",
                url="https://scriptydev.github.io/prescripty/reference/",
            )
        )
        self.add_item(
            miru.Button(
                label="Invite",
                url=scripty.INVITE_URL,
            )
        )


@component.with_command
@tanchi.as_slash_command("help")
async def help_(ctx: tanjun.abc.SlashContext) -> None:
    """Display the help interface"""
    view = HelpView()
    await ctx.respond(components=view.build())


@tanjun.as_loader
def load_component(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())


@tanjun.as_unloader
def unload_component(client: tanjun.Client) -> None:
    client.remove_component_by_name(component.name)
