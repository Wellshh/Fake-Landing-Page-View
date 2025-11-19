import random
import csv
from fake_useragent import UserAgent

REFERERS = [
    "https://www.facebook.com/",
    "https://www.facebook.com/",
    "https://www.facebook.com/",
    "https://www.facebook.com/",
    "https://www.reddit.com/",
]

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

EMAIL_DOMAINS = [
    "gmail.com", "hotmail.com", "outlook.com", "yahoo.com",
    "proton.me", "icloud.com", "aol.com",
]

COMPANY_SUFFIXES = [
    "Labs", "Studio", "Solutions", "Digital", "Analytics",
    "Partners", "Collective",
]

FIRST_NAMES = [
    "Alex", "Bella", "Carlos", "Diana", "Ethan", "Fiona", "Gabriel",
    "Hannah", "Isaac", "Julia", "Kevin", "Lara", "Mason", "Nina",
    "Owen", "Pablo", "Quinn", "Riley", "Sofia", "Tyler", "Valerie",
]

LAST_NAMES = [
    "Anderson", "Bennett", "Chang", "Diaz", "Evans", "Foster", "Garcia",
    "Hughes", "Ibarra", "Jackson", "Kelley", "Lopez", "Mitchell", "Nguyen",
    "Owens", "Parker", "Quintana", "Reed", "Sullivan", "Turner", "Valdez",
]

def generate_identity() -> dict:
    """Generate a realistic identity and email address"""
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    suffix = random.choice(COMPANY_SUFFIXES)
    number_suffix = str(random.randint(1, 97)) if random.random() < 0.35 else ""
    separator = random.choice([".", "_", ""])
    email = f"{first}{separator}{last}{number_suffix}@{random.choice(EMAIL_DOMAINS)}".lower()
    company = f"{last} {suffix}"
    return {
        "company": company,
        "email": email,
        "full_name": f"{first} {last}",
    }

def load_user_data(file_path: str) -> list[dict]:
    """
    Loads user data from a CSV file.
    The CSV file should have a header row with field names.
    """
    if not file_path:
        return []

    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        raise ValueError(f"Data file not found at: {file_path}")
    except Exception as e:
        raise ValueError(f"Error reading data file: {e}")
