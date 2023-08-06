from gamesaver.src import search_deals
import click, sys


@click.group()
@click.version_option("0.1.0")
def main(**kwargs) -> int:
    """Find the best deals on PC games from the terminal"""
    return 0


@main.command()
@click.option(
    "--title",
    "-t",
    "title",
    required=False,
    type=str,
    help="Search deals for a specific game title",
)
@click.option(
    "--store",
    "-s",
    "store",
    required=False,
    type=str,
    help="Search all deals from a specific store",
)
def search(**kwargs):
    """Search for all deals."""
    search_deals(kwargs.get("title"), kwargs.get("store"))


if __name__ == "__main__":
    args = sys.argv
    sys.exit(main())
