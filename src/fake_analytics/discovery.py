import asyncio
from playwright.async_api import async_playwright
import click

async def discover_form_fields(url: str):
    """
    Launches a headless browser to discover form fields on a given URL.
    """
    click.echo(f"🔍 Discovering form fields on {url}...")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            click.echo("Navigating to the page...")
            await page.goto(url, timeout=60000, wait_until="domcontentloaded")

            click.echo("Searching for input, textarea, and select elements...")

            # Select all relevant form elements
            elements = await page.query_selector_all("input, textarea, select")

            if not elements:
                click.secho("No form fields found on the page.", fg="yellow")
                return

            click.secho(f"✅ Found {len(elements)} potential form fields:", fg="green")

            field_details = []
            for element in elements:
                details = {
                    "tag": await element.evaluate("el => el.tagName.toLowerCase()"),
                    "type": await element.get_attribute("type") or "N/A",
                    "name": await element.get_attribute("name") or "N/A",
                    "id": await element.get_attribute("id") or "N/A",
                    "placeholder": await element.get_attribute("placeholder") or "N/A",
                    "aria-label": await element.get_attribute("aria-label") or "N/A",
                }
                field_details.append(details)

            # Print a formatted table
            click.echo("-" * 80)
            for item in field_details:
                click.echo(f"Tag: {item['tag']}, Type: {item['type']}, Name: {item['name']}, ID: {item['id']}")
            click.echo("-" * 80)
            click.secho(
                "Use the 'name' or 'id' above to create your JSON configuration file for the 'run' command.",
                fg="cyan"
            )

            await browser.close()
    except Exception as e:
        click.secho(f"An error occurred during discovery: {e}", fg="red")
