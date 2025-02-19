import os
from urllib.parse import urlparse

def normalize_url(url):
    """Normalize URL by removing 'www.' and trailing slash."""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lstrip("www.")
    path = parsed_url.path.rstrip("/")
    return f"{parsed_url.scheme}://{domain}{path}"

def ensure_folder(domain):
    """Ensure the /data/{domain}/ folder exists."""
    folder = os.path.join("data", domain)
    os.makedirs(folder, exist_ok=True)
    return folder
