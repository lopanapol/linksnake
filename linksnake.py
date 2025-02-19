import argparse
import asyncio
import logging
import aiohttp
from urllib.parse import urlparse
from playwright.async_api import async_playwright

from modules.utils import normalize_url, ensure_folder
from modules.robots import check_robots_txt
from modules.fetcher import get_links_bs4, get_links_playwright
from modules.parser import save_links, export_json, generate_sitemap

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

async def crawl(base_url, output_folder, limit):
    visited_links = set()
    queue = [base_url]
    output_txt = f"{output_folder}/links.txt"

    # Get crawl delay from robots.txt
    crawl_delay = await check_robots_txt(base_url)

    async with aiohttp.ClientSession() as session:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            while queue and len(visited_links) < limit:
                url = queue.pop(0)
                if url in visited_links:
                    continue

                logging.info(f"Crawling: {url}")
                visited_links.add(url)

                # Save immediately after discovering a new link
                await save_links(sorted(visited_links), output_txt)

                links = await get_links_bs4(url, base_url, session) or await get_links_playwright(url, base_url, page)

                queue.extend(link for link in sorted(links) if link not in visited_links)

                # Respect crawl delay
                await asyncio.sleep(crawl_delay)

            await browser.close()

def parse_args():
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Full Web Crawler")
    parser.add_argument("-u", "--url", required=True, help="Base domain to start crawling")
    parser.add_argument("-l", "--limit", type=int, default=10, help="Max number of URLs to crawl")
    return parser.parse_args()

async def main(args):
    base_url = normalize_url(f"https://{args.url.strip('/')}")
    domain_name = urlparse(base_url).netloc
    output_folder = ensure_folder(domain_name)

    await check_robots_txt(base_url)
    await crawl(base_url, output_folder, args.limit)

def entry_point():
    """Entry point for CLI execution."""
    args = parse_args()
    asyncio.run(main(args))

if __name__ == "__main__":
    entry_point()
