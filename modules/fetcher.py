import logging
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .utils import normalize_url
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

USER_AGENT = "LinkSnake/1.0 (+https://linksnake.io/bot-info)"

async def get_links_bs4(url, base_domain, session):
    """Extract links using BeautifulSoup if JavaScript is not required."""
    headers = {"User-Agent": USER_AGENT}
    try:
        async with session.get(url, headers=headers, timeout=10, ssl=False) as response:
            if response.status != 200:
                logging.warning(f"Failed to fetch {url} (status: {response.status})")
                return set()

            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")

            links = {
                normalize_url(urljoin(url, a["href"]))
                for a in soup.find_all("a", href=True)
                if normalize_url(urljoin(url, a["href"])).startswith(base_domain)
            }
            return links
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
        return set()

async def get_links_playwright(url, base_domain, page):
    """Extract links using Playwright for JavaScript-rendered pages."""
    try:
        logging.info(f"Crawling: {url}")
        response = await page.goto(url, wait_until="domcontentloaded")

        if response.status != 200:
            return set()

        a_tags = await page.locator("a").all()
        links = {
            normalize_url(await a.get_attribute("href"))
            for a in a_tags if await a.get_attribute("href")
        }
        return {link for link in links if link.startswith(base_domain)}
    except PlaywrightTimeoutError:
        logging.error(f"Timeout while loading: {url}")
    except Exception as e:
        logging.error(f"Error fetching {url} with Playwright: {e}")
    return set()
