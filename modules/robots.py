import logging
import aiohttp
import re
from urllib.parse import urljoin

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

async def check_robots_txt(base_url):
    robots_url = f"{base_url}/robots.txt"
    logging.info(f"Checking robots.txt: {robots_url}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(robots_url) as response:
                if response.status == 200:
                    content = await response.text()
                    logging.info(f"robots.txt content:\n{content}")

                    # Extract Crawl-delay
                    match = re.search(r"Crawl-delay:\s*(\d+)", content, re.IGNORECASE)
                    if match:
                        return int(match.group(1))

    except Exception as e:
        logging.warning(f"Failed to fetch robots.txt: {e}")

    return 1  # Default delay = 1s ถ้าไม่มี Crawl-delay

