__all__: list[str] = ["load_component", "unload_component"]

import aiohttp
import alluka
import tanchi
import tanjun
import scripty

component = tanjun.Component()

analyze = component.with_slash_command(
    tanjun.slash_command_group("analyze", "Safety analysis for moderation")
)


@analyze.with_command
@tanchi.as_slash_command("url")
async def analyze_url(
    ctx: tanjun.abc.Context, session: alluka.Injected[aiohttp.ClientSession], url: str
) -> None:
    """Analyze URL safety

    Parameters
    ----------
    url : str
        URL to analyze
    """
    url_parsed = scripty.validate_and_encode_url(url)

    if url_parsed is None:
        await ctx.respond(
            scripty.Embed(
                title="Analyze Error",
                description=(
                    "Provided URL is invalid!\n"
                    "Please check if it includes `http(s)://` and complies with the "
                    "[DNS](https://en.wikipedia.org/wiki/Domain_Name_System) structure"
                ),
            )
        )
        return

    async with session.get(
            f"https://ravy.org/api/v1/urls/{url_parsed}",
            headers={"Authorization": f"Ravy {scripty.AERO_API_KEY}"},
        ) as response:
        data = await response.json()

        if not response.ok:
            await ctx.respond(
                scripty.Embed(
                    title="Analyze Error",
                    description="An error occurred while analyzing the URL",
                )
            )


            raise scripty.HTTPError(
                f"The Aero Ravy API returned a mentally unok {response.status} status"
                f" with the following data: {data}"
            )

        embed = (
            scripty.Embed(
                title="Analyze",
                description=url,
            )
            .add_field("Fraudulent", data["isFraudulent"], inline=True)
            .add_field("Information", data["message"], inline=True)
        )

        await ctx.respond(embed)


@tanjun.as_loader
def load_component(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())


@tanjun.as_unloader
def unload_component(client: tanjun.Client) -> None:
    client.remove_component_by_name(component.name)
