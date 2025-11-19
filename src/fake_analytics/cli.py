import asyncio
import click
from concurrent.futures import ThreadPoolExecutor
from .core import TrafficBot
from .config import Config
from .data import load_user_data
from .discovery import discover_form_fields

@click.group()
def cli():
    """A tool to fake website analytics."""
    pass

def run_bot_instance(config, identity):
    """Wrapper function to run a single bot instance in an async event loop."""
    async def main():
        bot = TrafficBot(config, identity)
        await bot.run()

    asyncio.run(main())

@cli.command()
@click.option("--url", help="The target URL to visit.")
@click.option("--threads", default=1, help="The number of concurrent threads to run.")
@click.option("--config", "config_path", help="Path to a custom JSON config file.")
@click.option("--data-file", "data_path", help="Path to a CSV file with user data.")
def run(url, threads, config_path, data_path):
    """Run the traffic bot."""
    try:
        config = Config(config_path)
        if url:
            config.target_url = url

        user_data = load_user_data(data_path)

        if user_data:
            click.echo(f"Loaded {len(user_data)} user records from {data_path}")
            # If user data is provided, the number of threads is determined by the data
            threads = len(user_data)
            click.echo(f"Running with {threads} threads based on the data file.")

        with ThreadPoolExecutor(max_workers=threads) as executor:
            # If we have user data, map each record to a bot instance.
            # Otherwise, just run 'threads' number of instances with generated data.
            identities = user_data if user_data else [None] * threads

            futures = [executor.submit(run_bot_instance, config, identity) for identity in identities]

            for future in futures:
                future.result() # Wait for all threads to complete

        click.secho("All bot instances have completed their tasks.", fg="green")

    except ValueError as e:
        click.secho(str(e), fg="red")


@cli.command()
@click.option("--url", required=True, help="The URL to discover forms on.")
def discover(url):
    """Discover input fields on a page."""
    asyncio.run(discover_form_fields(url))

if __name__ == "__main__":
    cli()
