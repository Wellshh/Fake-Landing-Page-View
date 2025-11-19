import asyncio
import json
import random
import os
import shutil
import tempfile
from playwright.async_api import (
    async_playwright,
    Page,
    Request,
    Response,
    TimeoutError as PlaywrightTimeoutError,
    WebSocket,
)

from . import actions
from . import data
from .config import Config

class TrafficBot:
    def __init__(self, config: Config, identity: dict | None = None):
        self.config = config
        self.identity = identity

    async def run(self):
        print("Starting Traffic Bot...")
        proxy_config = self.config.get_proxy_config()
        use_proxy = self.config.use_proxy

        if proxy_config and use_proxy:
            # ... (proxy logging logic remains the same)

        else:
            print("WARNING: Running without proxy (Local IP mode)")
            use_proxy = False

        referer = random.choice(data.REFERERS)
        user_agent = data.USER_AGENT
        # This print statement can get noisy in multithreaded mode, consider removing or logging to a file.
        # print(f"Configuration: Referer={referer}, UA={user_agent}")

        async with async_playwright() as p:
            args = [
                "--disable-blink-features=AutomationControlled", "--no-sandbox",
                "--disable-setuid-sandbox", "--ignore-certificate-errors",
                "--ignore-ssl-errors", "--disable-web-security",
                "--disable-features=IsolateOrigins,site-per-process",
            ]

            is_ci = os.getenv("CI") == "true"
            headless_mode = not is_ci # Run headless in CI, with head locally for debugging

            geo_info = {"country": "US", "timezone": "America/New_York", "locale": "en-US"}

            if use_proxy and proxy_config:
                # ... (proxy detection logic remains the same)
                pass

            launch_kwargs = {
                "headless": headless_mode, "args": args, "user_agent": user_agent,
                "viewport": {"width": 1440, "height": 900},
                "locale": geo_info.get('locale', 'en-US'),
                "timezone_id": geo_info.get('timezone', 'America/New_York'),
            }

            if use_proxy and proxy_config:
                launch_kwargs["proxy"] = proxy_config

            user_data_dir = tempfile.mkdtemp(prefix="chrome_profile_")

            try:
                context = await p.chromium.launch_persistent_context(
                    user_data_dir, **launch_kwargs
                )
                page = context.pages[0] if context.pages else await context.new_page()

                await page.set_extra_http_headers({"Referer": referer, "DNT": "0"})
                # ... (init scripts remain the same)

                # actions.setup_network_logging(page) # Can be too verbose for concurrent runs

                try:
                    print(f"Navigating to {self.config.target_url}")
                    await page.goto(
                        self.config.target_url, timeout=120000, wait_until="domcontentloaded"
                    )
                    await page.wait_for_load_state("networkidle", timeout=60000)
                    await asyncio.sleep(random.uniform(5, 8))

                    await actions.random_sleep(2, 5)
                    await actions.random_mouse_move(page)
                    await actions.random_scroll(page)

                    should_convert = random.random() <= self.config.conversion_rate
                    if should_convert and self.config.form_fields:
                        identity_to_use = self.identity if self.identity else data.generate_identity()

                        print(f"Thread {os.getpid()}: Submitting as {identity_to_use.get('full_name', 'Unknown')}")

                        form_completed = await actions.fill_form(page, self.config.form_fields, identity_to_use)
                        if form_completed and self.config.submit_button:
                            submit_btn = await page.query_selector(self.config.submit_button)
                            if submit_btn:
                                await actions.random_mouse_move(page)
                                await submit_btn.hover()
                                await asyncio.sleep(1.0)
                                await submit_btn.click()
                                print(f"Thread {os.getpid()}: Form submitted.")
                                await asyncio.sleep(15)
                                # Consider unique screenshot names in concurrent mode
                                # await page.screenshot(path=f"success_{os.getpid()}.png")
                            else:
                                print(f"Submit button not found with selector: {self.config.submit_button}")
                        else:
                            print("Form not submitted. Check completion status or submit button config.")
                    else:
                        print(f"Thread {os.getpid()}: Simulating bounce.")

                    await actions.random_sleep(8, 12)

                except Exception as e:
                    print(f"Error in thread {os.getpid()}: {e}")
                finally:
                    await context.close()
            finally:
                try:
                    shutil.rmtree(user_data_dir)
                except Exception as e:
                    pass # Suppress cleanup errors in concurrent runs
