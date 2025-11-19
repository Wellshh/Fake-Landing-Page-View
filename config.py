import os
from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()


class Config:
    # Target URL
    TARGET_URL = os.getenv("TARGET_URL", "https://genma.lovable.app/")

    # Conversion rate for form submissions (0 - 1)
    # FORCE 1.0 for debugging to ensure we see POST requests
    CONVERSION_RATE = float(os.getenv("CONVERSION_RATE", "1.0"))

    # Proxy Configuration (Bright Data)
    PROXY_HOST = os.getenv("PROXY_HOST", "brd.superproxy.io:33335")
    PROXY_USER = os.getenv("PROXY_USER")
    PROXY_PASS = os.getenv("PROXY_PASS")

    # Validation
    @classmethod
    def validate(cls):
        missing = []
        if not cls.PROXY_USER:
            missing.append("PROXY_USER")
        if not cls.PROXY_PASS:
            missing.append("PROXY_PASS")

        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

        if not 0 <= cls.CONVERSION_RATE <= 1:
            raise ValueError("CONVERSION_RATE must be between 0 and 1.")

    @classmethod
    def get_proxy_config(cls):
        if not cls.PROXY_USER or not cls.PROXY_PASS:
            return None
        return {
            "server": f"http://{cls.PROXY_HOST}",
            "username": cls.PROXY_USER,
            "password": cls.PROXY_PASS,
        }
