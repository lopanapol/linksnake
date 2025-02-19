import logging
import aiohttp
from urllib.parse import urljoin

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

async def check_robots_txt(base_url):
    """Check robots.txt to see if crawling is allowed."""
    robots_url = urljoin(base_url, "/robots.txt")
    headers = {"User-Agent": USER_AGENT}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(robots_url, headers=headers, timeout=5, ssl=False) as response:
                if response.status == 200:
                    text = await response.text()
                    logging.info(f"robots.txt content:\n{text}")
                    if "Disallow" in text:
                        logging.warning(f"robots.txt found at {robots_url}. Check before crawling!")
        except Exception:
            pass
