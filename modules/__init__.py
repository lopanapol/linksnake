# modules/__init__.py

# Import modules to make them accessible when importing `modules`
from .utils import normalize_url, ensure_folder
from .fetcher import get_links_bs4, get_links_playwright
from .parser import save_links, export_json, generate_sitemap
from .storage import save_to_file
from .robots import check_robots_txt
